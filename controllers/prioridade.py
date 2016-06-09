# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.prioridade, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Prioridade #%s cadastrada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    prioridade = db.prioridade(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.prioridade, prioridade, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Prioridade #%s atualizada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.prioridade.id==id).delete():
        session.flash = 'Prioridade #%s excluída com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Prioridade não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.prioridade, user_signature=False)
    return locals()
