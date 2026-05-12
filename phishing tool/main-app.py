from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_sender import send_email

# =====================================================
# Flask Documentation Reference:
# https://flask.palletsprojects.com/en/stable/quickstart/
# =====================================================

# =====================================================
# CREATE FLASK APPLICATION
# Based on:
# https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
# =====================================================
app = Flask(__name__)

# =====================================================
# CONFIGURATION
# Based on Flask configuration examples
# https://flask.palletsprojects.com/en/stable/config/
# =====================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# INITIALIZE DATABASE
# Flask-SQLAlchemy Documentation:
# https://flask-sqlalchemy.palletsprojects.com/
# =====================================================
db = SQLAlchemy(app)

# =====================================================
# DATABASE MODEL
# =====================================================
class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        nullable=False
    )

    clicked_link = db.Column(
        db.Boolean,
        default=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

# =====================================================
# CREATE DATABASE TABLES
# =====================================================
with app.app_context():
    db.create_all()

# =====================================================
# HOME PAGE ROUTE
# Based on Flask Routing Documentation:
# https://flask.palletsprojects.com/en/stable/quickstart/#routing
# =====================================================
@app.route('/')
def index():
    return render_template('index.html')

# =====================================================
# SEND PHISHING EMAIL
# Uses Flask URL generation:
# https://flask.palletsprojects.com/en/stable/quickstart/#url-building
# =====================================================
@app.route('/send_phishing_email/<string:to_email>')
def send_phishing_email(to_email):

    subject = "Important Security Update"

    # Generate tracking URL
    tracking_link = url_for(
        'track_click',
        email=to_email,
        _external=True
    )

    # Render email template
    body = render_template(
        'phishing_email.html',
        link=tracking_link
    )

    try:
        # Send email
        send_email(to_email, subject, body)

        # Save interaction in database
        new_entry = UserInteraction(
            email=to_email,
            clicked_link=False
        )

        db.session.add(new_entry)
        db.session.commit()

        # Return JSON response
        # Based on:
        # https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
        return jsonify({
            "message": f"Simulation email sent to {to_email}",
            "tracking_link": tracking_link
        })

    except Exception as e:

        return jsonify({
            "message": "Failed to send email",
            "error": str(e)
        }), 500

# =====================================================
# TRACK EMAIL LINK CLICKS
# =====================================================
@app.route('/track/<string:email>')
def track_click(email):

    interaction = UserInteraction(
        email=email,
        clicked_link=True
    )

    db.session.add(interaction)
    db.session.commit()

    return render_template('thank_you.html')

# =====================================================
# REPORT DASHBOARD
# =====================================================
@app.route('/report')
def report():

    interactions = UserInteraction.query.order_by(
        UserInteraction.timestamp.desc()
    ).all()

    total_emails = len(interactions)

    total_clicks = len([
        interaction for interaction in interactions
        if interaction.clicked_link
    ])

    click_rate = 0

    if total_emails > 0:
        click_rate = round(
            (total_clicks / total_emails) * 100,
            2
        )

    return render_template(
        'report.html',
        interactions=interactions,
        total_emails=total_emails,
        total_clicks=total_clicks,
        click_rate=click_rate
    )

# =====================================================
# RUN APPLICATION
# Based on:
# https://flask.palletsprojects.com/en/stable/quickstart/#debug-mode
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)