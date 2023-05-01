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

# Setup of key Flask object (app)
app = Flask(__name__)

# Setup SQLAlchemy object and properties for the database (db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "SECRET_KEY"
db = SQLAlchemy(app)

# Images storage
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]  # supported file types
app.config["UPLOAD_FOLDER"] = "volumes/uploads/"  # location of user uploaded content




from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.exc import IntegrityError
import json
from werkzeug.security import generate_password_hash, check_password_hash


# 
# bread ranking DB class that maps rank SQL table 
#
class Bread(db.Model):
    __tablename__ = "leaderboard"

    # 
    # bread DB columns for easy, medium and hard points with user info
    #    
    id = Column(Integer, primary_key=True)
    _breadName = Column(String(255), unique=True, nullable=False)
    _rank = Column(String(255), nullable=False)

    # 
    # bread DB class constructor 
    #
    def __init__(self, breadName, rank):
        self._breadName = breadName
        self._rank = rank

    def __repr__(self):
        return "<Bread(id='%s', breadName='%s', rank='%s'>" % (
            self.id,
            self._breadName,
            self._rank,
        )

    # 
    # Returns Bread ranking username
    #    
    @property
    def breadName(self):
        return self._breadName

    # 
    # Sets Leaderboard username
    #        
    @breadName.setter
    def breadName(self, value):
        self._breadName = value

    # 
    # checks bread name valid
    #            
    def is_breadName(self, breadName):
        return self._breadName == breadName

    # 
    # Returns ranking
    #        
    @property
    def rank(self):
        return self._rank

    # 
    # Sets Leaderboard easy points
    #        
    @rank.setter
    def rank(self, value):
        self._rank = value

    # Converts Leaderboard to dictionary
    #            
    def to_dict(self):
        return {"id": self.id, "breadName": self.breadName, "rank": self.rank}

    # 
    # Converts Leaderboard to string values
    #                
    def __str__(self):
        return json.dumps(self.read())

    # 
    # Creates Leaderboard database
    #                
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    # 
    # Returns Leaderboard name value pairs
    #            
    def read(self):
        return {
            "id": self.id,
            "breadName": self.breadName,
            "rank": self.rank
        }

    # 
    # Updates Leaderboard DB rows for points and user data
    #                
    def update(self, breadName="", rank=""):
        """only updates values with length"""
        if len(breadName) > 0:
            self.breadName = breadName
        if len(rank) > 0:
            self.pointsEasy = rank
        db.session.add(self)
        db.session.commit()
        return self

    # 
    # Delets Leaderboard row from teh DB
    #                
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    

#
# Initializes Leaderboard DB with test data
#   
def init_bread():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        l1 = Bread(breadName="sourdough", rank="2")
        l2 = Bread(breadName="whole grain", rank="4")
        l3 = Bread(breadName="pretzel", rank="1")
        l4 = Bread(breadName="white bread", rank="3")
        breads = [l1, l2, l3, l4]

        """Builds sample user/note(s) data"""
        for l in breads:
            try:
                '''add user to table'''
                object = l.create()
                print(f"Created new uid {object.breadName}")
                db.session.add(l)
                db.session.commit()
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {l.breadName}, or error.")

init_bread()





# full list of leaderboard
class BreadListAPI(Resource):
    # GET method
    def get(self):
        try:
            # attempts to find the entire database requested and is stored in variable
            breads = db.session.query(Bread).all()
            # sends back the entire database
            return [bread.to_dict() for bread in breads]
        except Exception as e:
            # error checking for request errors
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    # DELETE method
    def delete(self):
        try:
            # deletes entire database
            db.session.query(Bread).delete()
            db.session.commit()
            return []
        except Exception as e:
            # checks for errors in request
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500