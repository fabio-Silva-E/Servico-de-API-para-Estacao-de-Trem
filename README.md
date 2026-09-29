# Serviço de API para Estação de Trem

API REST para gerenciamento de estações, rotas, trens, viagens e pedidos de passagem, construída com Django + Django REST Framework.

## Tecnologias

- Python 3
- Django 6.1
- Django REST Framework
- PostgreSQL
- JWT (djangorestframework-simplejwt)
- drf-spectacular (documentação da API)

## Pré-requisitos

- Python 3.11+ instalado
- PostgreSQL instalado e rodando
- Git

## Como rodar o projeto localmente

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Servico-de-API-para-Estacao-de-Trem
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados PostgreSQL

Crie um banco de dados local (via `psql`, pgAdmin ou similar) com o nome que você definirá no `.env`.

### 5. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

> ⚠️ O `.env` contém dados sensíveis e não deve ser commitado no Git.

### 6. Rodar as migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Criar um superusuário (para acessar o admin)

```bash
python manage.py createsuperuser
```

### 8. Rodar o servidor

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

## Endpoints principais

### Autenticação (`/api/user/`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/user/register/` | Criar novo usuário |
| POST | `/api/user/token/` | Obter token JWT (login) |
| POST | `/api/user/token/refresh/` | Renovar token |
| POST | `/api/user/token/verify/` | Verificar validade do token |
| GET/PUT/PATCH | `/api/user/me/` | Ver/editar o próprio perfil |

### Estação de trem (`/api/train/`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET/POST | `/api/train/stations/` | Listar/criar estações |
| GET/POST | `/api/train/routes/` | Listar/criar rotas |
| GET/POST | `/api/train/crew/` | Listar/criar tripulação |
| GET/POST | `/api/train/train-types/` | Listar/criar tipos de trem |
| GET/POST | `/api/train/trains/` | Listar/criar trens |
| GET/POST | `/api/train/journeys/` | Listar/criar viagens |
| GET/POST | `/api/train/orders/` | Listar/criar pedidos de passagem |

Todos os endpoints de `/api/train/` exigem autenticação (token JWT no header `Authorization: Bearer <token>`).

### Admin

Painel administrativo disponível em `http://127.0.0.1:8000/admin/` (requer superusuário).

## Rodando os testes

```bash
python manage.py test
```
