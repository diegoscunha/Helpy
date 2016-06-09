# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.auth_user, user_signature=False)
    return locals()

@auth.requires_login()
def inserir():
    db.auth_user.cliente_id.requires = IS_IN_DB(db, db.cliente, '%(nome_fantasia)s', zero='.: Selecione :.')
    form = SQLFORM(db.auth_user, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Usuário #%s cadastrado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    usuario = db.auth_user(request.args(0)) or redirect(URL('listar'))
    db.auth_user.cliente_id.requires = IS_IN_DB(db, db.cliente, '%(nome_fantasia)s', zero='.: Selecione :.')
    form = SQLFORM(db.auth_user, usuario, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Usuário #%s cadastrado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

#implementar na view componente de seleção de varios setores
@auth.requires_login()
def usuario_setor():
    usuario = db.auth_user(request.args(0)) or redirect(URL('listar'))
    db.usuario_setor.usuario_id.default = usuario.id
    db.usuario_setor.usuario_id.writable = False
    db.usuario_setor.setor_id.requires = IS_IN_DB(db, db.setor, '%(nome)s', zero='.: Selecione :.')
    form = SQLFORM(db.usuario_setor, submit_button='Salvar')
    form.vars.usuario_id = usuario.id
    try:
        if form.process(onvalidation=valida_setor).accepted:
            response.flash = 'Setor #%s adicionado ao usuário com sucesso!' %(db.setor(form.vars.setor_id).nome)
        elif form.errors:
            response.flash = 'Erros no formulário!'
    except Exception as ex:
        response.flash = 'Erro inesperado!'
    grid = SQLFORM.grid((db.usuario_setor.usuario_id==usuario.id), field_id=db.usuario_setor.usuario_id, user_signature=False)
    return dict(form=form, grid=grid)

# validar se o setor já está vinculado ao usuario
def valida_setor(form):
    usuario_id = form.vars.usuario_id
    setor_id = form.vars.setor_id
    if not db((db.usuario_setor.usuario_id==usuario_id) & (db.usuario_setor.setor_id==setor_id)).isempty():
        form.errors.setor_id = 'Usuário já possui o setor cadastrado!'
