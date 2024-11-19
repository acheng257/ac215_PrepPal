# Testing Dockerfile with Container Structure Tests

This test ensures that the Dockerfile is correctly configured, including environment variables, user permissions, installed tools, and the expected functionality of the container.

## Steps to Test the Dockerfile
Make sure you are in the folder `apiservice`: `cd ac215_preppal/src/apiservice`

### 1. Build the Docker Image
Run the following command to build the Docker image: `docker build -t test-api-image -f Dockerfile .`

### 2. Install Container Structure Tests (MacOS/Linux)
- Install the container-structure-test tool via brew: `brew install container-structure-test`
- Download the container-structure-test:

    #### OS X
    `curl -LO https://storage.googleapis.com/container-structure-test/latest/container-structure-test-darwin-amd64 && chmod +x container-structure-test-darwin-amd64 && sudo mv container-structure-test-darwin-amd64 /usr/local/bin/container-structure-test`

    #### Linux
    `curl -LO https://storage.googleapis.com/container-structure-test/latest/container-structure-test-linux-amd64 && chmod +x container-structure-test-linux-amd64 && sudo mv container-structure-test-linux-amd64 /usr/local/bin/container-structure-test`

- Note: You only need to run these commands once

### 3. Run the Tests
Execute the following command to test the Dockerfile: `container-structure-test test --image test-api-image --config tests/docker_test.yml`

### 4. Delete the test-api-image
`docker image rm test-api-image`


## Expected Output
If all tests pass, the output will look like this:

======================================== <br>
====== Test file: docker_test.yml ====== <br>
======================================== <br>
=== RUN: Verify Python binary <br>
--- PASS <br>
=== RUN: Check pip version <br>
--- PASS <br>
=== RUN: Check git installed <br>
--- PASS <br>
... <br>
=== RUN: Check current working directory is /app <br>
--- PASS <br>

========================================= <br>
================ RESULTS ================ <br>
========================================= <br>
Passes:      13 <br>
Failures:    0 <br>
Duration:    Xs <br>
Total tests: 13 <br>

PASS
