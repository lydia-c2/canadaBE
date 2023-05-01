# if these are not showing up, do pip install (the specific library that is missing)
# ex: if flask_cors is not showing, do "pip install flask_cors" and "pip install cors"
#import CORS
from hacks import app, db

from hacks.model.leaderboard import leaderboard_bp
from hacks.model.leaderboard import init_leaderboards
from flask_cors import CORS

from hacks.api.leaderboards import leaderboard_api # initializing function

app.register_blueprint(leaderboard_bp)



@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_leaderboards
        # put your initializing function here

if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8199")



