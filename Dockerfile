# Base com Python 3.12
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH" \
    PYSETUP_PATH="/opt/pysetup"

# Instalar dependências do sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl build-essential libpq-dev gcc \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version \
    && apt-get purge --auto-remove -y build-essential curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração do Poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Instalar dependências principais direto no sistema (sem virtualenv)
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar código do projeto
WORKDIR /app
COPY . .

# Expor porta do Django
EXPOSE 8000

# Comando padrão (dev)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
