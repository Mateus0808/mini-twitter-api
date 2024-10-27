# Nome da Aplicação
Mini Twitter

## Descrição

Esta aplicação é uma API desenvolvida em Django usando Django REST Framework. Ela permite: ["gerenciar postagens, timeline, seguir usuários, etc."].

## Tecnologias Utilizadas

- Django
- Django REST Framework
- PostgreSQL
- Redis (para cache)
- Docker

## Requisitos

Antes de começar, você precisa ter instalado em sua máquina:

- Python 3.12
- pip (gerenciador de pacotes do Python)
- PostgreSQL
- Redis
- Docker e Docker Compose

## Configuração

### Passo 1: Clone o Repositório

Clone o repositório em sua máquina local:
```bash
git clone https://github.com/Mateus0808/mini-twitter-api.git
cd mini-twitter-api
```


### Usando Docker
First of all, let's run the database:
```bash
docker-compose up -d db
```

Build the Django app:
```bash
docker compose build
```

Run the Django app
```bash 
docker compose up -d
```

Migrando o Banco de Dados
Depois que os contêineres estiverem rodando, você pode executar as migrações do banco de dados. Em um novo terminal, execute:

```bash
docker-compose exec djangoapp python manage.py migrate
```

## Acessar a Aplicação
A aplicação estará disponível em ```http://localhost:8000/```.


