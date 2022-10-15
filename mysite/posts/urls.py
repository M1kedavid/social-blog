from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:pk>/about/', views.PostDetail.as_view(), name='post_detail'),
    path('new/in/<slug:slug>', views.CreatePost.as_view(), name='create'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete'),
    path('edit/<int:pk>', views.EditPost.as_view(), name='edit'),
    path('like/<int:id>', views.like_post, name='like_post'),
]
