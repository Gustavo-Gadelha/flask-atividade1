# Atividade 1 de Web Flask

## Objetivo

Desenvolver um sistema web para gerenciar usuários e produtos utilizando Flask.

## Tecnologias Utilizadas

- HTML, CSS, JavaScript
- Bootstrap 5 (Framework de Estilo)
- Flask (Framework Web)
- Jinja2 (Template Engine para Flask)
- PostgreSQL (Banco de Dados)

## Módulos do Sistema

1. **Login**
2. **Cadastro de Usuário**
3. **Cadastro de Produto**

## Regras de Negócio

- Existem dois tipos de usuários: **super** e **normal**.
    - O usuário **super** pode cadastrar quantos produtos desejar.
    - O usuário **normal** pode cadastrar até 3 produtos.


- **Tabela user_account**
    - `id`: Inteiro
    - `login`: String
    - `password`: String
    - `type`: String (`super` ou `normal`)


- **Tabela product**
    - `id`: Inteiro
    - `name`: String
    - `quantity`: Inteiro (Deve ser igual ou maior que 0)
    - `price`: Decimal (Deve ser igual ou maior que 0)
    - `user_id`: String (Referência ao usuário que cadastrou o produto)

## Considerações

Use sua criatividade para interpretar e desenvolver as necessidades adicionais que o sistema possa ter.

Data de entrega: 17 de set.