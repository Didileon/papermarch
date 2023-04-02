from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import get_object_or_404, render


class PostsList(ListView):
    model = Post
    ordering = 'title'
    ordering = '-dateCreation'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    ordering = '-dateCreation'
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class SearchDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'flatpages/delete.html'
    success_url = '/posts/'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/edit.html'
    success_url = '/posts/'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/create.html'
    success_url = '/posts/'


class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})
