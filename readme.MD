



# Server (Django Rest-API)

## Requirements
*  Python 3.6
*  virtualenv python module (https://virtualenv.pypa.io/en/latest/installation/)
*  Linux or Unix based development system (Linux Recommended)

## Create a Python Virtual Environment
From the project root directory

    # virtualenv venv

## Activate Python Virtual Environment  
    # source venv/bin/activate

## Install dependencies
    # pip install -r rest-api/requirements.txt 

## Make Migrations  
From the rest-api directory

    # cd rest-api
    # python manage.py makemigrations recommender
    # python manage.py migrate

## Create Rest-API Superuser  
From the rest-api directory

    # cd rest-api
    # python manage.py createsuperuser
    # user: admin, pass: admin123$

## Run the Rest-API Server

    # python manage.py runserver
* From a web browser navigate to http://localhost:8000/admin/ and verify the Rest-API Server is running and that you can log in.
* From a web browser navigate to http://localhost:8000/api/v1/rest-auth/login/ and verify that the Rest-API Server login page endpoint shows.


# Client (VueJS Web Application)

## Requirements
*  NodeJS 
*  NPM

## Install dependencies with npm
From the client-app directory install dependencies

    # cd client-app
    # npm install

## Run Client Application

    # npm run serve

From a web browser navigate to 



#### Build the base docker image
From the root directory:  
*  Run docker build -t grayrobert/google-sheets-image-base -f docker/Dockerfile .

#### Build the development docker image from the base docker image
From the root directory:  
*  Run docker build -t grayrobert/google-sheets-image-dev -f docker/dev/Dockerfile .

#### Run the application in the docker image
For example:  
*  docker run --rm grayrobert/google-sheets-image-dev -g ResortTransferData001 -s transfer_planner_query_v4_winter.sql -t "tab"

#### Production
For the moment i'm just going to dump the image onto the nagios server and schedule in cron, but a CICD type pipeline in jenkins would be the best way forward if many changes are required.

#### Build the production docker image from the base docker image
From the root directory:    
*  docker build -t grayrobert/google-sheets-image-prod -f docker/prod/Dockerfile .

From the root directory, save docker image:  
*  docker save -o target/google-sheets-docker-prod-2018-12-06.tar grayrobert/google-sheets-image-prod:latest  
*  copy over to server (currently krusty)  
*  load the image #docker load < google-sheets-docker-prod-2018-12-06.tar  
