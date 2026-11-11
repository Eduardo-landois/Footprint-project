from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

# Always get the user model this way, so it points at our custom accounts.User
User = get_user_model()


def is_admin(user):
    # Who can manage users: the Admin role, or a superuser
    # (createsuperuser makes Runners by default, so this lets that account in)
    return user.role == User.Role.ADMIN or user.is_superuser


# Home page: home.html shows different content for logged-in users
def home(request):
    return render(request, 'home.html')


def signup(request):
    errors = []
    username = ''
    email = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        # Passwords are not stripped: spaces can be part of a password
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('That username is already taken.')

        if '@' not in email:
            errors.append('Enter a valid email address.')

        if password1 != password2:
            errors.append("The two passwords don't match.")
        else:
            # Django's password rules (min length, not too common, not all numbers)
            try:
                validate_password(password1)
            except ValidationError as e:
                errors.extend(e.messages)

        if not errors:
            # create_user saves the password hashed; role defaults to Runner
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')

    # GET, or POST with errors: show the form again and keep what they typed
    return render(request, 'accounts/signup.html', {
        'errors': errors,
        'username': username,
        'email': email,
    })


@login_required
def profile(request):
    # The template reads the logged-in user from {{ user }}
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    errors = []

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        if '@' not in email:
            errors.append('Enter a valid email address.')

        if not errors:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return redirect('profile')
    else:
        # GET: fill the form with the user's current details
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email

    return render(request, 'accounts/edit_profile.html', {
        'errors': errors,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    })


@login_required
def user_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only admins can manage users.")

    users = User.objects.all().order_by('username')
    return render(request, 'accounts/user_list.html', {
        'users': users,
        'roles': User.Role.choices,  # [('runner', 'Runner'), ...] for the dropdown
    })


@login_required
def change_role(request, user_id):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only admins can manage users.")

    if request.method == 'POST':
        member = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role', '').strip()
        # Only accept real roles, and don't let admins change their own
        # role (they could lock themselves out of this page)
        if new_role in User.Role.values and member != request.user:
            member.role = new_role
            member.save()

    return redirect('user_list')
