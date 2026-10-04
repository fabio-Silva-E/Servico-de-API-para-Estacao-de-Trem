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

### Permissões

As permissões ficam em `train/permissions.py` (`IsAdminOrIfAuthenticatedReadOnly`):

| Recurso | Operações disponíveis | Quem pode |
|---------|-----------------------|-----------|
| Estações, tripulação, tipos de trem | listar e criar | leitura: usuário autenticado; criação: staff |
| Rotas, trens | listar, detalhar e criar | leitura: usuário autenticado; criação: staff |
| Viagens | CRUD completo | leitura: usuário autenticado; escrita: staff |
| Pedidos | listar, detalhar e criar | usuário autenticado (vê apenas os próprios pedidos) |

A listagem de pedidos é paginada (10 por página, máximo de 100) com `?page=` e `?page_size=`.

> O limite de requisições (throttling) está em `REST_FRAMEWORK` > `DEFAULT_THROTTLE_RATES` no `settings.py`. O padrão é restritivo (10/dia para anônimos e 30/dia para usuários autenticados); ajuste para desenvolvimento, por exemplo `"anon": "100/hour", "user": "1000/hour"`.

## Interface web (templates)

Além da API, o projeto tem telas em HTML na pasta `templates/`, separadas por funcionalidade. As páginas são estáticas e consomem a API com JavaScript (`fetch`), autenticando com o JWT guardado no `localStorage`. O token de acesso é renovado automaticamente pelo endpoint de refresh.

```
templates/
├── base.html              # layout comum (CSS básico, navbar e scripts)
├── home.html
├── partials/
│   ├── _navbar.html       # menu de navegação
│   └── _api.html          # JavaScript compartilhado (api(), login, formulários)
├── user/        login.html, register.html, profile.html
├── stations/    list.html
├── routes/      list.html
├── crew/        list.html
├── train_types/ list.html
├── trains/      list.html
├── journeys/    list.html, detail.html
└── orders/      list.html
```

### Páginas disponíveis

| URL | Template | Descrição |
|-----|----------|-----------|
| `/` | `home.html` | Página inicial |
| `/login/` | `user/login.html` | Login |
| `/register/` | `user/register.html` | Cadastro |
| `/profile/` | `user/profile.html` | Editar e-mail e senha |
| `/stations/` | `stations/list.html` | Estações |
| `/routes/` | `routes/list.html` | Rotas |
| `/crew/` | `crew/list.html` | Tripulação |
| `/train-types/` | `train_types/list.html` | Tipos de trem |
| `/trains/` | `trains/list.html` | Trens |
| `/journeys/` | `journeys/list.html` | Viagens |
| `/journeys/detail/?id=<id>` | `journeys/detail.html` | Detalhes de uma viagem |
| `/orders/` | `orders/list.html` | Meus pedidos e criação de pedido com vários tickets |

Os formulários de criação (estações, rotas, tripulação, tipos de trem, trens e viagens) só aparecem para usuários staff.

### Configuração necessária

1. No `train_service/settings.py`, o `TEMPLATES` deve apontar para a pasta:

```python
'DIRS': [BASE_DIR / 'templates'],
```

2. No `train_service/urls.py`, importe `TemplateView` e registre as páginas dentro de `urlpatterns`:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ... rotas existentes (admin, api/user, api/train, debug toolbar)
    path("", TemplateView.as_view(template_name="home.html")),
    path("login/", TemplateView.as_view(template_name="user/login.html")),
    path("register/", TemplateView.as_view(template_name="user/register.html")),
    path("profile/", TemplateView.as_view(template_name="user/profile.html")),
    path("stations/", TemplateView.as_view(template_name="stations/list.html")),
    path("routes/", TemplateView.as_view(template_name="routes/list.html")),
    path("crew/", TemplateView.as_view(template_name="crew/list.html")),
    path("train-types/", TemplateView.as_view(template_name="train_types/list.html")),
    path("trains/", TemplateView.as_view(template_name="trains/list.html")),
    path("journeys/", TemplateView.as_view(template_name="journeys/list.html")),
    path("journeys/detail/", TemplateView.as_view(template_name="journeys/detail.html")),
    path("orders/", TemplateView.as_view(template_name="orders/list.html")),
]
```

Depois acesse `http://127.0.0.1:8000/login/`. Para ver os formulários de criação, entre com um usuário staff (por exemplo, o superusuário criado com `createsuperuser`).

### Admin

Painel administrativo disponível em `http://127.0.0.1:8000/admin/` (requer superusuário).


