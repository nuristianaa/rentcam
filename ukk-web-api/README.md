# Backend Project Mgt with FastAPI

## Python Virtual Env
pip install virtualenv
virtualenv .venv
Mac/Linux:  source .venv/bin/activate
Win: .\.venv\Scripts\activate
allow permission in windows: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

## Requirements.txt
Install
- pip install -r requirements.txt

## Setting ENV
- cp env.copy .env
- cp alembic/env.copy alembic/.env
- ./runlink.sh

## Run server
- cd apps - ['identity', 'rental']
- python src/main.py

## Migrations & Seeding
cd alembic
alembic upgrade head
cd apps - ['identity', 'rental']
python src/seed.py

## Project Dependencies
- schema
  - table
    - model     : Column dan model database module terkait
    - repo      : Berisi query dan function2 terkait data, sebagai jembatan antara route dan model
    - route     : Endpoint atau url
    - schema    : Base struktur / json data dari untuk request & response api
- utils: berisi config atau utilisasi dari project
  - database    : Config connection database
  - exceptions  : Handle / helper terkait kode dan message error HTTP
  - hash        : Helper untuk encrypt dan decrypt password
- main.py

* schema dan table disesuaikan dengan database postgre agar rapi penamaannya. contoh di postgre table user ada di schema auth, jadi folderingnya auth.user