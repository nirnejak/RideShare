# RideShare

Application for RideShare



## What is RideShare?

A web application to help people share ride. User can register with their contact number.
After logging into the application users can share their ride. With the details of time, source, destination. Other users can look for other available rides in their location. Interested users can send requests. The creator of ride can view and accept the ride request. After that contact of the other user will be displayed to the interested user.
In this way people can contact and share rides.

### Version
2.0

## Installation and Usage

### Clone
Clone the Project

```sh
$ git clone https://github.com/nirnejak/RideShare.git
$ cd RideShare
```

### Installation

Install the dependencies (flask, passlib, flask-wtf, gunicorn, psycopg2)
pipenv is required for the installation.

```sh
$ pip install pipenv
$ pipenv install
```

### Run

This will start flask server and at http://localhost:7070/

```sh
$ python app.py
```
