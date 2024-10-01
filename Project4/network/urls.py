from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:i>", views.index, name="page"),
    path("following",views.following,name="following"),
    path('update_post/<int:post_id>', views.update_post, name='update_post'),
    path("following/page/<int:i>",views.following,name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("follows_count/<int:user_id>", views.follows_count, name="follows"),
    path("toggle_follow/<int:user_id>",views.toggle_follow, name="toggle_follow"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>",views.profile_load,name="profile"),
    path("profile/<int:user_id>/page/<int:i>",views.profile_load,name="profile")

]
