import json
import requests
import bson.errors
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'starwars_planets'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1/starwars_planets'

mongo = PyMongo(app)


@app.route('/')
def greeting():
    return jsonify({'result': 'Hello there!'})


def get_planet_appearances(name):
    """accesses swapi to get the number of times the planet appeared in a movie"""
    swapi_url = 'https://swapi.co/api/planets/?search=' + name
    response = requests.get(swapi_url)
    planet_data = json.loads(response.content)

    try:
        appearances = len(planet_data['results'][0]['films'])

    except IndexError as e:
        print(e)
        appearances = 0

    return appearances


@app.route('/planets', methods=['GET'])
def get_planets():
    """get a list of all planets registered in the database and their values in json format"""
    planets = mongo.db.starwars_planets
    output = list()

    for planet in planets.find():
        output.append({
            'nome': planet['nome'],
            'clima': planet['clima'],
            'terreno': planet['terreno'],
            'numero_de_aparicoes': planet['numero_de_aparicoes']})

    return jsonify({'planets': output})


@app.route('/planets', methods=['POST'])
def add_planet():
    """add a new planet to the database"""
    planets = mongo.db.starwars_planets

    name = request.json['name']
    climate = request.json['climate']
    terrain = request.json['terrain']
    n_appearances = get_planet_appearances(name)

    if planets.find_one({'nome': name}):
        output = 'This planet is already in the database.'

    else:
        planet = planets.insert_one({"nome": name.capitalize(),
                                     "clima": climate,
                                     "terreno": terrain,
                                     "numero_de_aparicoes": n_appearances})
        planet_id = planet.inserted_id

        new_planet = planets.find_one({'_id': planet_id})
        output = {'nome': new_planet['nome'],
                  'clima': new_planet['clima'],
                  'terreno': new_planet['terreno'],
                  'numero_de_aparicoes': new_planet['numero_de_aparicoes']}

    return jsonify({'result': output})


@app.route('/planets/name/<name>', methods=['GET'])
def find_planet_by_name(name):
    """get the values of a single planet in json format using the name as the search parameter"""
    planets = mongo.db.starwars_planets
    planet = planets.find_one({'nome': name.capitalize()})

    if planet:
        output = {'nome': planet['nome'],
                  'clima': planet['clima'],
                  'terreno': planet['terreno'],
                  'numero_de_aparicoes': planet['numero_de_aparicoes']}
    else:
        output = 'No results found.'

    return jsonify({'result': output})


@app.route('/planets/id/<_id>', methods=['GET'])
def find_planet_by_id(_id):
    """get the values of a single planet in json format using the id as the search parameter"""
    planets = mongo.db.starwars_planets

    try:
        planet = planets.find_one({'_id': ObjectId(_id)})

        output = {'nome': planet['nome'],
                  'clima': planet['clima'],
                  'terreno': planet['terreno'],
                  'numero_de_aparicoes': planet['numero_de_aparicoes']}

    except bson.errors.InvalidId as e:
        print(e)
        output = 'ID not found! If an item does not appear in our records, it does not exist.'
    except TypeError as te:
        print(te)
        output = 'ID not found! If an item does not appear in our records, it does not exist.'

    return jsonify({'result': output})


@app.route('/planets/name/<name>', methods=['DELETE'])
def delete_planet_by_name(name):
    """deletes a planet from the database that matches the name"""
    planets = mongo.db.starwars_planets
    planet = planets.find_one({'nome': name.capitalize()})

    if planet:
        planets.delete_one({'nome': name.capitalize()})
        output = name.capitalize() + ' has been deleted.'
    else:
        output = 'Name not found! If an item does not appear in our records, it does not exist.'

    return jsonify({'result': output})


@app.route('/planets/id/<_id>', methods=['DELETE'])
def delete_planet_by_id(_id):
    """deletes a planet from the database that matches the id"""
    planets = mongo.db.starwars_planets

    try:
        planet = planets.find_one({'_id': ObjectId(_id)})
        name = planet['nome']

        planets.delete_one({'nome': name.capitalize()})
        output = name.capitalize() + ' has been deleted.'
    except bson.errors.InvalidId as e:
        print(e)
        output = 'ID not found! If an item does not appear in our records, it does not exist.'
    except TypeError as te:
        print(te)
        output = 'ID not found! If an item does not appear in our records, it does not exist.'

    return jsonify({'result': output})


if __name__ == "__main__":
    app.run(debug=True)
