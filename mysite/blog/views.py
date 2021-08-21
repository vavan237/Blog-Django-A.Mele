from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

#class PostListView(ListView):
	#queryset = Post.published.all()
	#context_object_name = 'posts'
	#paginate_by = 3
	#template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag=None 

	if tag_slug:
		tag=get_object_or_404(Tag, slug=tag_slug)
		object_list=object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts= paginator.page(page)	
		
	except PageNotAnInteger:
		#Если страница не целое число, вернуть 1 cтраницу
		posts = paginator.page(1)
	except EmptyPage:
		#Если номер страницы больше общего колличества страниц возвращаем последнюю
		posts = paginator.page(paginator.num_pages)		
	#posts = Post.published.all()
	return render (request, 'blog/post/list.html', {'page':page,'posts': posts, 'tag':tag})

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
								   status='published',
								   publish__year=year,
								   publish__month=month,
								   publish__day=day)

	# List of active comments for this post
	comments = post.comments.filter(active=True)
	new_comment = None

	
	if request.method != 'POST':
		comment_form = CommentForm()
	else:
		comment_form = CommentForm(data = request.POST)	
		# A comment was posted
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet          
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			
			# Save the comment to the database
			new_comment.save()
			return redirect(post)	
	post_tags_ids=post.tags.values_list('id', flat=True)
	similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]                 
	return render(request,
			  	'blog/post/detail.html',
			  	{'post': post, 'comments':comments,
			  	'new_comment':new_comment,	   		
			   	'comment_form': comment_form,
			   	'similar_posts':similar_posts})


def post_share(request, post_id):
	#получение статьи по ID
	form = EmailPostForm()
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False 
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			post_url=request.build_absolute_uri(my_post.get_absolute_url())
			subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'vavan@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
			