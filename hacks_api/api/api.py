from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.model import # class from model

example_bp = Blueprint("leaderboards", __name__)
example_api = Api(example_bp)


class ExampleAPI(Resource):
# make sure to have all of CRUD made here
# make a second api for images as well, in a different file

class ExampleListAPI(Resource):
# edit the links below in order to 

example_api.add_resource(ExampleAPI, "/data-points")
example_api.add_resource(ExampleListAPI, "/database")