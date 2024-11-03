from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import UserFile
from .forms import RegisterForm, LoginForm, UpdateUserForm, FileForm


@login_required
def home(request):
    return render(request, 'home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "Мы отправили вам по электронной почте инструкции по установке вашего пароля, " \
                      "если существует учетная запись с указанным вами адресом электронной почты." \
                      " Если вы не получили электронное письмо, " \
                      "пожалуйста, убедитесь, что вы ввели адрес, на который указывали при регистрации, и проверьте свою папку со спамом."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Пароль успешно изменён"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль успешно обновлён')
            return redirect(to='users-profile')
    else:   
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'profile.html', {'user_form': user_form})

@login_required
def upload_file(request):
    
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.save()
            messages.success(request, 'Файл успешно загружен!')
            return redirect(to='all_files')
    else:
        form = FileForm(instance=request.user)
        
    return render(request, 'post.html', {'form': form})

@login_required
def all_files(request):
    data = UserFile.objects.filter(user=request.user)
    return render(request, 'files.html', {'data': data})