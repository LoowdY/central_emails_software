#realizando imports  de bibliotecas e packages necessarios
import streamlit as st
from pathlib import Path
from utils import enviar_email

# Pastas
atual_pasta = Path(__file__).parent
template_pasta = atual_pasta / 'templates'
pasta_lista_email = atual_pasta / 'lista_emails'
pasta_configuracoes = atual_pasta / 'configuracoes'

# Fluxo de controle caso não ache a página --> redirect para a home
def inicio():
    if not 'pagina_central_email'in st.session_state:
        st.session_state.pagina_central_email = 'Home'
    if not 'destinatario_atual' in st.session_state:
        st.session_state.destinatario_atual = ''
    if not 'titulo_atual' in st.session_state:
        st.session_state.titulo_atual = ''
        if not 'corpo_atual' in st.session_state:
            st.session_state.corpo_atual = ''

# Função para mudar de página (entre funções e cabeçalhos e estados)
def mudar_pagina(nome_pagina):
    st.session_state.pagina_central_email = nome_pagina

# HOME
def home():

    destinatario_atual = st.session_state.destinatario_atual
    titulo_atual = st.session_state.titulo_atual
    corpo_atual = st.session_state.corpo_atual

    st.markdown("# Central de E-mails")
    dest = st.text_input('Destinatário do E-mail:', value=destinatario_atual)
    titulo = st.text_input('Titulo do E-mail', value=titulo_atual)
    corpo_email = st.text_area('Digite o conteúdo do E-mail:',value=corpo_atual, height=260)
    col1,col2,col3 = st.columns(3)
    col1.button('Enviar E-mail',use_container_width=True, on_click=envia_email, args=(dest, titulo, corpo_email))
    col3.button('Limpar',use_container_width=True, on_click=faz_a_limpa)

    #atualizando variaveis conforme mudança do usuario para salvar estado caso o usuario mude de rota (qualquer uma?)
    st.session_state.destinatario_atual = dest
    st.session_state.titulo_atual = titulo
    st.session_state.corpo_atual = corpo_email

def faz_a_limpa():
    st.session_state.destinatario_atual = ' '
    st.session_state.titulo_atual = ' '
    st.session_state.corpo_atual = ' '
# Templates
def templates():
    st.markdown("# Templates")
    st.divider()
    for arquivo in template_pasta.glob('*.txt'):
        nome_arquivo = arquivo.stem  # Usamos o stem para remover a extensão '.txt'
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.button(nome_arquivo.upper(), key=f'{nome_arquivo}', use_container_width=True, on_click=usa_template, args=(nome_arquivo,))
        with col2:
            st.button('Editar', key=f'editar_{nome_arquivo}', use_container_width=True, on_click=editar_template, args=(nome_arquivo,))
        with col3:
            st.button('Remover', key=f'remover_{nome_arquivo}', use_container_width=True, on_click=remove_template, args=(nome_arquivo,))
    st.divider()
    st.button('Adicionar template', on_click=mudar_pagina, args=('adicionar_template',))

