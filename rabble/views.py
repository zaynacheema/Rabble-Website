from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import SubRabble, Post, Comment
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def index(request):
#context = {"welcome": "Hello, world!"}

#return render(request, "rabble/index.html", context)
    subrabbles = SubRabble.objects.filter(community_id=1)
    return render(request, "rabble/index.html", {"subrabbles": subrabbles})

@login_required
def subrabble_detail(request, identifier):
    subrabble = get_object_or_404(SubRabble, id=identifier)
    posts = Post.objects.filter(subrabble=subrabble)

    return render(request, "rabble/subrabble_detail.html", {
        "subrabble": subrabble,
        "posts": posts
    })

@login_required
def post_detail(request, identifier, pk):
    subrabble = get_object_or_404(SubRabble, id=identifier)
    post = get_object_or_404(Post, pk=pk, subrabble=subrabble)

    return render(request, "rabble/post_detail.html", {
        "subrabble": subrabble,
        "post": post
    })

@login_required
def post_create(request, identifier):
    subrabble = get_object_or_404(SubRabble, id=identifier)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.subrabble = subrabble
            post.save()
            return redirect("post-detail", identifier=subrabble.id, pk=post.pk)
    else:
        form = PostForm()

    return render(request, "rabble/post_form.html", {
        "form": form,
        "subrabble": subrabble
    })

@login_required
def post_edit(request, identifier, pk):
    subrabble = get_object_or_404(SubRabble, id=identifier)
    post = get_object_or_404(Post, pk=pk, subrabble=subrabble)
    
    if post.author != request.user:
        return HttpResponseForbidden("You’re not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", identifier=subrabble.id, pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "rabble/post_form.html", {
        "form": form,
        "subrabble": subrabble
    })

@login_required
def profile(request):
    return render(request, "rabble/profile.html")
