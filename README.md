# Flask Market

## Objetivo

Desenvolver um sistema web para gerenciar usuários e produtos utilizando Flask

## Tecnologias Utilizadas

- **Frontend**
    - **HTML, CSS, JavaScript**: Tecnologias utilizadas para o desenvolvimento da interface do usuário.
    - **Jinja2**: Template engine para renderização de templates no Flask.
    - **Bootstrap 5**: Framework de estilo para layout responsivo e design moderno.


- **Backend**
    - **Flask**: Framework web utilizado para construir a aplicação.
    - **Flask-Login**: Extensão para gerenciar sessões de usuários e autenticação.
    - **Flask-Bcrypt**: Para hashing de senhas.
    - **Flask-JWT-Extended**: Suporte para autenticação baseada em tokens JWT.
    - **Flask-SQLAlchemy**: Extensão do Flask para facilitar a integração com bancos de dados SQL.
    - **Flask-Migrate**: Ferramenta para gerenciamento de migrações de banco de dados.
    - **gunicorn**: Servidor WSGI para executar a aplicação Flask em produção.


- **Análise e Visualização de Dados**
    - **pandas**: Para manipulação e análise de dados.
    - **plotly**: Para a visualização de dados e gráficos.


- **Serialização e Validação**
    - **marshmallow** e **marshmallow-sqlalchemy**: Para serialização e validação de dados.

## Rotas Disponíveis

- **Usuário**
    - `/user/login`: Rota para login de usuários
    - `/user/register`: Rota para cadastro de novos usuários
    - `/user/logout`: Rota para encerrar a sessão atual


- **Produto**
    - `/product/list`: Rota para listar todos os produtos
    - `/product/register`: Rota para cadastrar novos produtos


- **Vendas**
    - `/sales/chart`: Rota para visualizar o gráfico de vendas


- **API**
    - `/api/dashboard`: Rota para gerar um token de autenticação JWT
    - `/api/docs`: Rota com documentação de endpoints disponíveis
    - `/api//token`: Rota API para geração de token de autenticação JWT com base nas credenciais do usuário
    - `/api/products`: Rota API para Listar todos os produtos, Inserir produto, buscar produto por nome ou ID
    - `/api/users`: Rota API para todos os usuários

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
