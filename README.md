# fromScratch-API

This is a pretty basic API implementation using `FastAPI` and `Postgres` and `SqlAlchemy` for ORM. The project is containerized using `Docker` and should be pretty easy to set up and run locally for development purposes.

# How to run 
To spin up the server you should be fine running the command from the `Makefile`

`make build_and_up` (which runs `docker compose up -d --build`)

This spins up the server locally and you should be able to see the endpoint
documentation on `localhost:8000/docs`

### For development
This project uses `uv` as package manager so to further develop you would need to have it installed and run `uv sync` to get the packages and your virtual environment ready. 

### Run the tests
`make test_all` should have all the tests running.
`make test test_file={path to the test_*.py}` should run a specific test (the path should be relative to the /tests folder *see make command implementation*)

**example*: `make test test_file=services/test_customer_service.py` runs the customer service tests.

The make file indicates how to perform other actions too like migration,displaying the default server logs, "down"-ing the containers etc.

## Disclaimers
For the sake of simplicity some assumptions and simplifications were used

1. The postgres server credentials are hardcoded in the docker compose file
which is of course extremely wrong for a production aspiring project. Normally we would have secrets like .env and json files that we would 
be stored somewhere (for example in a cloud bucket storage) and with the 
right credentials we would pull them locally to work with. This project was inspired by previous works that did exactly that so the set up for this
is there but the true implementation was considered redundant for this specific exercise

2. Use of `Session` over `AsyncSession`. Normally for a production ready 
API project that communicates in an ORM manner with `SqlAlchemy` we would prefer to use `AsyncSession` over `Session` because the first is suited for concurrency thus taking into account scalability concerns.

3. Lack of complete test coverage. Some basic tests were written to showcase the need for tests (actually helped me debug stuff) using the behavior driven approach. Of course more tests that explore many more aspects of the app would be included normally for a production ready implementation (more use cases, correct error handling and responses etc)
but again those were omitted for simplicity purposes.

4. Use of `uv` package manager in the setup. Could go for the good ol `pip`
but decided that it would be a good opportunity to try using `uv` for the project's set up. Normally you should not have any problems with it because it is containerized but in case that happens let me know to provide you with a simpler `pip` version.


5. The server does not have an independent logger which can be generally useful
