from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
	title = 'My blog'
	link = '/blog/'
	description = 'New posts of my blog'

	def items(self):
		return Post.published.all()[:5]

	def items_title(self):
		return item.title	

	def items_description(self):
		return items.truncatewords(item.body, 30)		