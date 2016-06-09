# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.sistema, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Sistema #%s cadastrado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    sistema = db.sistema(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.sistema, sistema, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Sistema #%s atualizado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.sistema.id==id).delete():
        session.flash = 'Sistema #%s excluído com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Sistema não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.sistema, user_signature=False)
    return locals()
