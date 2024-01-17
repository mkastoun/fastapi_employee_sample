# Employee management sample

The app built with FASTAPI and Postgres

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
* Postgres DB (if you don't have it, and you want to use partial docker run this command: docker run --name sample-pg -d -e POSTGRESQL_PASSWORD=samplePass123 -p 5432:5432 bitnami/postgresql:13)

### 1. Prepare DB
If you already have a postgres DB then you should do the following:
* Create 2 databases, name them `sample_project` and `sample_project`
* Set owner to these username `sampleMaster`

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

### 5. Start the sample app
```commandline
uvicorn app.main:app --reload
```

## Test using postman
On the root level there is a [Postman Collection](employee_test.postman_collection.json) imported to your postman,
and start making calls, with different scenarios.

## API Docs
Access http://localhost:8000/docs to check the api documentation


## 1. Create patient record

`POST /v1/patients` with request body (all fields are required, email is unique per
patient):

```json
{
    "email": "hanna@hannouch.com",
    "first_name": "hanna",
    "last_name": "Hannouch",
    "date_of_birth": "1993-09-05",
    "sex_at_birth": "FEMALE"
}

```

Returns:

```json
{
    "data": {
        "id": 1,
        "email": "hanna@hannouch.com",
        "first_name": "hanna",
        "last_name": "Hannouch",
        "date_of_birth": "1993-09-05",
        "sex_at_birth": "FEMALE"
    }
}
```

## 2. Getting a patient record

`GET /v1/patients/1` returns:

```json
{
    "data": {
        "id": 1,
         "email": "hanna@hannouch.com",
        "first_name": "hanna",
        "last_name": "Hannouch",
        "date_of_birth": "1993-09-05",
        "sex_at_birth": "FEMALE"
    }
}
```

## 3. List patient records alphabetically by last name and by pages of 10 records at a time

`GET /v1/patients?offset=40&limit=10` returns:

```json
{
    "data": [
        {
            "id": 17,
            "email": "hanna1@hannouch.com",
            "first_name": "hanna",
            "last_name": "Hannouch",
            "date_of_birth": "1993-09-05",
            "sex_at_birth": "FEMALE"
        },
        {
            "id": 21,
            "email": "hanna@hannouch.com",
            "first_name": "hanna",
            "last_name": "Hannouch",
            "date_of_birth": "1993-09-05",
            "sex_at_birth": "FEMALE"
        }
    ],
    "meta": {
        "offset": 40,
        "total_items": 42,
        "total_pages": 5,
        "page_number": 5
    }
}
```

## Quickstart


You'll need python 3.10 and [poetry](https://python-poetry.org/).
OR, you can use docker. A `Makefile` with all usefull commands is provided.
