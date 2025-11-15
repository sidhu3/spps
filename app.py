from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
import pickle
import pandas as pd
from markupsafe import Markup


app = Flask(__name__)

#Database
db=SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

with app.app_context():
    db.create_all() 

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'  # View to redirect unauthorized users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin role
    reset_token = db.Column(db.String, nullable=True)  # For password reset


class PredictedPerformance(db.Model):
    __tablename__ = 'predicted_performance'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    hours_studied = db.Column(db.Float, nullable=False)
    attendance_percentage = db.Column(db.Float, nullable=False)
    assignments_submitted = db.Column(db.Integer, nullable=False)
    previous_grades = db.Column(db.Float, nullable=False)
    predicted_score = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    pass_fail = db.Column(db.String(10), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = "login" 
# Optional: Customize the unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the login page
    return redirect(url_for('login')) 


# ADMIN USER
# from werkzeug.security import generate_password_hash
# with app.app_context():
#     hashed_password = generate_password_hash('sidhu@1212')  
#     admin_user = User(
#         username='admin',
#         password=hashed_password,
#         firstname='siddhu',
#         lastname='mallah',
#         email='sahanisidhu123@gmail.com.com',
#         is_admin=True
#     )
#     db.session.add(admin_user)
#     db.session.commit()
#     print(f"Admin {admin_user.username} created successfully!")

from flask import abort
from functools import wraps
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            abort(403)  
        return f(*args, **kwargs)
    return decorated_function    


from werkzeug.security import check_password_hash
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('uname')
        pwd = request.form.get('upassword')
        user = User.query.filter_by(username=name).first()

        if user and check_password_hash(user.password, pwd):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Invalid username or password!')
            return redirect('/login')
    return render_template('login.html')
            

from werkzeug.security import generate_password_hash
@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
    if request.method == 'POST':
        name = request.form.get('uname')
        pwd = request.form.get('upassword')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')

        hashed_pwd = generate_password_hash(pwd)  # Hash the password here

        user = User(username=name, password=hashed_pwd, firstname=fname, lastname=lname, email=email)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html')



@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')   


import secrets
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            user.reset_token = secrets.token_urlsafe(16)  # Generate reset token
            db.session.commit()
            reset_url = url_for('reset_password', token=user.reset_token, _external=True)
            # Include HTML in the flash message
            flash(Markup(f'Reset link sent to {email}: <a href="{reset_url}">{reset_url}</a>'), 'info')
        else:
            flash('Email not found!', 'error')
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        flash('Invalid or expired token!', 'error')
        return redirect('/forgot-password')

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password) # Hash the new password
        user.reset_token = None  # Clear reset token
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html',token=token) # Pass the token
                

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    users = User.query.filter(User.username != 'admin').all()
    return render_template('admin_panel.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_panel'))


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def temp_view():
    return render_template('home.html')

@app.route('/km')
def know_more():
    return render_template('knowmore.html')

@app.route('/sd')
@login_required
def student_detail():
    return render_template('student_detail.html', current_route = 'prediction')

# Function to predict grade based on performance score
def predict_grade(performance_score):
    if performance_score >= 90:
        return 'A+'
    elif performance_score >= 80:
        return 'A'
    elif performance_score >= 70:
        return 'B+'
    elif performance_score >= 60:
        return 'B'
    elif performance_score >= 50:
        return 'C'
    elif performance_score >= 40:
        return 'D'
    else:
        return 'F'

