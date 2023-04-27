## Containerizing
- build docker image with `docker build -t resurety-hw .` from top level directory
  - Verify docker daemon is running beforehand!
- Start docker container with `docker run --rm -it -p 5001:5001/tcp resurety-hw:latest`; wait for console output giving debugger pin
- Send API requests to `localhost:5001`
## Running tests locally
- make sure you're in the top level directory `resurety-homework` and you have the venv activated
  - Create venv via `python -m venv venv`
  - Activate venv via source `venv/Scripts/activate on windows`, source `venv/bin/activate` on unix
  - install dependencies via `pip install -r requirements.txt`
- run `python -m pytest .`
## Running tests in container
- Not implemented! I would be happy to work on this given further guidance.