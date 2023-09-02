.PHONY: build

build:
	docker compose build
	@echo ""
	@echo "You can now start your containers with \`make start\`"

start:
	docker compose up -d
	@echo ""
	@echo "You can now enter your Django container with \`make sh\`"

stop:
	docker compose down

restart: stop start

sh:
	@if [ -z "$$(docker compose ps -q web)" ]; then \
		echo "Your containers aren't running." >&2;  \
		echo "" >&2;  \
		echo "Run \`make start\` to start your containers." >&2;  \
		echo "" >&2;  \
		exit 1; \
	fi
	@echo ""
	@echo "You can run your development server with \`djrun\`"
	@echo ""
	@echo "Several bash aliases exist in this container such as:"
	@echo "  - \`dj\` - \`./manage.py\`"
	@echo "  - \`djtest\` - \`./manage.py test --settings=htmx_demo.settings.test -v=2\`"
	@echo "  - \`djtestkeepdb\` - \`./manage.py test --settings=htmx_demo.settings.test -v=2 --keepdb\`"
	@echo ""
	docker compose exec web bash

test:
	docker compose exec web python3 manage.py test --settings=htmx_demo.settings.test -v=2

test-keepdb:
	docker compose exec web python3 manage.py test --settings=htmx_demo.settings.test -v=2 --keepdb

bump-deps:
	docker compose run --rm --no-deps web poetry up --latest
	docker compose run --rm --no-deps web pre-commit autoupdate

rename:
	@# Check if PROJECT_NAME is defined
	@if [ -z "$$PROJECT_NAME" ]; then \
		echo ""; \
		echo "Usage:"; \
		echo "    make rename PROJECT_NAME=my_project_name_with_underscores"; \
		echo ""; \
		exit 1; \
	fi

	@# Get a version of PROJECT_NAME but with dashes instead of underscores
	$(eval PROJECT_NAME_KEBAB := $(subst _,-,$(PROJECT_NAME)))

	@echo ""
	@echo "This Makefile target will:"
	@echo "1.) Replace all instances of the following in files and folders:"
	@echo "  - \`htmx_demo\` with \`$(PROJECT_NAME)\`"
	@echo "  - \`htmx-demo\` with \`$(PROJECT_NAME_KEBAB)\`"
	@echo ""
	@echo "Proceeding in 10 seconds..."
	@echo ""

	@sleep 10

	@# Rename the htmx_demo directory
	mv htmx_demo $(PROJECT_NAME)

	@# Replace all instances of htmx_demo with PROJECT_NAME
	grep -rl htmx_demo . | xargs perl -i -pe "s/htmx_demo/$(PROJECT_NAME)/g"

	@# Replace all instances of htmx-demo with PROJECT_NAME_KEBAB
	grep -rl htmx-demo . | xargs perl -i -pe "s/htmx-demo/$(PROJECT_NAME_KEBAB)/g"

	@# Reset git index
	rm .git/index
	git reset

	@echo ""
	@echo "Done!"
