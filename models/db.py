# -*- coding: utf-8 -*-
# Alterar nomeclatura dos models garantindo que seja executados na ordem correta
# Criar um arquivo especifico para criar os validadores dos campos
# Criar arquivo de mensagens utilizadas na aplicação
db = DAL('sqlite://helpy3.db')

# TABLE situacao - crud - OK
db.define_table('situacao',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Situações', format='%(nome)s')

# TABLE categoria - crud - OK
db.define_table('categoria',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Categorias', format='%(nome)s')

# TABLE prioridade - crud - OK
db.define_table('prioridade',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Prioridades', format='%(nome)s')

# TABLE tipo_avaliacao - crud - OK
db.define_table('tipo_avaliacao',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Tipos de Avaliações', format='%(nome)s')

# TABLE tipo_contrato - crud - OK
db.define_table('tipo_contato',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Tipos de Contatos', format = '%(nome)s')

# TABLE tipo_chamado - crud - OK
db.define_table('tipo_chamado',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'), singular='Tipos de Chamados', format='%(nome)s')

# TABLE sistema - crud - OK
db.define_table('sistema',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'),
                Field('descricao', type='text', length=500, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(500, error_message='Informe no maxímo 500 caracteres!')], notnull=True, label='Descrição'),
                Field('imagem', type='upload', required=False, requires=IS_EMPTY_OR(IS_IMAGE(extensions=('jpeg', 'png'), maxsize=(200, 200))), notnull=False, label='Imagem'),
                Field('versao', type='string', length=20, required=False, requires=None, notnull=False, label='Versão'), singular='Sistemas', format='%(nome)s - %(versao)s')

# TABLE cliente - crud - OK
db.define_table('cliente',
                Field('razao_social', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Razão Social'),
                Field('nome_fantasia', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome Fantasia'),
                Field('cnpj', length=20, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(20, error_message='Informe no maxímo 20 caracteres!')], notnull=True, label='Cnpj'),
                Field('email_contato', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!'), IS_EMAIL(error_message='E-mail inválido!')], notnull=True, label='E-mail'),
                Field('is_ativo', required=True, requires=IS_IN_SET(['sim', 'não']), widget=SQLFORM.widgets.radio.widget, label='Cliente ativo?'),
                Field('telefone', length=14, requires=IS_LENGTH(14, error_message='Informe no maxímo 60 caracteres!'), label='Telefone'),
                Field('is_atende', required=True, requires=IS_IN_SET(['sim', 'não']), widget=SQLFORM.widgets.radio.widget, label='Atende chamados?'), singular='Clientes', format='%(nome_fantasia)s')

# TABLE setor - crud - OK
db.define_table('setor',
                Field('nome', type='string', length=60, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(60, error_message='Informe no maxímo 60 caracteres!')], notnull=True, label='Nome'),
                Field('cliente_id', 'reference cliente', label='Cliente'), singular='Setores', format='%(nome)s')

# TABLE cliente_sistema - OK
db.define_table('cliente_sistema',
                Field('cliente_id', 'reference cliente', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Cliente'),
                Field('sistema_id', 'reference sistema', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Sistema'),
                Field('is_ativo', required=True, notnull=True, requires=[IS_IN_SET(['sim', 'não']), IS_NOT_EMPTY('Campo obrigatório!')], widget=SQLFORM.widgets.radio.widget, label='Sistema ativo?'), primarykey= ['cliente_id', 'sistema_id'])

# Componente Auth
from gluon.tools import Auth
auth = Auth(db)

auth.settings.extra_fields['auth_user']= [
  Field('is_admin', required=True, notnull=True, requires=[IS_IN_SET(['sim', 'não']), IS_NOT_EMPTY('Campo obrigatório!')], widget=SQLFORM.widgets.radio.widget, label='É administrador?'),
  Field('is_atendente', required=True, notnull=True, requires=[IS_IN_SET(['sim', 'não']), IS_NOT_EMPTY('Campo obrigatório!')], widget=SQLFORM.widgets.radio.widget, label='Atende chamados?'),
  Field('cliente_id', 'reference cliente', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Cliente'),
  Field('telefone', length=14, requires=IS_LENGTH(14, error_message='Informe no maxímo 14 caracteres!'), label='Telefone')]
auth.define_tables(username=True)

# verificar primary key da tabela
# TABLE liberacao_sistema - OK
db.define_table('liberacao_sistema',
                Field('cliente_id', 'reference cliente', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Cliente'),
                Field('solicitante_id', 'reference auth_user', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Solicitante'),
                Field('sistema_id', 'reference sistema', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Sistema'),
                Field('responsavel_id', 'reference auth_user', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Responsável'),
                Field('codigo_ativacao', type='string', length=45, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(minsize=45, maxsize=45, error_message='O código deve possuir 45 caracteres!')], notnull=True, label='Codigo de ativação'),
                Field('codigo_liberacao', type='string', length=45, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(minsize=45, maxsize=45, error_message='O código deve possuir 45 caracteres!')], notnull=True, label='Codigo de liberação'),
                Field('data', type='datetime', notnull=True, label='Data', default=request.now),
                Field('dias_liberado', type='integer', length=3, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(3, error_message='Informe no maxímo 3 caracteres!')], notnull=True, label='Dias liberação'))
db.liberacao_sistema.data.writable = db.liberacao_sistema.data.readable = False

# TABLE usuario_setor
db.define_table('usuario_setor',
                Field('usuario_id', 'reference auth_user', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Usuário'),
                Field('setor_id', 'reference setor', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Setor'))

# TABLE chamado
db.define_table('chamado',
                Field('responsavel_id', 'reference auth_user', required=True, label='Responsável'),
                Field('solicitante_id', 'reference auth_user', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Solicitante'),
                Field('tipo_contato_id', 'reference tipo_contato', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Tipo de contato'),
                Field('tipo_chamado', 'reference tipo_chamado', label='Tipo de chamado'),
                Field('sistema_id', 'reference sistema', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Sistema'),
                Field('assunto', type='string', length=100, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(100, error_message='Informe no maxímo 100 caracteres!')], notnull=True, label='Assunto'),
                Field('descricao', type='text', length=500, required=True, requires=[IS_NOT_EMPTY('Campo obrigatório!'), IS_LENGTH(500, error_message='Informe no maxímo 500 caracteres!')], notnull=True, label='Descrição'),
                Field('data_abertura', type='datetime', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Data de abertura'),
                Field('data_conclusao', type='datetime', label='Data de conclusão'),
                Field('situacao_id', 'reference situacao', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Situação'),
                Field('prioridade_id', 'reference prioridade', label='Prioridade'),
                Field('categoria_id', 'reference categoria', label='Categoria'),
                Field('setor_id', 'reference setor', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Setor'),
                Field('visualizado', type='boolean', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, default=False, label='Visualizado'), format='Chamado #%(id)s - %(assunto)s')

# TABLE anexo
db.define_table('anexo',
               Field('diretorio', type='upload', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!'), notnull=True, label='Anexo'),
               Field('chamado_id', 'reference chamado', required=True, requires=IS_NOT_EMPTY('Campo obrigatório!')), format='Chamado #%(chamado_id)s - %(diretorio)s')

# TABLE historico_chamado
db.define_table('historico_chamado',
               Field('chamado_id', 'reference chamado', required=True, notnull=True, label='Chamado'),
               Field('responsavel_id', 'reference auth_user', notnull=True, label='Responsável'),
               Field('situacao_id', 'reference situacao', required=True, notnull=True, label='Situação'),
               Field('prioridade_id', 'reference prioridade', notnull=True, label='Prioridade'),
               Field('categoria_id', 'reference categoria', notnull=True, label='Categoria'),
               Field('data', required=True, notnull=True, label='Data histórico'),
               Field('comentario', required=True, notnull=True, label='Comentário'), format='Chamado #%(chamado_id) - %(comentario) - data: %(data)s')

# TABLE avaliacao_chamado
db.define_table('avaliacao_chamado',
               Field('obs', label='Observação'),
               Field('chamado_id', 'reference chamado', required=True, notnull=True, label='Chamado'),
               Field('tipo_avaliacao_id', 'reference tipo_avaliacao', required=True, label='Tipo de avaliação'))

#auth.settings.actions_disabled = ['register'] # desabilita a ação de registrar usuários
#auth.settings.registration_requires_verification = True # requer a confirmação do registro por e-mail
#auth.settings.login_after_registration = True # faz o login do usuário após o registro
#auth.settings.login_url = URL('user', args='login') # url de login
auth.settings.login_url = URL('index', args='login')
#auth.settings.login_next = URL('index') # página de redirecionamento após o login
auth.settings.login_next = URL('dashboard', 'index') # página de redirecionamento após o login
auth.settings.logout_next = URL('dafault', 'index')
#auth.settings.expiration = 3600  # tempo até que a sessão do usuário expire, em segundos
#auth.messages.submit_button = 'Entrar'
auth.settings.hideerror = True

db.auth_user.password.comment = 'Diegite a senha'
auth.messages.invalid_login = 'Login ou senha inválidos'
auth.messages.invalid_user = 'Usuário inválido'
auth.messages.is_empty = "campo obrigatório"
auth.messages.mismatched_password = "campos de senha devem ser iguais"
