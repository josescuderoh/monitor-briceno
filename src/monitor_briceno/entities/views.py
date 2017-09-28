from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import UserProfileForm, UserProfileFormUpdate
from .models import UserProfile


# User views
def register(request):
    """This view is used to render the registration form and create the new user in the database."""

    registered = False
    # Check if is already logged in
    if request.user.is_authenticated():
        return render(request, 'entities/already_logged_in.html')
    # If method is post
    elif request.method == "POST":
        user_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            # Store extra information
            user = user_form.save(commit=False)
            # Clean password
            password1 = user_form.cleaned_data['password1']
            user.set_password(password1)
            # Inactive until email confirmation
            user.is_active = False
            user.save()
            registered = True

            # # Send verification email
            # site_domain = get_current_site(request).domain
            # send_verification_email.delay(user.pk, site_domain)

        else:
            print(user_form.errors)
    # If method is get
    else:
        user_form = UserProfileForm()

    return render(request, 'entities/registration_form.html',
                  {'user_form': user_form,
                   'registered': registered})


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponseRedirect('/projects')
#     else:
#         return HttpResponse('El link de activación es inválido.')


@login_required
def edit_user(request, pk):

    updated = False

    user = UserProfile.objects.get(pk=pk)
    user_form = UserProfileFormUpdate(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileFormUpdate(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save()
                created_user.save()
                updated = True

        return render(request, "entities/profile_form.html", {
            "noodle": pk,
            "user_form": user_form,
            "updated": updated,
        })
    else:
        raise PermissionDenied
