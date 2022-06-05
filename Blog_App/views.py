from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Blog_Post, Blog_Comment, User_Profile, Contacts
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import mail
import uuid
from .forms import BlogPostForm

# Create your views here.


def index(request):
    posts = Blog_Post.objects.filter(is_approved=True)
    last3 = posts.order_by('-sl_no')[:3][::-1]
    
    context = {"posts": posts, 'last1': last3[2], 'last2': last3[1], 'last3': last3[0]}
    return render(request, "index.html", context)


def about_me(request):
    return render(request, "about.html")


def contact_me(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        emails = request.POST.get('email')
        message = request.POST.get('message')
        print(name, emails, phone, message)
        contact = Contacts(name=name, phone=phone, email=emails, message=message)
        contact.save()

        messages.success(request, "Message has been sent successfuly!")
        return redirect('/contact_me')
    return render(request, "contact.html")


def single_post(request, slug):
    post = Blog_Post.objects.get(slug=slug)
    comments = Blog_Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments}
    return render(request, "single-post.html", context)

# add blog post by user
def create_post(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'Please Login to create a blog post.')
        return redirect('/')
    
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        
        blog_obj = Blog_Post.objects.create(author=author, title=title,image=image, content=content)
        blog_obj.save()
        messages.success(request, 'Blog post created successful!')
        return redirect('/create_post')
            
    return render(request, 'create-post.html')

# @login_required(login_url='/add_comment')
def add_comment(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment")
        post_sl_no = request.POST.get("sl_no")
        post = Blog_Post.objects.get(sl_no=post_sl_no)

        comment = Blog_Comment.objects.create(user=user, comment=comment, post=post)
        comment.save()
    return redirect(f"/single_post/{post.slug}")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, "User not found.")
            return redirect("/login")

        profile_obj = User_Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, "Your account is not verified, Check your mail to verify.")
            return redirect("/")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, authenticate(request, username=username, password=password))
            return redirect("/")

        if user is None:
            messages.success(request, "Wrong username or password!")
            return redirect("/")
        auth_login(request, user)
        messages.success(request, 'Login successfull!')
        return redirect("/")

    # return render(request, "login.html")
    return redirect('/')


def logout_view(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You wasn\'t Logged-In.')
        return redirect('/')
    
    logout(request)
    messages.success(request, "You are Logged-Out!")
    return redirect('/')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = str(request.POST.get("password"))
        password_2 = str(request.POST.get("password_2"))
        try:
            if User.objects.filter(username=username).exists() and username != "":
                messages.success(request, "Username already exists.")
                return redirect("/")
            if User.objects.filter(email=email).exists() and email != "":
                messages.success(request, "Your email already exists.")
                return redirect("/")
            if len(password) < 4 or password == "" or password == " ":
                messages.success(
                    request, "Please, Enter atleast 4 charecter as your password.")
                return redirect("/register")
            if password != password_2:
                messages.success(request, "Please, Enter the same password.")
                return redirect("/")

            try:
                user_obj = User.objects.create_user(username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()

                auth_token = str(uuid.uuid4())
                user_profile_obj = User_Profile.objects.create(user=user_obj, auth_token=auth_token)
                user_profile_obj.save()

                verify_mail(email, auth_token)
                messages.success(request, 'Your account created. We sent you a confirmation mail.')
                return redirect('/')
                
            except Exception as e:
                print(e)
                messages.success(request, "Something went wrong!")
                return redirect(request, "/")

        except Exception as e:
            print(e)
            # return render(request, "register.html")
            return redirect('/')

    else:
        return redirect("/")


def verify_mail(email, auth_token):
    subject = "Verify your email address."
    message = f"Please, Copy this link and paste it in your browser to verify your accounts: http://127.0.0.1:8000/verify/{auth_token}"
    admin_email_info = settings.EMAIL_HOST_USER
    receiver = [email]
    mail.send_mail(subject, message, admin_email_info, receiver)


# This funtion have no use right now. i will use it later, for now verify autometically
def verify(request, auth_token):
    user_obj = User_Profile.objects.filter(auth_token=auth_token).first()
    if user_obj:
        if user_obj.is_verified:
            messages.success(request, "Your account is already verified.")
            return redirect("/login")
        user_obj.is_verified = True
        user_obj.save()
        messages.success(
            request, "Congratulations, Your accout has been verified.")
        return redirect("/login")
    else:
        return HttpResponse("<h3>Something went wrong!</h3>")


def my_profile(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'Please Login to open your profile.')
        return redirect('/')

    user_profile_obj = User_Profile.objects.get(user=request.user)
    user_obj = User.objects.get(username=request.user.username)
    context = {'user': user_obj, 'user_profile': user_profile_obj}
    
    if request.method == 'POST':
        avatar = request.FILES.get('image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if avatar is not None:
            user_profile_obj.avatar = avatar
            user_profile_obj.save()
            
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.save()
        messages.success(request, 'Profile updated successful!')
    
    return render(request, "my-profile.html", context)

def search(request):
    query = request.GET.get('query')
    all_posts = Blog_Post.objects.filter(is_approved=True)
    if len(query) > 60:
        all_posts = Blog_Post.objects.none()
        messages.warning(request, 'Please, search some short keywords, Thanl you!')
    if len(query) <= 0:
        all_posts = Blog_Post.objects.none()
        messages.warning(request, 'You can\'t search an empty value.')
    else:
        all_posts_title = Blog_Post.objects.filter(title__icontains=query)
        all_posts_content = Blog_Post.objects.filter(content__icontains=query)
        all_posts = all_posts_title.union(all_posts_content)
        
    if all_posts.count() <= 0:
        messages.warning(request, 'No results found, Please refine your query!')

    context = {'all_posts': all_posts, 'query': query}
    return render(request, 'search_query.html', context)