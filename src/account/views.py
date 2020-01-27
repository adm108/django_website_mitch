from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticatedForm, \
    AccountUpdateForm
from blog.models import BlogPost


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # collect email and password from form and authenticate it during
            # creating account, next login and redirect to home
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            # name home in url
            return redirect('home')
        else:
            context['registration_form'] = form
    # get request - when it is not POST, we want to go again to register page
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticatedForm(request.POST)

        # if form is valid, if not it will show ValidationError from forms !
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            # if user exists
            if user:
                login(request, user)
                return redirect('home')

    else:
        form = AccountAuthenticatedForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):
    # go to login page if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    # instance for taking user's pk to check correctness
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        # saving changes in database
        if form.is_valid():
            # form initial remember email and username after changing and
            # shows it after saving to the databases
            form.initial = {
                'email': request.POST['email'],
                'username': request.POST['username']
            }
            form.save()
            context['success_message'] = "Updated"

    else:
        # initial option displays user's email and username
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username
            }
        )
    context['account_form'] = form

    # adding all user's post to his/her account view
    blog_post = BlogPost.objects.filter(author=request.user)

    context['blog_posts'] = blog_post

    return render(request, 'account/account.html', context)


def must_authenticate(request):
    return render(request, 'account/must_authenticate.html', {})
