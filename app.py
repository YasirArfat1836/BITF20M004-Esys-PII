from StudentInterests import  StudentInterests
from connection import Connection
from Model import Model
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify

app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key='Password@.com12345'
#connection functions my custom functions
conn = Connection('localhost', 'root', 'root', 'student_interest_system')
mydb = conn.MakeConnection()
model = Model()

def get_user_id_from_request(request):
    # Assuming you store user information in the session during authentication
    # Adjust this based on your actual authentication mechanism
    return session.get('user_id', None)
@app.route("/")
def home():
    return 'Welcome to Student Interests System'

@app.route('/login', methods=['POST'])
def login():
    # Handle user login
    user_id = get_user_id_from_request(request)
    model.log_user_activity(user_id, 'login', mydb)
    # ... (other login logic)
    return jsonify({'message': 'Login successful'})

@app.route('/add_record', methods=['POST'])
def add_record():
    # Handle adding a record
    user_id = get_user_id_from_request(request)
    model.log_user_activity(user_id, 'add_record', mydb)
    # ... (other add record logic)
    return jsonify({'message': 'Record added successfully'})
@app.route('/view_student/<int:student_id>',methods=['GET', 'POST'])
def view_student(student_id):
    if request.method=='GET':
        student_details=model.view_student(student_id,mydb)
        print(student_details)
        if student_details:
            return render_template('view_student.html', students=student_details)
    return "no data fetched"

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method=='POST':
        full_name = request.form['full_name']
        roll_number = request.form['roll_number']
        email_address = request.form['email_address']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        city = request.form['city']
        interest = request.form['interest']
        other_interest = request.form.get('otherInterest', '')
        department = request.form['department']
        degree_title = request.form['degree_title']
        subject = request.form['subject']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        if interest == 'Other':
            interest = other_interest
        student_interest = StudentInterests(
            full_name,
            roll_number,
            email_address,
            gender,
            date_of_birth,
            city,
            interest,
            department,
            degree_title,
            subject,
            start_date,
            end_date
        )
        insert = model.edit_student(student_id,student_interest, mydb)
        print(insert)
        if insert:
            flash("Student Edited  Successfully!!!", 'success')
            return render_template("flash.html")
        else:
            "some error"

    already_given_interests = model.AlreadyGivenInterests(mydb)
    return render_template('edit_student.html', interests=already_given_interests,student_id=student_id)

@app.route('/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    if request.method == 'GET':
        effected=model.delete_student(student_id,mydb)
        if effected:
            flash('Student deleted successfully', 'success')
            return render_template('flash.html')

@app.route("/ViewStudents",methods=['GET', 'POST'])
def StudentsList():
    if request.method == 'GET':
        result = model.AllStudents(mydb)
        if result:
            return render_template("ViewAllStudents.html", students=result)

    return "Invalid request"

@app.route('/Add', methods=['GET', 'POST'])
def AddStudents():

    if request.method == 'POST':
        full_name = request.form['full_name']
        roll_number = request.form['roll_number']
        email_address = request.form['email_address']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        city = request.form['city']
        interest = request.form['interest']
        other_interest = request.form.get('otherInterest', '')
        department = request.form['department']
        degree_title = request.form['degree_title']
        subject = request.form['subject']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        if interest == 'Other':
            interest = other_interest
        student_interest = StudentInterests(
            full_name,
            roll_number,
            email_address,
            gender,
            date_of_birth,
            city,
            interest,
            department,
            degree_title,
            subject,
            start_date,
            end_date
        )
        insert = model.AddStudents(student_interest,mydb)
        if insert:
            flash("Student with specified Data has been Added Successfully!!!", 'success')
            return render_template("flash.html")


    already_given_interests=model.AlreadyGivenInterests(mydb)
    return render_template('AddStudents.html',interests=already_given_interests)

# Flask route endpoint for provincial distribution
@app.route("/provincial_distribution", methods=['GET'])
def provincial_distribution():
    provincial_data = model.get_provincial_distribution(mydb)
    return jsonify({'data': provincial_data})


@app.route("/submission_chart_data", methods=['GET'])
def submission_chart_data():
    submission_data = model.get_daily_submission_counts(mydb)
    return jsonify({'data': submission_data})

@app.route("/age_distribution")
def age_distribution():
    age_distribution_data = model.get_age_distribution(mydb)
    return jsonify({'data':age_distribution_data})


@app.route('/department_distribution')
def department_distribution():
    department_distribution_data = model.get_department_distribution(mydb)
    return jsonify({'data': department_distribution_data})

@app.route('/degree_distribution')
def degree_distribution():
    degree_distribution_data = model.get_degree_distribution(mydb)
    return jsonify({'data': degree_distribution_data})

@app.route('/gender_distribution')
def gender_distribution():
    gender_distribution_data = model.get_gender_distribution(mydb)
    return jsonify({'data': gender_distribution_data})


@app.route('/last_30_days_activity')
def last_30_days_activity():
        activity_data = model.get_last_30_days_activity(mydb)
        return jsonify({'data': activity_data})

@app.route('/last_24_hours_activity')
def last_24_hours_activity():
        activity_data = model.get_last_24_hours_activity(mydb)
        return jsonify({'data': activity_data})

@app.route('/student_status')
def student_status():
    status_data = model.get_student_status(mydb)
    return status_data


@app.route('/most_active_hours')
def most_active_hours():
    try:
        activity_data = model.get_activity_by_hour(mydb)
        most_active_hours = [data['hour'] for data in activity_data if data['count'] > 0]
        return jsonify({'most_active_hours': most_active_hours})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/least_active_hours')
def least_active_hours():
    try:
        activity_data = model.get_activity_by_hour(mydb)
        least_active_hours = [data['hour'] for data in activity_data if data['count'] > 0][-5:]  # Adjust the number as needed
        return jsonify({'least_active_hours': least_active_hours})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dead_hours')
def dead_hours():
    try:
        activity_data = model.get_activity_by_hour(mydb)
        dead_hours = [data['hour'] for data in activity_data if data['count'] == 0]
        return jsonify({'dead_hours': dead_hours})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    top_interests_data = model.top_5(mydb)
    bottom_interests_data = model.bottom_5(mydb)
    interest_counts = model.interest_count(mydb)
    return render_template('dashboard.html', top=top_interests_data,bottom=bottom_interests_data,counts=interest_counts)


if __name__ == '__main__':
    app.run(debug=True)
