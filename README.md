# Movie Genre Classification Service

This service uses machine learning to predict the genre of a movie based on its overview. It provides an API that accepts a movie overview and returns the predicted genre.

## Prerequisites

Python 3

## Getting Started
These instructions will guide on how to set up and run the movie genre classification service.

1. Download the Dataset
Download the dataset from Kaggle using the following link: The Movies Dataset. Extract the file movies_metadata.csv from the downloaded zip file and save in data folder.

2. Set Up the Environment
Install the required Python packages by running the following command.
`pip3 install -r ./requirements.txt`

3. Preprocess the Data and Train the Model using the Notebook(Movie_Genre_Classification_Assignment.ipynb) 
    * Run the commant `jupyter notebook` on the terminal window.   
    * Load the dataset into a pandas DataFrame.
    * Preprocess the data by selecting relevant columns and cleaning the overview text.
    * Split the data into training and testing sets.
    * Choose a machine learning algorithm for text classification, such as Naive Bayes, Support Vector Machines (SVM), or Random Forests.
    * Train the model on the preprocessed data.
    * Save the Model in the model folder

4. Run the Service Locally  on the terminal
Start the Flask application by running the following command `python app.py`:
The service should now be running on http://localhost:8000.

5. Test the API using the below curl 
Use a tool like curl to send a POST request to the API endpoint:

```curl -d '{"overview":"A movie about penguins in Antarctica building a spaceship to go to Mars."}' -H "Content-Type: application/json" -X POST http://localhost:8000```

The response should contain the predicted genre in JSON format.