# Function to predict pass/fail status
def predict_pass_fail(performance_score):
    if performance_score >= 40:
        return 'Pass'
    else:
        return 'Fail'


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Get values from the form
        student_name = request.form['student_name']
        roll_no = request.form['roll_no']
        hours_studied = float(request.form['hours_studied'])
        attendance_percentage = float(request.form['attendance_percentage'])
        assignments_submitted = float(request.form['assignments_submitted'])
        previous_grades = float(request.form['previous_grades'])

        # Prepare input data with feature names for prediction
        features = ['hours_studied', 'attendance_percentage', 'assignments_submitted', 'previous_grades']
        input_data = pd.DataFrame([[
            hours_studied,
            attendance_percentage,
            assignments_submitted,
            previous_grades
        ]], columns=features)

        # Predict the performance score
        prediction = model.predict(input_data)
        prediction = max(0, min(100, prediction[0]))

        # Predict grade and pass/fail status
        grade = predict_grade(prediction)
        pass_fail = predict_pass_fail(prediction)

        # Save to the database
        predicted_data = PredictedPerformance(
            student_name=student_name,
            roll_no=roll_no,
            hours_studied=hours_studied,
            attendance_percentage=attendance_percentage,
            assignments_submitted=assignments_submitted,
            previous_grades=previous_grades,
            predicted_score=prediction,
            grade=grade,
            pass_fail=pass_fail
        )
        db.session.add(predicted_data)
        db.session.commit()

        student_data={
                'previousGrades': previous_grades,
                'predictedScore': round(prediction, 2),
                'attendance': attendance_percentage,
                'hoursStudied': hours_studied,
                'assignmentsSubmitted': assignments_submitted
            }

        return render_template('result.html', prediction=round(prediction, 2), grade=grade, pass_fail=pass_fail,student=student_data, student_name=student_name)

    except Exception as e:
        return f"Error: {e}"


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Start with a query object
    query = PredictedPerformance.query

    # Get filter values and page number from request arguments
    min_score = request.args.get('min_score')
    max_score = request.args.get('max_score')
    grade_filter = request.args.get('grade')
    pass_fail_filter = request.args.get('pass_fail')
    page = int(request.args.get('page', 1))  # Default to page 1

    # Apply each filter conditionally
    if min_score:
        query = query.filter(PredictedPerformance.predicted_score >= float(min_score))
    if max_score:
        query = query.filter(PredictedPerformance.predicted_score <= float(max_score))
    if grade_filter:
        query = query.filter(PredictedPerformance.grade == grade_filter)
    if pass_fail_filter:
        query = query.filter(PredictedPerformance.pass_fail == pass_fail_filter)

    # Pagination logic
    per_page = 10  # Records per page
    paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'dashboard.html',
        data=paginated_data.items,
        page=page,
        per_page=per_page,
        total_pages=paginated_data.pages,
        min_score=min_score,
        max_score=max_score,
        grade_filter=grade_filter,
        pass_fail_filter=pass_fail_filter,
        current_route = 'dashboard'
    )


@app.route('/student/<int:id>', methods=['GET'])
@login_required
def student_info(id):
    student = PredictedPerformance.query.get_or_404(id)
    return render_template('student_info.html', student=student)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_record(id):
    record = PredictedPerformance.query.get_or_404(id)

    if request.method == 'POST':
        # Update fields from the form
        record.student_name = request.form['student_name']
        record.roll_no = request.form['roll_no']
        record.hours_studied = float(request.form['hours_studied'])
        record.attendance_percentage = float(request.form['attendance_percentage'])
        record.assignments_submitted = float(request.form['assignments_submitted'])
        record.previous_grades = float(request.form['previous_grades'])

        # Prepare input data with feature names for prediction
        features = ['hours_studied', 'attendance_percentage', 'assignments_submitted', 'previous_grades']
        input_data = pd.DataFrame([[
            record.hours_studied,
            record.attendance_percentage,
            record.assignments_submitted,
            record.previous_grades
        ]], columns=features)

        # Recalculate prediction
        prediction = model.predict(input_data)
        prediction = max(0, min(100, prediction[0]))  

        # Update grade and pass/fail status
        record.predicted_score = prediction
        record.grade = predict_grade(prediction)
        record.pass_fail = predict_pass_fail(prediction)

        # Save changes to the database
        db.session.commit()
        flash('Record updated successfully!', 'success')
        return redirect('/dashboard')

    return render_template('update.html', record=record)


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_record(id):
    record = PredictedPerformance.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!', 'danger')
    return redirect('/dashboard')

@app.route('/help')
def help_view():
    return render_template('help.html', current_route='help')  

@app.after_request
def add_header(response):
    # Prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)