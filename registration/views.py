from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authorization.models import ProFile
from services.forms import RegisterUserForm
from services.registration import registration
from django.contrib.auth import login
from werkzeug.security import generate_password_hash
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
        form = RegisterUserForm(request.POST)
        if request.method == 'POST':
            name = f'{form.data["first_name"]} {form.data["last_name"]}'
            user_login = form.data['username']
            email = form.data['email']
            password = form.data['password1']
            id_num = generate_random_num()
            user = User.objects.create_user(id=id_num, username=user_login, email=email,
                                            first_name=form.data["first_name"],
                                            last_name=form.data["last_name"], password=password)
            userfile = UserFile(id=id_num, user_name=name, user_login=user_login, email=email,
                                password=generate_password_hash(password))
            user.save()
            user_id = user.id
            userfile.save()
            profile = ProFile(user_id=user_id, user_login=user_login)
            profile.save()

            registration(user_id, name, user_login, email, generate_password_hash(password))
            login(request, user)
            request.session['sessionID'] = user.id

            return redirect(f'http://localhost:8000/users/{user_id}')

        return render(request, 'reg.html', {'form': RegisterUserForm})
