import flask
from data import db_session
from data.users import Jobs, User
from flask import jsonify, Flask, make_response, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'Users':
                [item.to_dict(only=('name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:job_id>',  methods=['GET'])
def get_one_user(job_id):
    session = db_session.create_session()
    users = session.query(User).get(job_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'User': users.to_dict(only=('name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email'))
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    users = User(
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        about=request.json['about'],
        position=request.json['position'],
        address=request.json['address'],
        speciality=request.json['speciality'],
        email=request.json['email']
    )
    session.add(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:job_id>', methods=['DELETE'])
def delete_users(job_id):
    session = db_session.create_session()
    users = session.query(User).get(job_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:job_id>', methods=['PUT'])
def change_users(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    users = session.query(User).filter(User.id == job_id).first()

    users.name = request.json['name']
    users.surname = request.json['surname']
    users.age = request.json['age']
    users.about = request.json['about']
    users.position = request.json['position']
    users.address = request.json['address']
    users.speciality = request.json['speciality']
    users.email = request.json['email']

    session.commit()
    return jsonify({'success': 'OK'})
