from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.users import Jobs, User

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True)
parser.add_argument('about', required=True)
parser.add_argument('position', required=True)
parser.add_argument('address', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('email', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message="user {} not found".format(user_id))


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('name', 'surname', 'age', 'about', 'position', 'address', 'speciality', 'email')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        print(session.query(User).filter(User.email == args['email']).first())
        if session.query(User).filter(User.email == args['email']).first():
            abort(500, message="Пользователь с почтой: {} уже существует".format(args['email']))
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            about=args['about'],
            position=args['position'],
            address=args['address'],
            speciality=args['speciality'],
            email=args['email']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run()
