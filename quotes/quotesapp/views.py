from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Quote, Tag, Author
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, "quotesapp/index.html", {"quotes": quotes})


def authors(request):
    authors = Author.objects.all().order_by("full_name")
    return render(request, "quotesapp/authors.html", {"authors": authors})


def login(request):
    return render(request, "quotesapp/login.html")


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "quotesapp/author_detail.html", {"author": author})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("quotesapp:index")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "quotesapp/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "quotesapp/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "quotesapp/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "quotesapp/signup.html")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        auth_login(request, user)
        return redirect("quotesapp:index")

    return render(request, "quotesapp/signup.html")


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect("quotesapp:author_detail", author_id=author.id)
    else:
        form = AuthorForm()
    return render(request, "quotesapp/add_author.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            return redirect("quotesapp:index")
    else:
        form = QuoteForm()
    return render(request, "quotesapp/add_quote.html", {"form": form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password successfully updated!')
                return redirect('quotesapp:index')
            except Exception as e:
                messages.error(request, f'Error changing password: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'quotesapp/change_password.html', {'form': form})
