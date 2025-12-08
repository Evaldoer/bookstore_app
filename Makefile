.PHONY: help
help:  ## Mostra ajuda
	@echo "Comandos disponíveis:"
	@echo "  run              - Subir containers"
	@echo "  stop             - Derrubar containers"
	@echo "  migrate          - Aplicar migrações"
	@echo "  createsuperuser  - Criar superusuário"
	@echo "  collectstatic    - Coletar arquivos estáticos"
	@echo "  logs-web         - Ver logs do serviço web"
	@echo "  logs-db          - Ver logs do serviço db"
	@echo "  test             - Rodar testes"
	@echo "  check            - Rodar linters"
	@echo "  format           - Formatar código"
	@echo "  format-py        - Formatar código Python"
	@echo "  install          - Instalar dependências"

.PHONY: install
install:  ## Instala dependências do projeto
	poetry install

RUN_PYPKG_BIN = poetry run

.PHONY: format
format:  ## Formata código Python
	$(RUN_PYPKG_BIN) black .
	$(RUN_PYPKG_BIN) isort .

.PHONY: format-py
format-py:  ## Alias para formatar código Python
	$(RUN_PYPKG_BIN) black .
	$(RUN_PYPKG_BIN) isort .

.PHONY: run
run:
	docker compose up

.PHONY: stop
stop:
	docker compose down

.PHONY: migrate
migrate:
	docker compose exec web python manage.py migrate --noinput

.PHONY: createsuperuser
createsuperuser:
	docker compose exec web python manage.py createsuperuser

.PHONY: collectstatic
collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

.PHONY: logs-web
logs-web:
	docker compose logs -f web

.PHONY: logs-db
logs-db:
	docker compose logs -f db

.PHONY: test
test:
	$(RUN_PYPKG_BIN) pytest tests/*.py

.PHONY: check
check:
	$(RUN_PYPKG_BIN) flake8 .
	$(RUN_PYPKG_BIN) black --check --line-length 118 --fast .
	$(RUN_PYPKG_BIN) mypy $(LIBRARY_DIRS)
