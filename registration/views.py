from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse

from authorization.models import ProFile
from services.forms import RegisterUserForm
from services.registration import registration
from django.contrib.auth import login
from services.generate_id import generate_random_num
from authorization.models import UserFile
from werkzeug.security import generate_password_hash


class RegisterUser(CreateView):
    template_name = 'reg.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('/')

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        return dict(list(context.items()))

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            create_user_file = CreateUserFile(request)
            create_user_file.creator(request)
            print(create_user_file.user.id)
            return redirect(f'http://localhost:8000/users/{create_user_file.user.id}')
        return render(request, 'reg.html', {'form': RegisterUserForm})


class CreateUserFile:

    def __init__(self, request):
        self.form = RegisterUserForm(request.POST)
        self.name = f'{self.form.data["first_name"]} {self.form.data["last_name"]}'
        self.user_login = self.form.data['username']
        self.email = self.form.data['email']
        self.password = self.form.data['password1']
        self.id_num = generate_random_num()
        self.user = None

    def creator(self, request):
        if len(User.objects.filter(email=self.email)) > 0:
            return HttpResponse('Пользователь с таким email уже существует')

        self.user = User.objects.create_user(id=self.id_num, username=self.user_login, email=self.email,
                                             first_name=self.form.data["first_name"],
                                             last_name=self.form.data["last_name"], password=self.password)

        user_profile = UserFile(id=self.id_num, user_name=self.name, user_login=self.user_login, email=self.email,
                                password=generate_password_hash(self.password))
        self.user.save()

        user_profile.save()
        profile = ProFile(user_id=self.user.id, user_login=self.user_login)
        profile.save()

        registration(self.user.id, self.name, self.user_login, self.email, generate_password_hash(self.password))

        login(request, self.user)
        request.session['sessionID'] = self.user.id
