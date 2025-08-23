from flask import Flask, request, render_template
import csv

app = Flask(__name__)
CSV_FILE = 'students1.csv'

def load_students():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_students(students):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)

DISABLED_FIELDS = {
    "SNo", "Year of Joining", "Student Unique Enrolment ID","Name of the student", "Department",
    "Programme name","Present Year of Study", "Campus", "Name of the Mentor", "EMP ID"
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student')
def redirect_to_student():
    enrolment_id = request.args.get('id')
    return f'<script>window.location.href="/student/{enrolment_id}";</script>'

@app.route('/student/<enrolment_id>', methods=['GET', 'POST'])
def edit_student(enrolment_id):
    students = load_students()
    student = next((s for s in students if s['Student Unique Enrolment ID'] == enrolment_id), None)

    if request.method == 'POST' and student:
        for key in student:
            if key not in DISABLED_FIELDS:
                student[key] = request.form.get(key, student[key])
        save_students(students)
        return render_template('update_success.html')

    return render_template('edit_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
