# -*- coding: utf-8 -*-

response.controller = 'Categorias'

@auth.requires_login()
def index():
    return redirect(URL('listar'))

@auth.requires_login()
def listar():
    response.funcionalidade = 'Listagem'
    titulo = 'Listagem de Categorias'
    categorias = db(db.categoria).select()
    msg = "Exibindo {} resultado(s)".format(len(categorias))
    return dict(titulo=titulo, categorias=categorias, msg_paginacao=msg)

@auth.requires_login()
def inserir():
    response.funcionalidade = 'Inserir'
    titulo = 'Nova Categoria'
    form = SQLFORM(db.categoria, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Categoria #%s cadastrada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    response.funcionalidade = 'Editar'
    titulo = 'Editar Categoria'
    categoria = db.categoria(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.categoria, categoria, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Categoria #%s atualizada com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form, titulo=titulo)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.categoria.id==id).delete():
        session.flash = 'Categoria #%s excluída com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Categoria não existente!'
    redirect(URL('listar'))
