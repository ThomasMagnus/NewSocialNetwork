from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.models import User

from services.forms import UserAuthForm, AuthUserForm
import logging

module_logger = logging.getLogger('ex.authorization')


class LoginUser(LoginView):
    template_name = 'auth.html'
    form_class = AuthUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        form = UserAuthForm(request.POST)

        try:
            if request.session['sessionID']:
                print(request.session['sessionID'])
                return redirect(to=f"http://localhost:8000/users/{request.session['sessionID']}")
        except Exception as ex:
            module_logger.exception(ex)

        if request.method == 'POST':
            email = form.data['email']
            password = form.data['password']

            try:
                user = User.objects.get(email=email)
                user_id = user.id

                if user.check_password(raw_password=password):
                    login(request, user)
                    request.session['sessionID'] = user.id
                    return redirect(f'http://localhost:8000/users/{user_id}')
                else:
                    return HttpResponse('Неверно указан логин или пароль')
            except Exception as ex:
                module_logger.exception(ex)
                return HttpResponse('Неверно указан логин или пароль')

        return render(request, 'auth.html', {'form': form})
