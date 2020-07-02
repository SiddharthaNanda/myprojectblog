from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Author,PostView,Contact
from subscribe.models import Signup
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Count,Q
from blog.forms import CommentForm,PostForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    else:
        return None

def search(request):
    queries = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queries = queries.filter(Q(title__icontains=query)|Q(overview__icontains=query)|Q(content__icontains=query)).distinct()

    context={'queries':queries}

    return render(request,'search_result.html',context)


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    posts = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    return render(request,'index.html',{'posts':posts,'latest':latest})

def blog(request):
    category_count = get_category_count()

    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list,4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    return render(request,'blog.html',{'paginated_queryset':paginated_queryset,'page_request_var':page_request_var,'most_recent':most_recent,'category_count':category_count})

def post(request,pk):
    post =get_object_or_404(Post,pk =pk)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()
    form = CommentForm(request.POST or None)
    if request.user.is_authenticated:

        PostView.objects.get_or_create(user=request.user,post=post)
    if request.method == "POST":
        if form.is_valid():
            form.instance.post=post
            form.instance.user = request.user
            form.save()
            return redirect(reverse('post',kwargs={'pk':post.pk}))

    return render(request,'post.html',{'post':post,'most_recent':most_recent,'category_count':category_count,'form':form})

def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    title='Create'
    author = get_author(request.user)
    if form.is_valid():
        form.instance.author = author
        form.save()
        return redirect(reverse('post',kwargs={'pk':form.instance.pk}))

    return render(request,'post_create.html',{'form':form,'title':title})

def post_update(request,pk):
    post = get_object_or_404(Post,pk=pk)
    title='Update'
    form = PostForm(request.POST or None,request.FILES or None,instance=post)
    author = get_author(request.user)
    if form.is_valid():
        form.instance.author = author
        form.save()
        return redirect(reverse('post',kwargs={'pk':form.instance.pk}))

    return render(request,'post_create.html',{'form':form,'title':title})

def post_delete(request,pk):
    post= get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect(reverse('blog'))

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone=request.POST.get('phone','')
        message = request.POST.get('message','')
        contact = Contact(name=name,email=email,phone=phone,message=message)
        contact.save()



        return render(request,'contact.html',{'name':name})
    else:
        return render(request,'contact.html',{})
