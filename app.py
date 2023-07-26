from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import json
from bson import json_util
import environ

app = Flask(__name__, template_folder='templates')

environ.Env.read_env()
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

MONGO_HOST = env('host')
MONGO_DB_NAME = env('db')
MONGO_COLLECTION_NAME = env('collection')

client = MongoClient(MONGO_HOST)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


@app.route("/entity", methods=["POST"])
def create_entity():
    user_data=request.form.to_dict()
    inserted_user = collection.insert_one(user_data)
    user_data["code"] = str(inserted_user.inserted_id)
    return redirect(url_for('get_all_entity'))

@app.route("/entity", methods=["GET"])
def new_entity():
    return render_template('new.html', json={})

@app.route("/entity/add/<code>", methods=["GET"])
def add_entity(code):
    rec = collection.find_one({"code": code})
    return render_template('new.html', json={"code": code, "name": rec['name']})

@app.route("/", methods=["GET"])
def get_all_entity():
    entity_list = list(collection.find())
    return render_template('list.html', list=json.loads(json_util.dumps(entity_list)))

@app.route("/view_entity/<code>", methods=["GET"])
def view_entity(code):
    entity_list = collection.find({"code": code})
    return render_template('entity/add.html', list=json.loads(json_util.dumps(entity_list)))

@app.route("/delete_entity/<code>", methods=["GET"])
def delete_entity(code):
    collection.delete_one({"code": code} )
    return redirect(url_for('get_all_entity'))


if __name__ == "__main__":
    app.run(debug=True)
