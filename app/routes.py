import requests
from flask import redirect, render_template, request, url_for, flash, Response
from app import config
from app import app
from datetime import datetime

# User View

@app.route('/', methods=['GET'])
def home():
  ilt_feedback_best = requests.get(config.ILT_FEEDBACK_BEST)
  response_ilt_feedback_best = ilt_feedback_best.json()
  return render_template('index.html', ilt_feedback_best=response_ilt_feedback_best)

@app.route('/ilt-session', methods=['GET', 'POST'])
def ilt_session():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    learning_path = request.form['learning-path']
    session_name = request.form['session-name']
    rating = request.form['rating']
    feedback = request.form['feedback']

    user_input = {"name": name, "email": email, "learning_path": learning_path, "session_name": session_name, "rating": rating, "feedback": feedback}
    ilt_feedback = requests.post(config.ILT_FEEDBACK, json=user_input)

    if ilt_feedback.status_code == 201:
      flash('Feedback telah terkirim!', 'success')
      return redirect(url_for('ilt_session'))
    elif ilt_feedback.status_code == 404 :
      flash('Nama sesi tersebut tidak tersedia!', 'danger')
      return redirect(url_for('ilt_session'))
    else:
      return redirect(url_for('ilt_session'))

  ilt_session_detail = requests.get(config.ILT_SESSION_DETAIL)
  ilt_session_path = requests.get(config.ILT_SESSION_PATH)
  response_ilt_session_detail = ilt_session_detail.json()
  response_ilt_session_path = ilt_session_path.json()
  return render_template('ilt-session.html', ilt_session_detail=response_ilt_session_detail, ilt_session_path=response_ilt_session_path, datetime=datetime)

# Admin View

@app.route('/admin/ilt-session', methods=['GET', 'POST'])
def admin_ilt_session():
  if request.method == 'POST':
    title = request.form['title']
    learning_path = request.form['learning-path']
    session_name = request.form['session-name']
    mentor = request.form['mentor']
    date = request.form['date']
    start_time = request.form['start-time']
    end_time = request.form['end-time']

    user_input = {"title": title, "learning_path": learning_path, "session_name": session_name, "mentor": mentor, "date": date, "start_time": start_time, "end_time": end_time}
    ilt_session = requests.post(config.ILT_SESSION, json=user_input)

    if ilt_session.status_code == 201:
      flash('Data sesi ILT telah ditambahkan!', 'success')
      return redirect(url_for('admin_ilt_session'))
    elif ilt_session.status_code == 409:
      flash('Nama sesi ILT tersebut tidak tersedia (sudah ada atau kondisi lain)', 'danger')
      return redirect(url_for('admin_ilt_session'))
    else:
      return redirect(url_for('admin_ilt_session'))

  ilt_session = requests.get(config.ILT_SESSION)
  response_ilt_session = ilt_session.json()
  return render_template('admin-ilt-session.html', ilt_session=response_ilt_session, datetime=datetime)

@app.route('/admin/ilt-session/update/<string:session_name>', methods=['POST'])
def patch_ilt_session(session_name):
  title = request.form['title']
  learning_path = request.form['learning-path']
  session = request.form['session-name']
  mentor = request.form['mentor']
  date = request.form['date']
  start_time = request.form['start-time'] + ':00'
  end_time = request.form['end-time'] + ':00'
  user_input = {"title": title, "learning_path": learning_path, "session_name": session, "mentor": mentor, "date": date, "start_time": start_time, "end_time": end_time}
  ilt_session = requests.patch(config.ILT_SESSION + '/' + session_name, json=user_input)

  if ilt_session.status_code == 200:
    flash('Data sesi ILT telah diupdate!', 'success')
    return redirect(url_for('admin_ilt_session'))
  elif ilt_session.status_code == 404:
    flash('Data sesi ILT tersebut tidak tersedia!', 'danger')
    return redirect(url_for('admin_ilt_session'))
  else:
    return redirect(url_for('admin_ilt_session'))

@app.route('/admin/ilt-session/delete/<string:session_name>', methods=['GET'])
def delete_ilt_session(session_name):
  ilt_session = requests.delete(config.ILT_SESSION + '/' + session_name)

  if ilt_session.status_code == 204:
    flash('Data sesi ILT telah dihapus!', 'success')
    return redirect(url_for('admin_ilt_session'))
  elif ilt_session.status_code == 404:
    flash('Data sesi ILT tersebut tidak tersedia!', 'danger')
    return redirect(url_for('admin_ilt_session'))
  else:
    return redirect(url_for('admin_ilt_session'))

@app.route('/admin/ilt-feedback', methods=['GET'])
def admin_ilt_feedback():
  ilt_feedback = requests.get(config.ILT_FEEDBACK)
  response_ilt_feedback = ilt_feedback.json()
  return render_template('admin-ilt-feedback.html', ilt_feedback=response_ilt_feedback)

@app.route('/admin/ilt-feedback/delete/<string:data_id>', methods=['GET'])
def delete_ilt_feedback(data_id):
  ilt_feedback = requests.delete(config.ILT_FEEDBACK + '/' + data_id)

  if ilt_feedback.status_code == 204:
    flash('Data feedback ILT telah dihapus!', 'success')
    return redirect(url_for('admin_ilt_feedback'))
  elif ilt_feedback.status_code == 404:
    flash('Data feedback ILT tersebut tidak tersedia!', 'danger')
    return redirect(url_for('admin_ilt_feedback'))
  else:
    return redirect(url_for('admin_ilt_feedback'))

@app.route('/admin/ilt-feedback/csv', methods=['GET'])
def ilt_feedback_csv():
  ilt_feedback = requests.get(config.ILT_FEEDBACK_CSV)
  return Response(ilt_feedback.content, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=ilt_feedback.csv"})

@app.route('/admin/ilt-feedback/csv/ranged', methods=['POST'])
def ilt_feedback_ranged_csv():
  start_id = request.form['start-id']
  end_id = request.form['end-id']

  ilt_feedback = requests.get(config.ILT_FEEDBACK_CSV + '/' + start_id + '-' + end_id)
  return Response(ilt_feedback.content, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=ilt_feedback_ranged.csv"})