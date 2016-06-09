# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('listar'))

@auth.requires_login()
def inserir():
    form = SQLFORM(db.cliente, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Cliente #%s cadastrado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def editar():
    cliente = db.cliente(request.args(0)) or redirect(URL('listar'))
    form = SQLFORM(db.cliente, cliente, submit_button='Salvar')
    if form.process().accepted:
        session.flash = 'Cliente #%s atualizado com sucesso!' %(form.vars.id)
        redirect(URL('listar'))
    elif form.errors:
         response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def excluir():
    id = request.args(0)
    if db(db.cliente.id==id).delete():
        session.flash = 'Cliente #%s excluído com suscesso!' %(id)
    else:
        session.flash = 'Não foi possível excluir. Cliente não existente!'
    redirect(URL('listar'))

@auth.requires_login()
def listar():
    grid = SQLFORM.grid(db.cliente, user_signature=False)
    return locals()

# implementar na view componente de seleção de varios sistemas
@auth.requires_login()
def cliente_sistemas():
    cliente = db.cliente(request.args(0)) or redirect(URL('listar'))
    db.cliente_sistema.cliente_id.default = cliente.id
    db.cliente_sistema.cliente_id.writable = False
    db.cliente_sistema.sistema_id.requires = IS_IN_DB(db, db.sistema, '%(nome)s - %(versao)s', zero='.: Selecione :.')
    form = SQLFORM(db.cliente_sistema, submit_button='Salvar')
    form.vars.cliente_id = cliente.id
    try:
        if form.process(onvalidation=valida_sistema).accepted:
            response.flash = 'Sistema #%s adicionado ao cliente com sucesso!' %(db.sistema(form.vars.sistema_id).nome)
        elif form.errors:
            response.flash = 'Erros no formulário!'
    except Exception as ex:
        response.flash = 'Erro inesperado!'
    grid = SQLFORM.grid((db.cliente_sistema.cliente_id==cliente.id), field_id=db.cliente_sistema.cliente_id, user_signature=False)
    return dict(form=form, grid=grid)

# Verificar se o codigo de ativação é gerado ja nesse formulario ou é calculado depois
@auth.requires_login()
def liberar_sistemas():
    cliente = db.cliente(request.args(0)) or redirect(URL('listar'))
    db.liberacao_sistema.cliente_id.default = cliente.id
    db.liberacao_sistema.cliente_id.writable = False
    db.liberacao_sistema.responsavel_id.default = auth.user_id
    db.liberacao_sistema.responsavel_id.writable = False
    db.liberacao_sistema.solicitante_id.requires = IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s - %(username)s', zero='.: Selecione :.')
    db.liberacao_sistema.sistema_id.requires = IS_IN_DB(db, db.sistema, '%(nome)s - %(versao)s', zero='.: Selecione :.')
    form = SQLFORM(db.liberacao_sistema, submit_button='Salvar')
    if form.process().accepted:
        response.flash = ''
    elif form.errors:
        response.flash = ''
    grid = SQLFORM.grid((db.liberacao_sistema.cliente_id==cliente.id), user_signature=False)
    return dict(form=form, grid=grid)

# validar se o sistema já está vinculado ao cliente
def valida_sistema(form):
    cliente_id = form.vars.cliente_id
    sistema_id = form.vars.sistema_id
    if not db((db.cliente_sistema.cliente_id==cliente_id) & (db.cliente_sistema.sistema_id==sistema_id)).isempty():
        form.errors.sistema_id = 'Cliente já possui o sistema cadastrado!'

# metodo para teste
def exibir_cliente_sistemas():
    return dict(form=db((db.cliente_sistema.cliente_id==1) & (db.cliente_sistema.sistema_id==4)).isempty())
