import utils as utils
import pandas as pd
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with, abort
from datetime import datetime

app = Flask(__name__)

# Cloud SQL
DATABASE_PASSWORD ='YOUR DATABASE PASSWORD'
PUBLIC_IP_ADDRESS ='YOUR DATABASE PUBLIC IP ADDRESS'
DATABASE_NAME ='YOUR DATABASE NAME'
PROJECT_ID ='YOUR GCP PROJECT ID'
INSTANCE_NAME ='YOUR INSTANCE NAME'

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{DATABASE_PASSWORD}@{PUBLIC_IP_ADDRESS}/{DATABASE_NAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSV_REPORT'] = '/tmp'

db = SQLAlchemy(app)

class ILTSessionModel(db.Model):
  __tablename__ = 'ilt_session'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  learning_path = db.Column(db.String(200), nullable=False)
  session_name = db.Column(db.String(200), nullable=False)
  mentor = db.Column(db.String(200), nullable=False)
  date = db.Column(db.Date, nullable=False)
  start_time = db.Column(db.Time, nullable=False)
  end_time = db.Column(db.Time, nullable=False)

  def __init__(self, title, learning_path, session_name, mentor, date, start_time, end_time):
    self.title = title
    self.learning_path = learning_path
    self.session_name = session_name
    self.mentor = mentor
    self.date = date
    self.start_time = start_time
    self.end_time = end_time

class ILTFeedbackModel(db.Model):
  __tablename__ = 'ilt_feedback'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(200), nullable=False)
  learning_path = db.Column(db.String(200), nullable=False)
  session_name = db.Column(db.String(200), nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  feedback = db.Column(db.Text(), nullable=False)
  relevant = db.Column(db.Integer, nullable=True)
  sentiment = db.Column(db.Integer, nullable=True)
  validity = db.Column(db.Integer, nullable=True)

  def __init__(self, name, email, learning_path, session_name, rating, feedback, relevant, sentiment, validity):
    self.name = name
    self.email = email
    self.learning_path = learning_path
    self.session_name = session_name
    self.rating = rating
    self.feedback = feedback
    self.relevant = relevant
    self.sentiment = sentiment
    self.validity = validity

ilt_session_args = reqparse.RequestParser()
ilt_session_args.add_argument("title", type=str, help="Judul sesi tidak boleh kosong dan bertipe data String")
ilt_session_args.add_argument("learning_path", type=str, help="Learning path sesi tidak boleh kosong dan bertipe data String")
ilt_session_args.add_argument("session_name", type=str, help="Nama sesi tidak boleh kosong dan bertipe data String")
ilt_session_args.add_argument("mentor", type=str, help="Mentor sesi tidak boleh kosong dan bertipe data String")
ilt_session_args.add_argument("date", type=lambda x: datetime.strptime(x, '%Y-%m-%d'), help="Tanggal sesi tidak boleh kosong dan bertipe data Date")
ilt_session_args.add_argument("start_time", type=lambda x: datetime.strptime(x, '%H:%M'), help="Waktu mulai sesi tidak boleh kosong dan bertipe data Time")
ilt_session_args.add_argument("end_time", type=lambda x: datetime.strptime(x, '%H:%M'), help="Waktu berakhir sesi tidak boleh kosong dan bertipe data Time")

ilt_session_patch_args = reqparse.RequestParser()
ilt_session_patch_args.add_argument("title", type=str, help="Judul sesi tidak boleh kosong dan bertipe data String")
ilt_session_patch_args.add_argument("learning_path", type=str, help="Learning path sesi tidak boleh kosong dan bertipe data String")
ilt_session_patch_args.add_argument("session_name", type=str, help="Nama sesi tidak boleh kosong dan bertipe data String")
ilt_session_patch_args.add_argument("mentor", type=str, help="Mentor sesi tidak boleh kosong dan bertipe data String")
ilt_session_patch_args.add_argument("date", type=lambda x: datetime.strptime(x, '%Y-%m-%d'), help="Tanggal sesi tidak boleh kosong dan bertipe data Date")
ilt_session_patch_args.add_argument("start_time", type=lambda x: datetime.strptime(x, '%H:%M:%S'), help="Waktu mulai sesi tidak boleh kosong dan bertipe data Time")
ilt_session_patch_args.add_argument("end_time", type=lambda x: datetime.strptime(x, '%H:%M:%S'), help="Waktu berakhir sesi tidak boleh kosong dan bertipe data Time")

ilt_feedback_args = reqparse.RequestParser()
ilt_feedback_args.add_argument("name", type=str, help="Nama pengisi feedback tidak boleh kosong dan bertipe data String")
ilt_feedback_args.add_argument("email", type=str, help="Email pengisi feedback tidak boleh kosong dan bertipe data String")
ilt_feedback_args.add_argument("learning_path", type=str, help="Learning Path pengisi feedback tidak boleh kosong dan bertipe data String")
ilt_feedback_args.add_argument("session_name", type=str, help="Nama sesi tidak boleh kosong dan bertipe data String")
ilt_feedback_args.add_argument("rating", type=int, help="Rating sesi tidak boleh kosong dan bertipe data Integer")
ilt_feedback_args.add_argument("feedback", type=str, help="Feedback sesi tidak boleh kosong dan bertipe data Text")

ilt_session_resource_fields = {
  'id': fields.Integer,
  'title': fields.String,
  'learning_path': fields.String,
  'session_name': fields.String,
  'mentor': fields.String,
  'date': fields.String,
  'start_time': fields.String,
  'end_time': fields.String,
}

ilt_feedback_resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'email': fields.String,
  'learning_path': fields.String,
  'session_name': fields.String,
  'rating': fields.Integer,
  'feedback': fields.String,
  'relevant': fields.Integer,
  'sentiment': fields.Integer,
  'validity': fields.Integer,
}

