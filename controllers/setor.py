# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.setor, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Setor #%s cadastrado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    setor = db.setor(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.setor, setor, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Setor #%s atualizado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.setor.id==id).delete():
        session.flash = 'Setor #%s excluído com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Setor não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.setor, user_signature=False)
    return locals()
