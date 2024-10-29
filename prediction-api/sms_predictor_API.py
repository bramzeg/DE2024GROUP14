import json
import logging
import os
import joblib
from io import StringIO
from flask import jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import kfp
class SMSPredictor:
    def __init__(self):
        self.model = None
        #self.tfidf = TfidfVectorizer()  # Initialize TfidfVectorizer directly

    def load_model(self, model_file_path):
        """
        Load the machine learning model from a joblib file.
        """
        self.model = joblib.load(model_file_path)

    #def fit_tfidf(self, messages):
      #  """
      #  Fit the TF-IDF vectorizer on the training data.
      #  """
      # self.tfidf.fit(messages)

    def predict_classification(self, prediction_input):
        """
        Predict whether the given SMS message is spam or not.
        """
        logging.debug(prediction_input)
        if self.model is None:
            try:
                model_repo = os.environ['MODEL_REPO']
                model_file_path = os.path.join(model_repo, "model.joblib")
                self.model = joblib.load(model_file_path)
            except KeyError:
                print("MODEL_REPO is undefined")
                self.model = joblib.load('model.joblib')

        # Convert the input into a DataFrame for consistency
        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        messages = df['message'].fillna("").astype(str).str.lower()

        # Transform the input message using the loaded TF-IDF vectorizer
        #message_tfidf = self.tfidf.transform(messages)

        # Make predictions
        predictions = self.model.predict(messages)
        logging.info(type(predictions))
        result = predictions[0]

        # Return predictions in a structured JSON response
        # return result
        return jsonify({'result': str(result)}), 200
