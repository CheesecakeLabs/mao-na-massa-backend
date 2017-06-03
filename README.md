# Mão na Massa

## Running locally
1. `virtualenv venv -ppython3`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. `hug -f server.py -c create_db_tables`
1. `hug -f server.py`

## Exposing the server to the world
1. npm install -g localtunnel
2. lt --port 8000
