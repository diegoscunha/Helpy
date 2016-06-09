# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.situacao, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Situação #%s cadastrada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    situacao = db.situacao(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.situacao, situacao, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Situação #%s atualizada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.situacao.id==id).delete():
        session.flash = 'Situação #%s excluída com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Situação não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.situacao, user_signature=False)
    return locals()
