.PHONY: all

all: migrations import run

migrations:
	@alembic upgrade head
	@migration completed

import:
	@python fixtures/import_fixtures.py
	@echo manga imported
	

run:
	@echo running bot
	@python bot.py
	