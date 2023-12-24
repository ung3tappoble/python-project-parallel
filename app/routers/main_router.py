from flask import render_template, Blueprint, Response
from services import main_service

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def main_page():
    latest_mouse_data = main_service.get_latest_mouse_data()

    if latest_mouse_data:
        x_coordinate, y_coordinate, image_data = latest_mouse_data
        return render_template('index.html', x_coordinate=x_coordinate,
                               y_coordinate=y_coordinate, image_data=image_data,)
    else:
        return render_template('index.html', x_coordinate=None,
                               y_coordinate=None, image_data=None)