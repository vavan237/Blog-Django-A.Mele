from django.contrib.sitemaps import Sitemap 
from .models import Post

class PostSitemap (Sitemap):
	chengefreq = 'weekly'
	priority = 0.9

	def items(self):
		return Post.published.all()

	def lastmode(self, obj):
		return odj.updated	