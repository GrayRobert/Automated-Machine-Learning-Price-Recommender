# Requirements  
*  Python 3.6
*  virtualenv python module (https://virtualenv.pypa.io/en/latest/installation/)
*  Linux or Unix based development system (Linux Recommended)

# Create a Python Virtual Environment
From the project root directory
 
    # virtualenv venv

# Activate Python Virtual Environment  
    # source venv/bin/activate

# Install dependencies


# Run the API
cd to src directory
python manage.py runserver

# Database ORM
Django has some object relational model features so we can persist our models into a database with schemas

## Generate the schemas
python manage.py makemigrations recommender

## Persist the schemas
python manage.py migrate





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
