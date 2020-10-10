### FORMAT
# ¯¯¯¯¯¯¯¯

format.black: ## Run black on every file
	docker-compose run --rm server bash -c "python vendor/bin/black . test/ --exclude vendor/"

format.isort: ## Sort imports
	docker-compose run --rm server bash -c "python vendor/bin/isort -rc . test/ --skip vendor/ --skip models/__init__.py"
