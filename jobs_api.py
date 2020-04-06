import flask
from data import db_session
from data.users import Jobs
from flask import jsonify, Flask, make_response, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'Jobs':
                [item.to_dict(only=('user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>',  methods=['GET'])
def get_one_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'Job': jobs.to_dict(only=('user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators'))
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        user_id=request.json['user_id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def change_jobs(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['user_id', 'job', 'is_finished', 'team_leader', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == job_id).first()
    jobs.user_id = request.json['user_id']
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.is_finished = request.json['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})
