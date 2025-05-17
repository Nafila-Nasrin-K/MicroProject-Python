from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ExamSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    course_code = db.Column(db.String(50))
    batch = db.Column(db.String(20))
    year = db.Column(db.String(10))
    department = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    hall_invigilator = db.Column(db.String(100))
    hall_number = db.Column(db.String(50))
    start_roll_no = db.Column(db.Integer)
    end_roll_no = db.Column(db.Integer)

    @property
    def total_students(self):
        return (self.end_roll_no - self.start_roll_no + 1) if self.start_roll_no and self.end_roll_no else 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_code = request.form['course_code']
        batch = request.form['batch']
        year = request.form['year']
        department = request.form['department']
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        hall_invigilator = request.form['hall_invigilator']
        hall_number = request.form['hall_number']
        start_roll_no = int(request.form['start_roll_no'])
        end_roll_no = int(request.form['end_roll_no'])

        schedule = ExamSchedule(
            course_name=course_name,
            course_code=course_code,
            batch=batch,
            year=year,
            department=department,
            start_time=start_time,
            end_time=end_time,
            hall_invigilator=hall_invigilator,
            hall_number=hall_number,
            start_roll_no=start_roll_no,
            end_roll_no=end_roll_no
        )

        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('result'))

    return render_template('form.html')


@app.route('/result')
def result():
    schedules = ExamSchedule.query.all()
    return render_template('result.html', schedules=schedules)


@app.route('/add')
def add_more():
    return redirect(url_for('index'))


@app.route('/delete/<int:exam_id>', methods=['POST'])
def delete_exam(exam_id):
    exam = ExamSchedule.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    return redirect(url_for('result'))


@app.route('/delete', methods=['POST'])
def delete_all():
    db.session.query(ExamSchedule).delete()
    db.session.commit()
    return redirect(url_for('result'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created or already exists.")
    app.run(debug=True)
