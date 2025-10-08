# Database migration commands
new_migration:
	@if [ -z "$(title)" ]; then \
	  echo "Usage: make new_migration title=\"Your migration title\""; \
	  exit 1; \
	fi
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic revision --autogenerate -m '$(title)'"

upgrade:
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic upgrade head"

downgrade:
	@if [ -z "$(revision)" ]; then \
	  echo "Usage: make downgrade revision=<revision_id>"; \
	  exit 1; \
	fi
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic downgrade $(revision)"

current:
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic current"

history:
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic history"

show:
	@if [ -z "$(revision)" ]; then \
	  echo "Usage: make show revision=<revision_id>"; \
	  exit 1; \
	fi
	@docker compose exec server bash -c "cd /app/source && /app/.venv/bin/alembic show $(revision)"

# Docker commands
destroy:
	@docker compose down --volumes

up:
	@docker compose up -d

restart:
	@make destroy
	@make up

logs:
	@docker compose logs -f server

# Database commands
db_shell:
	@docker compose exec database psql -U admin -d fromScratchAPI

# Help command
help:
	@echo "Available commands:"
	@echo "  new_migration title=\"title\"     - Create new auto-generated migration"
	@echo "  upgrade                          - Apply all pending migrations"
	@echo "  downgrade revision=<id>          - Downgrade to specific revision"
	@echo "  current                          - Show current migration"
	@echo "  history                          - Show migration history"
	@echo "  show revision=<id>               - Show specific migration"
	@echo "  destroy                          - Stop and remove containers with volumes"
	@echo "  up                               - Start containers in background"
	@echo "  restart                          - Restart containers (destroy + up)"
	@echo "  logs                             - Show server logs"
	@echo "  db_shell                         - Connect to database shell"
	@echo "  help                             - Show this help message"
