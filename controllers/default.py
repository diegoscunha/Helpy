# -*- coding: utf-8 -*-

def index():
    if auth.is_logged_in():
        redirect(URL('dashboard', 'index'))
    form_login=auth.login()
    if form_login.errors:
        pass
    form_login.element(_name='username').update(_class='form-control', _placeholder='Usuário')
    form_login.element(_name='password').update(_class='form-control', _placeholder='Senha')
    form_login.element(_type='submit').update(_class='btn btn-primary btn-block btn-flat', _value='Entrar')
    return dict(form_login=form_login)

def esqueci_senha():
    pass
