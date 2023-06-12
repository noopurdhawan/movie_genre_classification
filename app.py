
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("model/log_model.pkl",'rb'))
mlb = pickle.load(open('model/mlb.pkl','rb'))
tfidf_vect = pickle.load(open('model/tfidf_vectorizer.pkl','rb'))


@app.route('/', methods=['POST'])
def predict_genre():
    """
    """
    try:
        data = request.get_json()
        overview = data['overview']
        pred = max(model.predict(tfidf_vect.transform(overview.strip().lower().split())), key=max)
        result = [mlb.classes_[ind] for ind in np.where(pred == 1)[0]]
        status = 200
        return jsonify({'genre': result})   
    except:
        # Set the status code 400 if Bad Request
        status = 400
        data = [{'message': 'Bad Request'}]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

