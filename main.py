from flask import Flask
from flask_cors import CORS
from flask import render_template, url_for
from hacks import app, db
from pathlib import Path
from flask import send_from_directory

from hacks.model.leaderboard import init_leaderboards
from hacks.api.leaderboards import leaderboard_bp

app.register_blueprint(leaderboard_bp)


@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_leaderboards()


# app.add_url_rule('/photos/<path:filename>', endpoint='photos', view_func=app.send_static_file)
# @app.route('/')
# def photo():
#     image_dir = Path.cwd()/"images/easy"
#     images_paths = [i.posix() for i in image_dir.iterdir()]
#     images = [Images("/image/easy/" + image, 250, 250, 1) for image in images_paths]
#     return render_template('photo1.html')

#@app.route('/')
# def capture_image(self):
#     self.cam = cv2.VideoCapture(0)
#     self.img = self.cam.read()
#     self.cam.release()
#     render_template(index.html,ob=self.img)


#@app.route('/static/images/easy/<path:path>')
#def send_report(path):
    #full_filename = project_path.as_posix() + path
    # url_for('static', filename=f'images/easy/{path}')
    #return render_template("image_template.html", user_image=path)


if __name__ == "__main__":
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8200")