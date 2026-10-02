# Eden

## Run with Docker Compose

Copy `example.env` to `.env` and set `POSTGRES_PASSWORD` and
`CHAT__SECRET_KEY` to your own values. If you already have a `.env`, add the
`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` settings from the example.
Use a URL-safe database password (for example, a random hexadecimal string),
because Compose includes it in the database connection URL.

```sh
docker compose up --build -d
```

The app is available at `http://localhost:8000` (API documentation at `/docs`).
Set `APP_PORT` in `.env` to change the host port. Both services join the explicitly
defined `eden` bridge network. PostgreSQL is reachable as `database:5432` within
the network, and its data is stored in the `postgres_data` volume.

Compose builds the app, waits for PostgreSQL to be healthy, and runs
`alembic upgrade head` before starting Uvicorn. The container's database URL is
derived from the `POSTGRES_*` settings and overrides `CORE__DATABASE_DSN` in `.env`.

```sh
docker compose logs -f app
docker compose down
```

`docker compose down` preserves the database volume. Adding `--volumes` deletes
the database data.

## Database migrations

Alembic configuration is in `alembic.ini`, and all migrations live in the root
`migrations/` directory. The initial revision creates the tables defined by the
SQLAlchemy models.

After changing the models, generate a migration against a running development
database using the project source mounted into a temporary app container:

```sh
docker compose run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/migrations:/app/migrations" \
  -v "$PWD/src:/app/src:ro" \
  app alembic revision --autogenerate -m "describe the schema change"
```

Review the generated migration before applying it:

```sh
docker compose run --rm app alembic upgrade head
```

Rebuild the image after creating migrations so they are included in deployments.
For local Alembic commands, run `uv sync`, set `CORE__DATABASE_DSN` to a reachable
PostgreSQL URL with the `postgresql+asyncpg` driver, and use
`uv run alembic upgrade head` or `uv run alembic revision --autogenerate -m "..."`.
Local migration commands only require the database setting.
