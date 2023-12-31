from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
#import datetime

load_dotenv

import os
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

app = Flask(__name__)
##cors = CORS(app, resources={r"/*/*": {"origins": "*"}})
CORS(app)

""" if __name__ == '__main__':
    app.debug = True
    app.run() """



###localhost app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:d3ctech@localhost/flask'
###external 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:d3ctech@127.0.0.1:3306/flask'
""" app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""viejo metodo cors app.config['CORS_HEADERS'] = 'Content-Type'"""
##app.config['CORS_HEADERS'] = 'Content-Type'


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Revisores(db.Model):
    IdRevisor = db.Column(db.Integer, primary_key=True)
    NombreRevisor = db.Column(db.String(100))

class Inspectores(db.Model):
    IdInspector = db.Column(db.Integer, primary_key=True)
    IdRevisor = db.Column(db.Integer, db.ForeignKey(Revisores.IdRevisor), primary_key=True)
    NombreInspector = db.Column(db.String(100))

class Certificados(db.Model):
    IdCertificado = db.Column(db.Integer, primary_key=True)
    IdRevisor = db.Column(db.Integer, db.ForeignKey(Revisores.IdRevisor), primary_key=True)
    FechaDePresentacion = db.Column(db.Date)

class Obras(db.Model):
    IdObra = db.Column(db.Integer, primary_key=True)
    IdRevisor = db.Column(db.Integer, db.ForeignKey(Revisores.IdRevisor), primary_key=True)
    NombreObra = db.Column(db.String(200))
    Codificacion = db.Column(db.String(50))
    FechaContrato = db.Column(db.Date)
    FechaInicio = db.Column(db.Date)
    PlazoDias = db.Column(db.Integer)
    IdInspector = db.Column(db.Integer, db.ForeignKey(Inspectores.IdInspector), primary_key=True)
    FechaFin = db.Column(db.Date)
    Prorroga = db.Column(db.Integer)

class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ccNumber = db.Column(db.Integer)
    imgUrl = db.Column(db.String(200))
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    origin = db.Column(db.String(100))
    director1 = db.Column(db.String(100))
    director1Genre = db.Column(db.String(10))
    director2 = db.Column(db.String(100))
    director2Genre = db.Column(db.String(10))
    director3 = db.Column(db.String(100))
    director3Genre = db.Column(db.String(10))
    director4 = db.Column(db.String(100))
    director4Genre = db.Column(db.String(10))
    score = db.Column(db.Float)
    host = db.Column(db.String(30))
    date = db.Column(db.Date)
    #date = db.Column(db.DateTime, default = datetime.datetime.now)

    """ def __init__(self, ccNumber, imgUrl, title, year, origin, director1, director1Genre, director2, director2Genre, director3, director3Genre, director4, director4Genre, score, host, date):
        self.ccNumber = ccNumber
        self.imgUrl = imgUrl
        self.title = title
        self.year = year
        self.origin = origin
        self.director1 = director1
        self.director1Genre = director1Genre
        self.director2 = director2
        self.director2Genre = director2Genre
        self.director3 = director3
        self.director3Genre = director3Genre
        self.director4 = director4
        self.director4Genre = director4Genre
        self.score = score
        self.host = host
        self.date = date """


class FilmSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ccNumber', 'imgUrl', 'title', 'year', 'origin', 'director1', 'director1Genre', 'director2', 'director2Genre', 'director3', 'director3Genre', 'director4', 'director4Genre', 'score', 'host', 'date')

film_schema = FilmSchema()
films_schema = FilmSchema(many=True)

class RevisorSchema(ma.Schema):
    class Meta:
        fields = ('IdRevisor', 'NombreRevisor')

revisor_schema = RevisorSchema()
revisores_schema = RevisorSchema(many=True)

"""viejo metodo cors@app.route("/get", methods = ["GET"])
def helloWorld():
      if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
      elif request.method == "GET":
          all_films = Films.query.all()
          results = films_schema.dump(all_films)
          return _corsify_actual_response(jsonify(results))"""
            

@app.route('/get/revisores', methods = ['GET'])
def get_revisores():
    all_revisores_by_IdRevisor = Revisores.query.order_by(Revisores.IdRevisor).all()
    results = revisores_schema.dump(all_revisores_by_IdRevisor)
    return jsonify(results)

@app.route('/get', methods = ['GET'])
def get_films():
    ###all_films = Films.query.all()
    ###results = films_schema.dump(all_films)
    ###return jsonify(results)
    ###all_films = Films.query.all()
    all_films_by_ccNumber = Films.query.order_by(Films.ccNumber).all()
    results = films_schema.dump(all_films_by_ccNumber)
    return jsonify(results)




@app.route('/adv-get/<field>/<contains>', methods = ['GET'])
def get_films_by_field_contains(field, contains):
    all_films_contains = Films.query.filter(getattr(Films,field).contains(contains)).order_by(Films.ccNumber).all()
    results = films_schema.dump(all_films_contains)
    return jsonify(results)


@app.route('/get/<id>', methods = ['GET'])
def post_details(id):
    film = Films.query.get(id)
    return film_schema.jsonify(film)


@app.route('/add', methods = ['POST'])
def add_film():
    ccNumber = request.json['ccNumber']
    imgUrl = request.json['imgUrl']
    title = request.json['title']
    year = request.json['year']
    origin = request.json['origin']
    director1 = request.json['director1']
    director1Genre = request.json['director1Genre']
    director2 = request.json['director2']
    director2Genre = request.json['director2Genre']
    director3 = request.json['director3']
    director3Genre = request.json['director3Genre']
    director4 = request.json['director4']
    director4Genre = request.json['director4Genre']
    score = request.json['score']
    host = request.json['host']
    date = request.json['date']

    films = Films(ccNumber, imgUrl, title, year, origin, director1, director1Genre, director2, director2Genre, director3, director3Genre, director4, director4Genre, score, host, date)
    db.session.add(films)
    db.session.commit()
    return film_schema.jsonify(films)

@app.route('/update/<id>', methods = ['PUT'])
##@cross_origin()
def update_film(id):
    ##if request.method == "OPTIONS": # CORS preflight
        ##return _build_cors_preflight_response()
    ##elif request.method == "PUT":
        film = Films.query.get(id)
        ccNumber = request.json['ccNumber']
        imgUrl = request.json['imgUrl']
        title = request.json['title']
        year = request.json['year']
        origin = request.json['origin']
        director1 = request.json['director1']
        director1Genre = request.json['director1Genre']
        director2 = request.json['director2']
        director2Genre = request.json['director2Genre']
        director3 = request.json['director3']
        director3Genre = request.json['director3Genre']
        director4 = request.json['director4']
        director4Genre = request.json['director4Genre']
        score = request.json['score']
        host = request.json['host']
        date = request.json['date']

        film.ccNumber = ccNumber
        film.imgUrl = imgUrl
        film.title = title
        film.year = year
        film.origin = origin
        film.director1 = director1
        film.director1Genre = director1Genre
        film.director2 = director2
        film.director2Genre = director2Genre
        film.director3 = director3
        film.director3Genre = director3Genre
        film.director4 = director4
        film.director4Genre = director4Genre
        film.score = score
        film.host = host
        film.date = date

        db.session.commit()
        return film_schema.jsonify(film)
        ##return _corsify_actual_response(results)


@app.route('/delete/<id>', methods = ['DELETE'])
def film_delete(id):
    film = Films.query.get(id)
    db.session.delete(film)
    db.session.commit()

    return film_schema.jsonify(film)

"""viejo metodo cors
##cosas del CORS
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response """ 
