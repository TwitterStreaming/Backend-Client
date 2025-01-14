.PHONY: help
help: ## Print info about all commands
	@echo "Commands:"
	@echo
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[01;32m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: ## Initialize venv
	@rm -rf venv
	@python3 -m venv venv

.PHONY: install
install: ## Initialize and install all dependencies
	@pip install django django-cors-headers elasticsearch python-dotenv

.PHONY: install
run: ## Run the project
	python3 elasticSeachConsumer.py
