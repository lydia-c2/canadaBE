#from flask import Blueprint, request
#from flask_restful import Api, Resource, reqparse
#from .. import db
# from ..model.model 
# import class from model

# example_bp = Blueprint("leaderboards", __name__)
# example_api = Api(example_bp)


# class ExampleAPI(Resource):
# make sure to have all of CRUD made here
# make a second api for images as well, in a different file

# class ExampleListAPI(Resource):
# edit the links below in order to 

# example_api.add_resource(ExampleAPI, "/data-points")
# example_api.add_resource(ExampleListAPI, "/database")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.Bread import Bread


Bread_api = Blueprint('Bread_api', __name__,
                   url_prefix='/api/Bread')

api = Api(Bread_api)

# Setup of key Flask object (app)
class BreadAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate exercise type
            breadName = body.get('breadName')
            if breadName is None or len(breadName) < 2:
                return {'message': f'Input Bread Type'}, 210
            # validate uid
            id = body.get('id')
            uid = str(datetime.now()) # temporary UID that is unique to fill garbage data
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 212
            rank = body.get('rank')
            if rank is None or not int:
                return {'message': f'Input rank (must be integer)'}, 213

            from model.Bread import Bread

            io = Bread(id=id,
                        uid = uid,
                        breadName = breadName,
                        rank = rank,
                        )
            
            Bread = io.create()

            if Bread:
                return jsonify(Bread.read())
            # failure returns error
            return {'message': f'Processed {Bread}, a format error or User ID {uid} is duplicate'}, 215
    

    class _Read(Resource):
        def get(self):
            Breads = Bread.query.all()    # read/extract all breads from database
            json_ready = [Bread.read() for Bread in Breads]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')