class ILTSession(Resource):
  @marshal_with(ilt_session_resource_fields)
  def get(self):
    result = ILTSessionModel.query.all()
    return result

  @marshal_with(ilt_session_resource_fields)
  def post(self):
    args = ilt_session_args.parse_args()
    result = ILTSessionModel.query.filter_by(session_name=args['session_name']).first()
    if result:
      abort(409, message="Nama sesi ILT tersebut tidak tersedia (sudah ada atau kondisi lain)")
    ilt_session = ILTSessionModel(title=args['title'], learning_path=args['learning_path'], session_name=args['session_name'], mentor=args['mentor'], date=args['date'], start_time=args['start_time'], end_time=args['end_time'])
    db.session.add(ilt_session)
    db.session.commit()
    return ilt_session, 201

class ILTSessionDetail(Resource):
  @marshal_with(ilt_session_resource_fields)
  def get(self, session_name):
    result = ILTSessionModel.query.filter_by(session_name=session_name).first()
    if not result:
      abort(404, message="Nama sesi ILT tersebut tidak tersedia")
    return result

  @marshal_with(ilt_session_resource_fields)
  def patch(self, session_name):
    args = ilt_session_patch_args.parse_args()
    result = ILTSessionModel.query.filter_by(session_name=session_name).first()
    if not result:
      abort(404, message="Nama sesi ILT tersebut tidak tersedia")

    if args['title']:
      result.title = args['title']
    if args['learning_path']:
      result.learning_path = args['learning_path']
    if args['session_name']:
      result.session_name = args['session_name']
    if args['mentor']:
      result.mentor = args['mentor']
    if args['date']:
      result.date = args['date']
    if args['start_time']:
      result.start_time = args['start_time']
    if args['end_time']:
      result.end_time = args['end_time']

    db.session.commit()
    return result

  def delete(self, session_name):
    result = ILTSessionModel.query.filter_by(session_name=session_name).first()
    if not result:
      abort(404, message="Nama sesi ILT tersebut tidak tersedia")
    delete_result = ILTSessionModel.query.filter_by(session_name=session_name).delete()
    db.session.commit()
    if delete_result:
      return {"message": "Data sesi ILT telah dihapus"}, 204
    else:
      abort(500, message="Server atau database error")

class ILTSessionPath(Resource):
  @marshal_with(ilt_session_resource_fields)
  def get(self, session_path):
    if session_path == 'android':
      learning_path = 'Android'
    elif session_path == 'machine-learning':
      learning_path = 'Machine Learning'
    elif session_path == 'cloud-computing':
      learning_path = 'Cloud Computing'
    elif session_path == 'soft-skill':
      learning_path = 'Soft Skill'
    else:
      abort(404, message="Learning path tersebut tidak tersedia")
    result = ILTSessionModel.query.filter_by(learning_path=learning_path).all()
    return result

