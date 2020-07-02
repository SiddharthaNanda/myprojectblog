from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class PostView(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    post = models.ForeignKey('Post',related_name='comments' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length = 200)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add= True)
    comment_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Author,on_delete = models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    content = RichTextUploadingField(blank=True,null=True)
    previous_post = models.ForeignKey('self',related_name='previous',null=True,blank=True,on_delete=models.SET_NULL)
    next_post = models.ForeignKey('self',related_name='next',null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post',kwargs={'pk':self.pk})

    def get_comment(self):
        return self.comments.all().order_by('-timestamp')

    def get_update_url(self,pk):
        return reverse('post_update',kwargs={'pk':self.pk})

    def get_delete_url(self,pk):
        return reverse('post_delete',kwargs={'pk',self.pk})

    def get_create_url(self):
        return reverse('post_create')

    def view_count(self):
        return PostView.objects.filter(post=self).count()

    def comment_count(self):
        return Comment.objects.filter(post=self).count()
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=5000,default='')
    email = models.CharField(max_length=100,default='')

    phone = models.PositiveIntegerField()
    message= models.CharField(max_length=5000,default='')
    def __str__(self):
        return self.name
