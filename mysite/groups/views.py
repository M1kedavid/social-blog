from sqlite3 import IntegrityError
from urllib import request
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Group, GroupMember
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

    def form_valid(self, form):
        result = super().form_valid(form)
        GroupMember.objects.create(user=self.request.user, group=self.object)
        return result


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group


class UserGroups(LoginRequiredMixin, generic.ListView):
    model = Group
    select_related = ('user', 'group')
    template_name = 'groups/group_user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user_groups = Group.objects.filter(
            members__id=self.request.user.id)
        context['user_groups'] = self.user_groups
        return context


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning already a member!')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user, group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not a member!')
        else:
            membership.delete()
        return super().get(request, *args, **kwargs)
