from django.urls import path
from Blog_App import views

urlpatterns = [
    path("", views.index, name='index'),
    path("about_us/", views.about_me, name='about_me'),
    path("contact_me/", views.contact_me, name='contact_me'),
    path("single_post/<str:slug>", views.single_post, name='single_post'),
    
    path("login/", views.login, name="login"),
    path('logout_view/', views.logout_view, name='logout_view'),
    path("register/", views.register, name="register"),
    path("verify/<str:auth_token>", views.verify, name='verify'),

    path("add_comment/", views.add_comment, name='add_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('my_profile/', views.my_profile, name='my_profile'),

]
