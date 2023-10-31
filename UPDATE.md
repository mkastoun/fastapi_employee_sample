# Toubib API - Code Challenge Update

The app now have a new structure working with Postgres


## Using Docker
prerequisites
* docker installed
```commandline
docker-compose up --build
```

This command will do the following:
* Install dependencies
* Run the DB migrations
* Run the test

To re-run the test please follow these steps:

#### 1. Go to the docker container
```commandline
docker-compose exec app bash
```

#### 2. Run the tests
```commandline
poetry run pytest
```

## Without docker
prerequisites
* python 3.10
* Poetry
* Postgres DB (if you don't have it, and you want to use partial docker run this command: docker run --name toubib-pg -d -e POSTGRESQL_PASSWORD=toubibPass123 -p 5432:5432 bitnami/postgresql:13)

### 1. Prepare DB
If you already have a postgres DB then you should do the following:
* Create 2 databases, name them `toubibdb` and `toubibdb_test`
* Set owner to these username `toubib`

### 2. Prepare APP
* Copy the .env.example to .env
* Update .env DB strings with your db credentials, and host

### 3. Run the migrations
```commandline
poetry run alembic upgrade head
```

### 4. Run the tests
```commandline
poetry run pytest
```

### 5. Start the toubib app
```commandline
uvicorn app.main:app --reload
```

## Test using postman
On the root level there is a [Postman Collection](Dialogue_test.postman_collection.json) imported to your postman,
and start making calls, with different scenarios.

## API Docs
Access http://localhost:8000/docs to check the api documentation
