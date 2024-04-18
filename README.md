# Projeto de Gerenciamento de Associações de Comunidades do Rio de Janeiro

Este projeto consiste em uma aplicação para gerenciamento de cadastros e formulários de associações de moradores, com um backend em Flask e frontend HTML, CSS e JavaScript.

## Funcionalidades

- Criação, consulta e exclusão de cadastros de associações.
- Adição de formulários vinculados a cada associação.
- Interface de usuário simples para interações com a API.

## Pré-requisitos

### Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas

- Git
- Python (versão 3.8 ou superior)
- Node.js (versão 14 ou superior)

## Tecnologias Utilizadas

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Swagger para documentação da API

## Configuração e Execução

### Backend

- Clone o repositório para sua máquina local:

bash
git clone https://github.com/Luciahelenasantos/Sistema-Cadastro-Comunidades-RJ.git
cd Sistema-Cadastro-Comunidades-RJ

- Navegue até a pasta do backend:

bash
cd backend

- Instale as dependências usando pip:

bash
pip install -r requirements.txt

- Execute a aplicação:

bash
python app.py

### Frontend

- Navegue até a pasta do frontend:

bash
cd frontend

- Se ainda não tiver, instale o Node.js e o pacote http-server globalmente:

bash
npm install -g http-server

- Inicie o servidor com suporte a CORS:

bash
http-server -c-1 --cors

A interface do usuário estará disponível em http://localhost:8080/cadastros.html.

### Documentação da API

Acesse a documentação da API via Swagger em http://localhost:5000/apidocs.
