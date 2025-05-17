from app import app, db, ExamSchedule

with app.app_context():
    records = ExamSchedule.query.all()
    for record in records:
        print(f"{record.id}: {record.course_name}, {record.course_code}, {record.batch}, {record.year}, {record.department}, "
              f"{record.start_time} - {record.end_time}, {record.hall_invigilator}, {record.hall_number}, "
              f"{record.start_roll_no}-{record.end_roll_no}, Total: {record.total_students}")
