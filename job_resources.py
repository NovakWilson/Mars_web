from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.users import Jobs

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True)
parser.add_argument('user_id', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message="Job {} not found".format(job_id))


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'Jobs': [item.to_dict(
            only=('user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators')) for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            user_id=args['user_id'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=bool(args['is_finished'])
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    abort_if_job_not_found(1)
    app.run()
