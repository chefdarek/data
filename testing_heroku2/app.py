"""

This module takes user input in JSON format, converts it and encodes it.
It also opens the pickled module trained in AWS, and uses the encoded inputs to predict a probaility for each class.
The module will loop over states and output the probabilities in each state, the output will have the following:
{state: "name of state": {probability of "citation", "No citation", "arrest", "search_conducted (BOOL)"} 
The output will be put in a jsonframe then transformed into a JSON file which is then pushed GET back to the user.

features = ['state', 'hour', 'night', 'location', 'lat', 'lng', 'district', 'subject_age', 'subject_race', 'subject_sex', 'type']

"""

from flask import Flask, render_template, request, jsonify
import category_encoders as ce
import pickle
import pandas as pd
import os

def create_app():
  """Create and configure an instance of the Flask application."""
  app = Flask(__name__)


  @app.route('/')
  def root():
    pass
    
  @app.route('/api', methods=['POST'])
  def json():
    age = request.json["age"]
    race = request.json['race']
    sex = request.json['sex']
    types = request.json['types']
    night = request.json['night']
    states = ['Az', 'Ca',
                'Co', 'Ct',
                'Fl',
                'Ga',
                'Ia',
                'Il',
                'Ma',
                'Md',
                'Mi',
                'Mt',
                'Nc',
                'Nh',
                'Nj',
                'Nv',
                'Oh',
                'Ri',
                'Dc',
                'Dd',
                'Tn',
                'Tx',
                'Vt',
                'Wa',
                'Wi']

    loaded_encoder = pickle.load(open("testing_encoder.pkl", 'rb'))
    loaded_model = pickle.load(open('testing_model.pkl', 'rb'))

    final_state_json = []
    json_responses_state = {}
    results = []
    for state in states:

        inputs = [state, night, age, race, sex, types]
        pred_input = pd.DataFrame([inputs], columns=['states', 'night', 'subject_age', 'subject_race', 'subject_sex', 'type'] )
        pred_input_encoded = loaded_encoder.transform(pred_input)
        result = loaded_model.predict_proba(pred_input_encoded)

        json_responses = {}
        for i in range(len(result[0])):
            json_response = {loaded_model.classes_[i]: str(result[0][i])}
            json_responses.update(json_response)
        json_response_state = {"{0}".format(state): json_responses}
        final_state_json.append(json_response_state)
    json = list(final_state_json)
    return jsonify(json)

  return app

if __name__ == "__main__":
  app = create_app()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)