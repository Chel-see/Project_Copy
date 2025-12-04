from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
index_views = Blueprint('index_views', __name__, template_folder='templates')


@index_views.route('/', methods=['GET'])
def index_page():
      # This replaces the HTML template with a simple JSON response
    return {
        render_template('index.html', is_authenticated=False)
    }



# @index_views.route('/', methods=['GET'])
# def index_page():
#     return jsonify({
#         "status": "running",
#         "message": "API is live!",
#         "available_endpoints": ["/user", "/auth", "/position", "/shortlist"]
#     })


@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})