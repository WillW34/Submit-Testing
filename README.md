# Submit-Testing
A server to use to test submit plugins.

# Install
## Using docker
Run `docker run --publish 3001:5000 --detach --name submit-testing synbiohub/submit-testing:snapshot`
Check it is up using localhost:3001.

## Using Python
Run `pip install -r requirements.txt` to install the requirements. Then run `FLASK_APP=app python -m flask run`. A flask module will run at localhost:5000/.
