# htmx-demo

## Getting started

Build your environment.

```bash
make build
```

Run your environment.

```bash
make start
```

Open an interactive shell into the Docker container that contains the Django project.

```bash
make sh
```

Run all migrations.

```bash
# inside `make sh`
dj migrate
```

Create a superuser to use with the demo.

```bash
# inside `make sh`
dj createsuperuser
```

Seed your project with a list of products.

```bash
# inside `make sh`
dj shell_plus
```

```python
# inside the Django shell
from htmx_demo.core.factories import ProductFactory
ProductFactory.create_batch(50, variants=["Small", "Medium", "Large"])
```

Start your dev server.

```bash
djrun
```

Visit https://localhost:8000/ to view the demo.

---

Most the files relevant to the demo can be found in the `htmx_demo.core` Django app.

Static files which are just the small amount of CSS I wrote and the minified HTMX JS can be found in `htmx_demo/staticfiles`.

The base template and a login template can be found in `htmx_demo/templates`.
