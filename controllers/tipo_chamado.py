# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.tipo_chamado, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Tipo de chamado #%s cadastrada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    tipo_chamado = db.tipo_chamado(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.tipo_chamado, tipo_chamado, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Tipo de chamado #%s atualizada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.tipo_chamado.id==id).delete():
        session.flash = 'Tipo de chamado #%s excluída com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Tipo de contato não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.tipo_chamado, user_signature=False)
    return locals()