def usa_lista(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    arquivo_path = pasta_lista_email / nome_arquivo

    if arquivo_path.exists():
        with open(arquivo_path) as arquivo:
            texto_arquivo = arquivo.read()
        st.session_state.destinatario_atual = texto_arquivo
        mudar_pagina('Home')
    else:
        st.error(f"O arquivo {nome_arquivo} não foi encontrado na pasta {pasta_lista_email}.")
def usa_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(template_pasta / nome_arquivo) as arquivo:
        texto_arquivo = arquivo.read()
    st.session_state.corpo_atual = texto_arquivo
    mudar_pagina('Home')

def envia_email(destinatario, titulo, corpo):
    destinatario = destinatario.replace(' ','').split(',')
    email_user = le_email_usuario()
    chave_user = le_chave_usuario()

    if email_user == '':
        st.error('Adicione seu E-mail nas configurações')
    elif chave_user == '':
        st.error('Adicione sua chave de E-mail nas configurações')
    else:
        enviar_email(email_user,
                     destinatario=destinatario,
                     titulo=titulo, corpo=corpo,
                     senha_aplicativo=chave_user)

# Listas de email
def lista_emails():
    st.markdown("# Lista de E-mails")
    st.divider()

    # Verifica se a pasta existe
    if not pasta_lista_email.exists():
        st.error("A pasta de listas de e-mails não existe.")
        return

    for arquivo in pasta_lista_email.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace(' ', '_').lower()
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.button(nome_arquivo.upper(), key=f'{nome_arquivo}', use_container_width=True, on_click=usa_lista,
                      args=(nome_arquivo,))
        with col2:
            st.button('Editar', key=f'editar_{nome_arquivo}', use_container_width=True, on_click=editar_lista_email,
                      args=(nome_arquivo,))
        with col3:
            st.button('Remover', key=f'remover_{nome_arquivo}', use_container_width=True, on_click=remove_lista_email,
                      args=(nome_arquivo,))
    st.divider()
    st.button('Adicionar Lista', on_click=mudar_pagina, args=('adicionar_nova_lista',))

# Adicionar nova lista de e-mails
def adicionar_lista(nome_lista='', emails_lista=''):
    st.markdown("# Adicionar nova lista")
    nome_lista = st.text_input("Nome da lista:", value=nome_lista)
    emails_lista = st.text_area("Escreva os E-mails separados por vírgula:", value=emails_lista, height=500)
    st.button('Salvar Lista', on_click=salvar_lista, args=(nome_lista, emails_lista))

# Função para salvar lista de e-mails
def salvar_lista(nome, emails):
    pasta_lista_email.mkdir(exist_ok=True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_lista_email / nome_arquivo, 'w') as arquivo:
        arquivo.write(emails)
    mudar_pagina('lista_emails')

# Configurações de e-mails
def configuracao():
    st.markdown("# Configuração")

# Função para adicionar novo template
def add_template(nome_template='', texto_template=''):
    st.markdown("# Adicionar Novo Template")
    nome_template = st.text_input("Nome do Template", value=nome_template)
    texto_template = st.text_area("Conteúdo do Template", value=texto_template, height=500)
    st.button('Salvar Template', on_click=salvar_template, args=(nome_template, texto_template))

# Função para salvar templates
def salvar_template(nome, texto):
    template_pasta.mkdir(exist_ok=True)
    # Padroniza o nome do arquivo para garantir a consistência
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    arquivo_path = template_pasta / nome_arquivo

    # Checa se o arquivo já existe para decidir entre editar ou criar um novo
    if arquivo_path.exists():
        with open(arquivo_path, 'w') as arquivo:  # Abre o arquivo existente para escrita
            arquivo.write(texto)
    else:
        with open(arquivo_path, 'w') as arquivo:  # Cria um novo arquivo
            arquivo.write(texto)
    mudar_pagina('Templates')

# Função para remover arquivo de lista de e-mails
def remove_lista_email(nome):
    nome_arquivo = nome.lower() + '.txt'  # Garante que o nome do arquivo seja tratado de forma consistente
    arquivo_path = pasta_lista_email / nome_arquivo
    if arquivo_path.exists():
        arquivo_path.unlink()
    else:
        st.error("Arquivo de lista de e-mails não encontrado.")

# Função para editar lista de e-mails
def editar_lista_email(nome):
    nome_arquivo = nome.lower() + '.txt'
    with open(pasta_lista_email / nome_arquivo) as arquivo:
        texto_arquivo = arquivo.read()
        st.session_state.nome_lista_editar = nome
        st.session_state.texto_lista_editar = texto_arquivo
        mudar_pagina('editar_lista')

# Função para editar arquivo de template de e-mail
def editar_template(nome):
    nome_arquivo = nome.lower() + '.txt'
    arquivo_path = template_pasta / nome_arquivo
    if arquivo_path.exists():
        with open(arquivo_path) as arquivo:
            texto_arquivo = arquivo.read()
        st.session_state.nome_template_editar = nome
        st.session_state.texto_template_editar = texto_arquivo
        mudar_pagina('editar_template')
    else:
        st.error("O arquivo do template não foi encontrado.")

# Função para remover template
def remove_template(nome):
    nome_arquivo = nome.lower() + '.txt'  # Consistência na nomenclatura do arquivo
    arquivo_path = template_pasta / nome_arquivo
    if arquivo_path.exists():
        arquivo_path.unlink()
    else:
        st.error("Arquivo de template não encontrado.")

# Função principal
def main():

    #invocando função de incialização
    inicio()
    # Botões da lateral esquerda da página
    st.sidebar.button('Central de E-mail', on_click=mudar_pagina, args=('Home',), use_container_width=True)
    st.sidebar.button('Templates', on_click=mudar_pagina, args=('Templates',), use_container_width=True)
    st.sidebar.button('Lista de E-mail', on_click=mudar_pagina, args=('lista_emails',), use_container_width=True)
    st.sidebar.button('Configuração', on_click=mudar_pagina, args=('config',), use_container_width=True)

    # Sessões com as funções criadas para cada "estado"
    if st.session_state.pagina_central_email == 'Home':
        home()

    elif st.session_state.pagina_central_email == 'Templates':
        templates()

    elif st.session_state.pagina_central_email == 'adicionar_template':
        add_template()

    elif st.session_state.pagina_central_email == 'lista_emails':
        lista_emails()

    elif st.session_state.pagina_central_email == 'editar_template':
        nome_template_editar = st.session_state.nome_template_editar
        texto_template_editar = st.session_state.texto_template_editar
        add_template(nome_template_editar, texto_template_editar)

    elif st.session_state.pagina_central_email == 'adicionar_nova_lista':
        adicionar_lista()

    elif st.session_state.pagina_central_email == 'editar_lista':
        nome_lista_editar = st.session_state.nome_lista_editar
        texto_lista_editar = st.session_state.texto_lista_editar
        adicionar_lista(nome_lista_editar, texto_lista_editar)

    elif st.session_state.pagina_central_email == 'config':
        configuracao()

#pagina de configuracao
def configuracao():
    st.markdown('#  Configurações')
    email = st.text_input('Digite o seu E-mail:')
    st.button('Salvar', key='salvar_email', on_click=email_salvar, args=(email,))
    chave = st.text_input('Digite sua chave:')
    st.button('Salvar', key='salvar_chave', on_click=chave_salvar, args=(chave,))

#funcao para salvar o email nas configurações
def email_salvar(email):
    pasta_configuracoes.mkdir(exist_ok=True)
    with open(pasta_configuracoes / 'email_usuario.txt', 'w') as arquivo:
        arquivo.write(email)


def le_email_usuario():
    pasta_configuracoes.mkdir(exist_ok=True)
    if (pasta_configuracoes / 'email_usuario.txt').exists():
        with open(pasta_configuracoes / 'email_usuario.txt', 'r') as arquivo:
            return arquivo.read()
    return ''

def le_chave_usuario():
    pasta_configuracoes.mkdir(exist_ok=True)
    if (pasta_configuracoes / 'chave_usuario.txt').exists():
        with open(pasta_configuracoes / 'chave_usuario.txt', 'r') as arquivo:
            return arquivo.read()
    return ''

#funcao para salvar chave do email (gmail)
def chave_salvar(chave):
    pasta_configuracoes.mkdir(exist_ok=True)
    with open(pasta_configuracoes / 'chave_usuario.txt', 'w') as arquivo:
        arquivo.write(chave)

# Bloco de execução do código
if __name__ == "__main__":
    main()