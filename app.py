from flask import Flask, render_template, request, jsonify
from backend.api.User_methods import User
import os
app = Flask(__name__, static_folder='frontend', template_folder='frontend/templates')

@app.route('/')
def index():
    # Log the current working directory
    # app.logger.info("Current working directory: %s", os.getcwd())
    # template_folder = os.path.join(os.getcwd(), 'frontend/templates')
    # app.logger.info("Looking for template in: %s", template_folder)

    return render_template('index.html')

@app.route('/find_waterbodies', methods=['POST'])
def find_waterbodies():
    address = request.form['address']
    user = User('User', address)
    closest_waterbodies = user.find_closest_waterbodies()
    return jsonify(closest_waterbodies)

@app.route('/get_waterbody_details', methods=['GET'])
def get_waterbody_details():
    waterbody_name = request.args.get('waterbody')
    user = User('User', '')  
    fish_data = user.getWaterbody(waterbody_name)
    return render_template('fish_details.html', waterbody_name=waterbody_name, fish_data=fish_data)
    # return jsonify(fish_data)

if __name__ == '__main__':
    app.run(debug=True)
