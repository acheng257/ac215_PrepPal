# API Service

## Backend API Container

Build with FastAPI framework

### Go into the api-service folder

- Open a terminal and go to `src/apiservice`

### Build & Run Container

- Run `sh docker-shell.sh`

### Start API Service

- To run development API service run `uvicorn api.service:app --host 0.0.0.0 --port 9000` from the docker shell
- Test the API service by going to `http://localhost:9000/`
