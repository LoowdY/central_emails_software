# Sistema de Gestão de E-mails

Este projeto é uma aplicação baseada em Streamlit para gerenciar modelos e listas de e-mails, permitindo aos usuários enviar e-mails, gerenciar modelos e configurar as definições de e-mail. A aplicação é projetada para funcionar com o Gmail para envio de e-mails.

## Funcionalidades

- **Página Inicial**: Enviar e-mails especificando o destinatário, assunto e corpo do e-mail.
- **Modelos**: Criar, editar e gerenciar modelos de e-mail.
- **Listas de E-mail**: Criar, editar e gerenciar listas de endereços de e-mail.
- **Configurações**: Configurar e salvar seu endereço de e-mail e chave de aplicativo para o Gmail.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seuusuario/central_emails_software.git
    cd central_emails_software
    ```

2. Instale os pacotes necessários:
    ```bash
    pip install streamlit
    ```

## Uso

1. Execute a aplicação Streamlit:
    ```bash
    streamlit run emails.py
    ```

2. Abra a aplicação no seu navegador. Você verá uma barra lateral com botões de navegação:
    - **Central de E-mail**: Página principal para compor e enviar e-mails.
    - **Modelos**: Gerenciar modelos de e-mail.
    - **Lista de E-mail**: Gerenciar listas de endereços de e-mail.
    - **Configuração**: Configurar suas definições de e-mail.

3. Use as diversas funcionalidades conforme necessário:
    - **Compor e enviar e-mails** na página Central de E-mail.
    - **Criar, editar ou remover modelos** na página Modelos.
    - **Criar, editar ou remover listas de e-mails** na página Lista de E-mail.
    - **Configurar seu e-mail e chave de aplicativo** na página Configuração.

## Explicação do Código

### `emails.py`

O script principal para a aplicação Streamlit:

- **Importações**: Importar as bibliotecas e módulos necessários.
    ```python
    import streamlit as st
    from pathlib import Path
    from utils import enviar_email
    ```

- **Caminhos dos Diretórios**: Definir caminhos para modelos, listas de e-mails e configurações.
    ```python
    atual_pasta = Path(__file__).parent
    template_pasta = atual_pasta / 'templates'
    pasta_lista_email = atual_pasta / 'lista_emails'
    pasta_configuracoes = atual_pasta / 'configuracoes'
    ```

- **Inicialização do Estado da Sessão**: Inicializar variáveis de estado da sessão.
    ```python
    def inicio():
        if not 'pagina_central_email' in st.session_state:
            st.session_state.pagina_central_email = 'Home'
        if not 'destinatario_atual' in st.session_state:
            st.session_state.destinatario_atual = ''
        if not 'titulo_atual' in st.session_state:
            st.session_state.titulo_atual = ''
        if not 'corpo_atual' in st.session_state:
            st.session_state.corpo_atual = ''
    ```

- **Navegação de Páginas**: Funções para mudar de páginas.
    ```python
    def mudar_pagina(nome_pagina):
        st.session_state.pagina_central_email = nome_pagina
    ```

- **Página Inicial**: Função para lidar com a Página Inicial.
    ```python
    def home():
        # Código para a página inicial
    ```

- **Modelos de E-mail**: Funções para gerenciar modelos de e-mail.
    ```python
    def templates():
        # Código para gerenciar modelos
    ```

- **Listas de E-mail**: Funções para gerenciar listas de e-mails.
    ```python
    def lista_emails():
        # Código para gerenciar listas de e-mails
    ```

- **Configuração**: Funções para gerenciar configurações de e-mail.
    ```python
    def configuracao():
        # Código para gerenciar configurações
    ```

- **Função Principal**: O ponto de entrada principal da aplicação.
    ```python
    def main():
        inicio()
        # Código para lidar com a navegação e renderização de páginas
    ```

### `utils.py`  

```python

import ssl
import smtplib
from email.message import EmailMessage

#rdga slmm ojns ztum

def enviar_email(usuario_email, destinatario, titulo, corpo, senha_aplicativo):
    mensagem = EmailMessage()
    mensagem['From'] = usuario_email
    mensagem['To'] = destinatario
    mensagem['Subject'] = titulo
    mensagem.set_content(corpo)
    safe = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as smtp:
        smtp.login(usuario_email, senha_aplicativo)
        smtp.sendmail(usuario_email, destinatario,mensagem.as_string())
 ```

