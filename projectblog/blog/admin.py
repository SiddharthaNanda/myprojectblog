from django.contrib import admin
from blog.models import Author,Category,Post,Comment,PostView,Contact

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Contact)
