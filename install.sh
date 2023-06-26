#!/bin/bash

echo "\n\n### Welcome to the Movie Genre Classification....### \n\n"

echo "-> Set the virtual env....\n\n"

# # Set the name and location for the virtual environment
ENV_NAME="movie_genre_classification"

# Create the virtual environment
python3 -m venv "${ENV_NAME}"

# # Activate the virtual environment
source "${ENV_NAME}/bin/activate"

# echo 'Install Libraries....'
pip3 install -r ./requirements.txt

# # Output a success message
echo "Done! Virtual environment '${ENV_NAME}' created and activated....\n\n"

echo "->Start Docker containers for setting up API on LocalHost using Flask..\n\n"
docker-compose up -d

echo "Done! API Created \n"
#python predict.py

echo "-> Run the Unit tests to check the API"
python -m unittest test.py

echo "Checked! Test Passed...\n\n"

echo "-> Run the curl request from the terminal..\n" 

curl -d '{"overview":"A movie about penguins in Antarctica building a spaceship to go to Mars."}' -H "Content-Type: application/json" -X POST http://localhost:8000

echo "Success...!! \n\n"

echo "\n->Stop Docker containers ..\n\n"
docker-compose down

echo "-\n>Delete the local env.\n\n"
rm -r "${ENV_NAME}"
