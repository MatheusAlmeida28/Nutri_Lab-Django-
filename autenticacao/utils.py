import re
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def password_is_valid(request, password, confirm_password):
    if (len(password.strip()) == 0):
        messages.add_message(request, constants.WARNING, 'senha em branco')
        return False
    
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False

    elif not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False
    
    elif not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    elif not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    elif not re.search('[0-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    return True

def username_is_valid(request, username):
    if (len(username.strip()) == 0):
        messages.add_message(request, constants.WARNING, 'Nome do usuário em branco')
        return False

    if len(username) <= 0:
        messages.add_message(request, constants.WARNING, 'Coloque o nome do seu usuário')
        return False

    if User.objects.filter(username = username).exists():
        messages.add_message(request, constants.ERROR, 'Usuário já cadastrado')
        return False
    
    
    return True

def email_is_valid(request, email):
    if (len(email.strip()) == 0):
        messages.add_message(request, constants.WARNING, 'Nome de email em branco')
        return False

    if len(email) <= 0:
        messages.add_message(request, constants.WARNING, 'Digite um email')
        return False

    elif User.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'O email digitado já foi usado')
        return False

    
    return True

def user_success(request):
    messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')


def sistema_erro(request):
    messages.add_message(request, constants.ERROR, 'Erro interno do Sistema')


def user_is_not_valid(request):
    messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
