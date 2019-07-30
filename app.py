import json
import requests
import bson.errors
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restplus import Api, Resource, fields

api = Api()

app = Flask(__name__)
api.init_app(app)

app.config['MONGO_DBNAME'] = 'starwars_planets'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1/starwars_planets'

mongo = PyMongo(app)

model = api.model('Planet', {
    'name': fields.String(required=True, description='Name of a planet', help='"name" cannot be blank.'),
    'climate': fields.String(required=True, description='Climate of the planet', help='"climate" cannot be blank.'),
    'terrain': fields.String(required=True, description='Terrain type of the planet',
                             help='"terrain" cannot be blank.'),
    'n_appearances': fields.Integer(description='Number of times a planet was featured in a movie'),
})


@api.route('/planets/')
class PlanetsList(Resource):
    def get(self):
        """returns a list of planets in the database"""
        planets_db = mongo.db.starwars_planets
        output = list()

        for planet in planets_db.find():
            output.append({
                'name': planet['name'],
                'climate': planet['climate'],
                'terrain': planet['terrain'],
                'n_appearances': planet['n_appearances']})

        return jsonify({'planets': output})

    @api.expect(model)
    def post(self):
        """add a new planet to the database"""
        planets_db = mongo.db.starwars_planets

        name = request.json['name']
        climate = request.json['climate']
        terrain = request.json['terrain']
        n_appearances = self.get_planet_appearances(name)

        if planets_db.find_one({'name': name}):
            output = 'This planet is already in the database.'

        else:
            planet = planets_db.insert_one({"name": name.capitalize(),
                                            "climate": climate,
                                            "terrain": terrain,
                                            "n_appearances": n_appearances})
            planet_id = planet.inserted_id

            new_planet = planets_db.find_one({'_id': planet_id})
            output = {'name': new_planet['name'],
                      'climate': new_planet['climate'],
                      'terrain': new_planet['terrain'],
                      'n_appearances': new_planet['n_appearances']}

        return jsonify({'result': output})

    def get_planet_appearances(self, name):
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


@api.route('/planets/id/<_id>')
class PlanetId(Resource):
    def get(self, _id):
        """returns a single planet and its details using the id as the search parameter"""
        planets_db = mongo.db.starwars_planets

        try:
            planet = planets_db.find_one({'_id': ObjectId(_id)})
            output = {'name': planet['name'],
                      'climate': planet['climate'],
                      'terrain': planet['terrain'],
                      'n_appearances': planet['n_appearances']}

        except bson.errors.InvalidId as e:
            print(e)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'
        except TypeError as te:
            print(te)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'

        return jsonify({'result': output})

    def delete(self, planet_id):
        """deletes a planet from the database using the id as the search parameter"""
        planets_db = mongo.db.starwars_planets

        try:
            planet = planets_db.find_one_and_delete({'_id': ObjectId(_id)})
            name = planet['name']
            output = name.capitalize() + ' has been deleted.'

        except bson.errors.InvalidId as e:
            print(e)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'

        except TypeError as te:
            print(te)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'

        return jsonify({'result': output})

    def put(self, planet_id):
        """updates a planet from the database using the id as the search parameter"""
        planets_db = mongo.db.starwars_planets

        name = request.json['name']
        climate = request.json['climate']
        terrain = request.json['terrain']

        output = list()

        try:
            planet = planets_db.find_one_and_update({'_id': ObjectId(planet_id)},
                                                    {'$set': {
                                                        'name': name,
                                                        'climate': climate,
                                                        'terrain': terrain
                                                    }})
            output = {'name': planet['name'],
                      'climate': planet['climate'],
                      'terrain': planet['terrain'],
                      'n_appearances': planet['n_appearances']}

        except bson.errors.InvalidId as e:
            print(e)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'

        except TypeError as te:
            print(te)
            output = 'ID not found! If an item does not appear in our records, it does not exist.'

        return jsonify({'result': output})


@api.route('/planets/name/<name>')
class PlanetName(Resource):
    def get(self, name):
        """returns a single planet and its details using the name as the search parameter"""
        planets_db = mongo.db.starwars_planets
        planet = planets_db.find_one({'name': name.capitalize()})

        if planet:
            output = {'name': planet['name'],
                      'climate': planet['climate'],
                      'terrain': planet['terrain'],
                      'n_appearances': planet['n_appearances']}
        else:
            output = 'No results found.'

        return jsonify({'result': output})

    def delete(self, name):
        """deletes a planet from the database using the name as the search parameter"""
        planets_db = mongo.db.starwars_planets

        try:
            planet = planets_db.find_one_and_delete({'name': name.capitalize()})
            name = planet['name']
            output = name.capitalize() + ' has been deleted.'

        except TypeError as te:
            print(te)
            output = 'Name not found! If an item does not appear in our records, it does not exist.'

        return jsonify({'result': output})

    def put(self, name):
        """updates a planet from the database using the name as the search parameter"""
        planets_db = mongo.db.starwars_planets

        name = request.json['name']
        climate = request.json['climate']
        terrain = request.json['terrain']

        output = list()

        try:
            planet = planets_db.find_one_and_update({'name': name.capitalize()},
                                                    {'$set': {
                                                        'name': name,
                                                        'climate': climate,
                                                        'terrain': terrain
                                                    }}, {'new': True}, upsert=False)
            output = {'name': planet['name'],
                      'climate': planet['climate'],
                      'terrain': planet['terrain'],
                      'n_appearances': planet['n_appearances']}
            status_code = 200

        except TypeError as te:
            print(te)
            output = 'Name not found! If an item does not appear in our records, it does not exist.'
            status_code = 404

        return jsonify({'result': output}), status_code


if __name__ == "__main__":
    app.run(debug=True)
