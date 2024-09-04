# Atividade 1 de Web Flask

## Objetivo

Desenvolver um sistema web para gerenciar usuários e produtos utilizando Flask.

## Tecnologias Utilizadas

- HTML, CSS, JavaScript
- Flask (Framework Web)
- PostgreSQL (Banco de Dados)

## Módulos do Sistema

1. **Login**
2. **Cadastro de Usuário**
3. **Cadastro de Produto**

## Regras de Negócio

- Existem dois tipos de usuários: **super** e **normal**.
    - O usuário **super** pode cadastrar quantos produtos desejar.
    - O usuário **normal** pode cadastrar até 3 produtos.


- **Tabela Usuário**
    - `loginUser`: String
    - `senha`: String
    - `tipoUser`: String (`super` ou `normal`)


- **Tabela Produtos**
    - `id`: Inteiro
    - `nome`: String
    - `loginUser`: String (Referência ao usuário que cadastrou o produto)
    - `qtde`: Inteiro (Quantidade)
    - `preço`: Decimal (Preço do produto)

## Considerações

Use sua criatividade para interpretar e desenvolver as necessidades adicionais que o sistema possa ter.

Data de entrega: 17 de set.