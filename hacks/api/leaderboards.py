#
# Initializes Leaderboard DB with test data

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from hacks.model.leaderboard import Leaderboard
import json

leaderboard_api = Blueprint('leaderboard_api', __name__,
                   url_prefix='/api/leaderboard')

api = Api(leaderboard_api)

# Setup of key Flask object (app)
class LeaderboardAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate exercise type
            username = body.get('username')
            if username is None or len(username) < 2:
                return {'message': f'Input username'}, 210
            # validate uid
            id = body.get('id')
            password = body.get('password')
            if password is None or len(password) < 2:
                return {'message': f'Input password'}, 210
            # validate uid
            pointsEasy = body.get('pointsEasy')
            if pointsEasy is None or not int:
                return {'message': f'Input points easy (must be integer)'}, 213
            pointsMedium = body.get('pointsMedium')
            if pointsMedium is None or not int:
                return {'message': f'Input points medium (must be integer)'}, 213
            pointsHard = body.get('pointsHard')
            if pointsHard is None or not int:
                return {'message': f'Input points hard (must be integer)'}, 213





            from model.leaderboard import Leaderboard

            io = Leaderboard(id=id,
                        username = username,
                        password = password,
                        pointsEasy = pointsEasy,
                        pointsMedium = pointsMedium,
                        pointsHard = pointsHard,
                        )
            
            Leaderboard = io.create()

            if Leaderboard:
                return jsonify(Leaderboard.read())
            # failure returns error
            return {'message': f'Processed {Leaderboard}, a format error or Usename is duplicate'}, 215
    

    class _Read(Resource):
        def get(self):
            Leaderboards = Leaderboard.query.all()    # read/extract all breads from database
            json_ready = [leaderboard.read() for leaderboard in Leaderboards]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')




