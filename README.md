## Containerizing
- build docker image with `docker build -t resurety-hw .`
- Start docker container with `docker run --rm -it -p 5001:5001/tcp resurety-hw:latest`; wait for console output giving debugger pin
- Send API requests to `localhost:5001`
## Running tests locally
- make sure you're in the top level directory `resurety-homework` and you have the venv activated
- run `python -m pytest .`
## Running tests in container
- Not implemented! I would be happy to work on this given further guidance.