class ILTFeedback(Resource):
  @marshal_with(ilt_feedback_resource_fields)
  def get(self):
    result = ILTFeedbackModel.query.all()
    return result

  @marshal_with(ilt_feedback_resource_fields)
  def post(self):
    args = ilt_feedback_args.parse_args()
    result = ILTSessionModel.query.filter_by(session_name=args['session_name']).first()
    if not result:
      abort(404, message="Nama sesi ILT tersebut tidak tersedia")

    relevant = utils.predict_relevant(args['feedback'])
    sentiment = utils.predict_sentiment(args['feedback'], relevant)
    validity = utils.feedback_validity(args['rating'], relevant, sentiment)

    relevant += 1
    if sentiment is not None:
      sentiment += 1
    validity += 1

    ilt_feedback = ILTFeedbackModel(name=args['name'], email=args['email'], learning_path=args['learning_path'], session_name=args['session_name'], rating=args['rating'], feedback=args['feedback'], relevant=relevant, sentiment=sentiment, validity=validity)
    db.session.add(ilt_feedback)
    db.session.commit()
    return ilt_feedback, 201

class ILTFeedbackDetail(Resource):
  @marshal_with(ilt_feedback_resource_fields)
  def get(self, data_id):
    result = ILTFeedbackModel.query.filter_by(id=data_id).all()
    if not result:
      abort(404, message="Id feedback tersebut tidak tersedia")
    return result

  def delete(self, data_id):
    result = ILTFeedbackModel.query.filter_by(id=data_id).first()
    if not result:
      abort(404, message="Id feedback tersebut tidak tersedia")
    delete_result = ILTFeedbackModel.query.filter_by(id=data_id).delete()
    db.session.commit()
    if delete_result:
      return {"message": "Data feedback yang diprediksi telah dihapus"}, 204
    else:
      abort(500, message="Server atau database error")

class ILTFeedbackBest(Resource):
  @marshal_with(ilt_feedback_resource_fields)
  def get(self):
    result = ILTFeedbackModel.query.filter_by(rating=5, relevant=2, sentiment=2, validity=2).limit(3).all()
    return result

class ILTFeedbackCSV(Resource):
  def get(self):
    result = ILTFeedbackModel.query.all()
    result = marshal(result, ilt_feedback_resource_fields)
    result = pd.DataFrame(result)
    result_csv = result.to_csv(app.config['CSV_REPORT'] + '/ilt_feedback.csv', sep=';', index=False)
    try:
      return send_from_directory(app.config['CSV_REPORT'], 'ilt_feedback.csv', as_attachment=True)
    except FileNotFoundError:
      abort(404)
    return result_csv

class ILTFeedbackRangedCSV(Resource):
  def get(self, start_id, end_id):
    result = ILTFeedbackModel.query.filter_by(id=start_id).first()
    if not result:
      abort(404, message="Id feedback tersebut tidak tersedia (id mulai)")
    result = ILTFeedbackModel.query.filter_by(id=end_id).first()
    if not result:
      abort(404, message="Id feedback tersebut tidak tersedia (id terakhir)")
    result = ILTFeedbackModel.query.all()
    result = marshal(result, ilt_feedback_resource_fields)
    result = pd.DataFrame(result)
    result = result[(result["id"] >= start_id) & (result["id"] <= end_id)]
    result_csv = result.to_csv(app.config['CSV_REPORT'] + '/ilt_feedback_ranged.csv', sep=';', index=False)
    try:
      return send_from_directory(app.config['CSV_REPORT'], 'ilt_feedback_ranged.csv', as_attachment=True)
    except FileNotFoundError:
      abort(404)
    return result_csv

api = Api(app)

ROOT_PATH = "/api/v1"

api.add_resource(ILTSession, ROOT_PATH + "/iltsession")
api.add_resource(ILTSessionDetail, ROOT_PATH + "/iltsession/<string:session_name>")
api.add_resource(ILTSessionPath, ROOT_PATH + "/iltsession/learningpath/<string:session_path>")
api.add_resource(ILTFeedback, ROOT_PATH + "/iltsession/feedback")
api.add_resource(ILTFeedbackDetail, ROOT_PATH + "/iltsession/feedback/<string:data_id>")
api.add_resource(ILTFeedbackBest, ROOT_PATH + "/iltsession/feedback/bestfeedback")
api.add_resource(ILTFeedbackCSV, ROOT_PATH + "/iltsession/feedback/csv")
api.add_resource(ILTFeedbackRangedCSV, ROOT_PATH + "/iltsession/feedback/csv/<int:start_id>-<int:end_id>")

if __name__ == "__main__":
  app.run()