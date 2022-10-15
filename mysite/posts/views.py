from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from .models import Post
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from groups.models import Group
User = get_user_model()
# Create your views here.


class PostDetail(generic.DetailView):
    template_name = 'posts/post_detail.html'
    model = Post


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ['title', 'message']
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.group = Group.objects.filter(
            slug=self.kwargs['slug']).get()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.object.pk})


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('groups:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)


class EditPost(generic.UpdateView):
    model = Post
    template_name = 'posts/post_edit_form.html'
    fields = ['title', 'message']

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.object.pk})


@login_required
def like_post(request, id):
    if request.method == "POST":
        instance = Post.objects.get(id=id)
        if not instance.likes.filter(id=request.user.id).exists():
            instance.likes.add(request.user)
            instance.save()
            return render(request, 'partials/likes_area.html', context={'post': instance})
        else:
            instance.likes.remove(request.user)
            instance.save()
            return render(request, 'partials/likes_area.html', context={'post': instance})
