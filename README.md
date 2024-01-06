# LinkMinify
LinkMinify: URL Shortening Service Overview LinkMinify is a simple yet powerful URL shortening service. It allows users to create short aliases for long URLs, making them easier to share and manage. The service is built using the FastAPI framework and stores data in a PostgreSQL database.

## Project's structure

```text
├── admin   ············· administration part
├── alembic ············· alembic's data, what were generated during init, but can be updated
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions ········· generated migrations by alembic
├── api ················· Api endpoints
├── dao ················· BaseDao for CRUD
├── db
│  ├── models ··········· db's models
│  ├── base.py ·········· base config for db models
│  └── session.py ······· params for connection to db
├── schemas ············· Types for request response
│  ├── base.py
│  ├── links.py
│  └── users.py
├── services
│  ├── users.py ········· users logic
│  ├── utils.py ········· generate short url logic
│  ├── utils.py ········· generate short url logic
│  ├── validators.py ···· user and url validators
│  └── links.py ········· short and full url logic
├── templates ··········· Templates for admin and swagger pages
├── tests ··············· Pytest
├── utils
│  └── auth.py ·········  Authentication logic
├── .gitignore ·········· Files and directories to ignore when committing changes
├── alembic.ini ········· Alembic's config
├── createuser.py ······· Script for adding new superuser
│── docker-compose.yaml · Compose configuration
│── Dockerfile ·······    Docker Setup
├── exceptions ·········· Handle Exceptions
├── main.py ············· Main code for starting app
├── messages.py ········· Errors and success messages for responses
├── permissions.py ······ Logic for admin permissions
├── README.md ··········· You're here
├── requirements.txt ···· Dependencies
├── run.sh ·············· Script fur db upgrade and run
├── settings.py ········· App settings

```

## Local deployment

## RUN PROJECT

```shell
docker compose up
```

## Alembic

**Create migration**:

```shell
alembic revision --autogenerate -m "Comment"
```

*Recommendation*: use '{000}_comment' format for comments.

**Migrate to last**:

```shell
alembic upgrade head
```

## Superuser adding

Use `createuser.py` for adding  superuser in table.

/admin for admin page

# Link Minify Service API Documentation

## API Endpoints

### 1. Create a Short Link

#### Endpoint
`POST /create-short-link`

#### Description
This endpoint accepts a full URL and returns a shortened version of it.

#### Input
- `full_url` (string): The full URL to be shortened.

#### Response
- `short_url` (string): The shortened URL.
.
  

### 2. Delete a Link

#### Endpoint
`DELETE /delete-link/{short_url}`

#### Description
This endpoint deletes a previously generated short link.

#### Input
- `short_url` (path parameter): The short URL to be deleted.

#### Response
A message indicating the operation's success status.


### 3. Redirect to Full URL

#### Endpoint
`GET /redirect/{short_url}`

#### Description
This endpoint handles the redirection from a short URL to the original full URL. When accessed, it redirects the client to the full URL associated with the provided short URL.

#### Input
- `short_url` (path parameter): The short URL for which the full URL redirection is desired.

#### Response
Redirects the client to the full original URL.
