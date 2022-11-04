# Address Book CRUD API
## Features
With this API;
- You can create, view, update, and delete address
## Tech stack
Tools used during the development of this API are:
- [Python3](https://www.python.org) - Programming language
- [FastAPI](https://fastapi.tiangolo.com) - FastAPI is a modern, fast (high-performance), web framework for building APIs
#### Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/addressbook/api/v1/'` | Create new address
GET | `/addressbook/api/v1/'` | Get all the available addresses
GET | `/addressbook/api/v1/{id}` | Get address by id
PUT | `/addressbook/api/v1/{id}` | Update address by id
DELETE | `/addressbook/api/v1/{id}` | Delete address by id
POST | `/addressbook/api/v1/'` | Retrieve the addresses that are within a given distance and location coordinates.
### Usage 
Git clone this repo to your PC

    $ git clone https://github.com/bkalyankumar/addressbook-minimal-fastapi.git
    $ cd addressbook-minimal-fastapi
Create a virtual environment

    $ python3 -m venv venv && source .venv/bin/activate
Install dependancies

    $ pip install -r requirements.txt
### Launching the app
    $ uvicorn main:app --reload
### Open your browser and enter the below url to open Swagger UI
    $ http://127.0.0.1:8000/docs
