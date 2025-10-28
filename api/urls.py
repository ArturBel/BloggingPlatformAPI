from django.urls import path
from . import auth, posts_crud
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path(route='register/', view=auth.register, name='Registration'),
    path(route='login/', view=auth.login, name='Login'),
    path(route='posts/', view=posts_crud.create_and_read_all, name='Create new post or read all posts'),
    path(route='posts/<int:pk>', view=posts_crud.specific_post, name='Post by its pk (id)'),
    path(route='refresh/', view=TokenRefreshView.as_view(), name='Refresh endpoint')
]