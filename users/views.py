from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


from users.forms import UserCreateForm, UserUpdateForm

class RegisterView(View):
    def get(self,request):
        create_form = UserCreateForm
        context = {
            "form":create_form
        }
        return render(request,'users/register.html', context)

    def post(self,request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            # username = request.POST['username']
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # email = request.POST['email']
            # password = request.POST['password']
            #
            # user = User.objects.create(
            #     username = username,
            #     first_name = first_name,
            #     last_name = last_name,
            #     email = email
            # )
            # user.set_password(password)
            # user.save()


            # create user account
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/register.html', context)


class LogInView(View):
    def get(self,request):
        login_form = AuthenticationForm()
        context = {
            "login_form":login_form
        }
        return render(request,'users/login.html', context)

    def post(self,request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)
            messages.success(request, "You have succesfully logged in.")
            return redirect("books:list")
        else:
            context = {
                "login_form": login_form
            }
            return render(request, 'users/login.html', context)


class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        # if not request.user.is_authenticated:
        #     return redirect("users:login")
        context = {
            "user":request.user
        }
        return render(request,"users/profile.html",context)


class LogoutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        messages.info(request, "You have succesfully logged out.")
        return redirect("landing_page")



class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self,request):
        user_update_form = UserUpdateForm(instance=request.user)
        context = {
            "form":user_update_form
        }
        return render(request, "users/profile_edit.html", context)

    def post(self,request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        context = {
            "form":user_update_form
        }
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully update your profile")
            return redirect("users:profile")
        return render(request, "users/profile_edit.html", context)
