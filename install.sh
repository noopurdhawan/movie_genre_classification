echo 'Welcome to the Movie Genre Classification....\n'

echo 'Install Libraries....'
pip3 install -r ./requirements.txt

echo "Download the Spacy Library..."
python -m spacy download en_core_web_sm

echo "Preprocess and Train the Data..."
python3 model.py

echo "Setting up API on LocalHost using Flask.."
python3 predict.py


