"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Method GET
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

#Retrieve one member
#Which returns the member of the family where id == member_id.
@app.route('/members/<int:id>', methods=['GET'])
def retrieve_member(id):
    member = jackson_family.get_member(id)
#    if id in member:
    return jsonify(member), 200
#    elif id not in member:
#        return 'Member not found', 400
#    else:
#        return 'Error 500', 500 

#Add (POST) new member
#Which adds a new member to the family data structure.
@app.route('/new_member/<int:id>', methods=['POST'])
def add_member(new_member):
        added_member = jackson_family.add_member(new_member)
        return jsonify(added_member), 200

#DELETE one member
#Which deletes a family member with id == member_id
@app.route('/delete_member/<int:id>', methods=['DELETE'])
def delete_member(id):
        deleted_member = jackson_family.delete_member(id)
        return jsonify(deleted_member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)