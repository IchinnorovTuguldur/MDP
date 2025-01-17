from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/portfolio')
@login_required
def portfolio():
    user = {
        'name': 'Ichinnorov Tuguldur',
        'email': 'ichinnorov.tuguldur99@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/ichinnorov-tuguldur/'
    }
    
    skills = ['Python', 'JavaScript', 'React', 'Node.js', 'Flask', 'PostgreSQL', 'MongoDB', 'Docker', 'AWS']

    experiences = [
        {
            'title': 'Machine Learning Data Specialist',
            'company': 'Amazon.com, Inc.',
            'location': 'Bellevue, WA',
            'date': 'Sep 2023 – Present',
            'details': [
                'Enhanced development processes through proactive problem-solving and knowledge-sharing, achieving a 20% reduction in bug resolution time and a 15% increase in team efficiency.',
                'Created comprehensive documentation detailing change logs, system requirements, performance metrics, and operational procedures. Ensured all stakeholders had access to critical information, facilitating smoother project management and enhancing team collaboration.',
                'Implemented robust data collection processes to track progress for multiple Alexa projects aimed at refining AI/ML model behind Alexa devices and improved entity detection by 20%.',
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'Cook Systems',
            'location': 'Remote - Memphis, TN',
            'date': 'Mar 2023 – Sep 2023',
            'details': [
                'Architected and implemented a robust web-based system capable of efficiently handling millions of daily requests, ensuring high availability and performance.',
                'Developed and maintained a scalable, cost-efficient, and distributed cloud-based infrastructure, optimizing resource utilization and reducing operational costs.',
                'Leveraged React to create dynamic user interfaces, significantly enhancing user engagement and application performance.'
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'Accenture PLC',
            'location': 'Seattle, WA',
            'date': 'May 2022 – Mar 2023',
            'details': [
                'Led the development of highly responsive and interactive web application using HTML, CSS, and JavaScript.',
                'Built fast-loading & stylish interactive Reports & Dashboards page using Node.js, JavaScript, Salesforce, SQL, and TypeScript for the multinational phone service provider.',
                'Enabled the client to deliver data-driven insights to over 10K users by implementing Graphs & Charts component using React under agile sprint methodology.',
                'Improved platform efficiency by 20% by implementing logic for data validation and bulk upload feature, collaborating with 25+ developers.'
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'Pinecone LLC',
            'location': 'Bellevue, WA',
            'date': 'Oct 2020 – May 2022',
            'details': [
                'Designed and implemented a robust cloud-based CI/CD pipeline for seamless continuous integration and deployment. Streamlined the development lifecycle, reducing deployment times by 40% and ensuring rapid delivery of high-quality software updates.',
                'Developed features for the Physics-Based Synthetic Data Generation project that allowed users to generate datasets using AI/ML in an agile SDLC.',
                'Improved the performance of the Real-time Data Migration project by 20% through developments such as Data Pipelines, REST APIs, and UI implementation.'
            ]
        }
    ]

    education = [
        {
            'degree': 'BSc in Computer Science',
            'institution': 'Central Washington University',
            'date': '2020 - 2023',
            'description': 'Focused on software development, algorithms, and machine learning.'
        }
    ]

    certifications = [
        {
            'title': 'AWS Certified Solutions Architect',
            'issuer': 'Amazon Web Services',
            'date': 'Nov 2021',
            'description': 'Validated expertise in designing and deploying scalable systems on AWS.'
        },
        {
            'title': 'Certified Kubernetes Administrator',
            'issuer': 'Cloud Native Computing Foundation',
            'date': 'Aug 2020',
            'description': 'Demonstrated proficiency in Kubernetes cluster management and orchestration.'
        }
    ]

    return render_template("portfolio.html", user=user, skills=skills, experiences=experiences, education=education, certifications=certifications)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)