from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from .models import Category, Tag, Post, Comment
from .forms import UserRegisterForm, UserLoginForm, CommentForm
from django.contrib.auth import login, logout
from django.db.models import F, Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from django.contrib.auth.models import User


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'  # замена obj_list
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic blog'
        context['post'] = Post.objects.order_by('-views')[0]
        # context['post'] = Post.objects.get(pk=9)
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


def post_detail(request, slug):
    template_name = 'blog/single.html'

    post = get_object_or_404(Post, slug=slug)
    post.views = F('views') + 1
    post.save()
    post.refresh_from_db()

    comments = Comment.objects.filter(Q(post_id=post.id) & Q(moderation=True))

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form, })


class PostByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно.\nВойдите в свой аккаунт ниже')
            return redirect('home')
        else:
            messages.warning(request, 'Ошибка при регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

# система лайков и комментариев еще недоработана...
def LikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('single', args=[str(comment.post.slug)]))
