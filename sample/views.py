from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
# def post_list(request):
#     return render(request, 'blog/post_list.html', {})

def post_list(request):
    posts = Post.objects.all().order_by('created_date')
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    print(pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        print (form)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# def post_delete(request, pk):
    
#     return redirect('post_list')
def post_delete(request, pk):
    print(request.method)
    new_to_delete = get_object_or_404(Post, pk=pk)
    #+some code to check if this object belongs to the logged in user
    if request.method == 'POST':
        new_to_delete.delete()
        return redirect('post_list') # wherever to go after deleting

        # print('form',form)
        # if form.is_valid(): # checks CSRF
        #     new_to_delete.delete()
        #     return HttpResponseRedirect("/") # wherever to go after deleting
        
    else:
        form = PostForm(instance=new_to_delete)

    template_vars = {'form': form}
    return render(request, 'blog/post_edit.html', template_vars)