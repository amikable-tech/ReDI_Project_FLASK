import datetime
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect, session
from flask_login import login_required, current_user
from .models import Admin, Appointment
from .forms import AppointmentForm
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/booking', methods=['GET', 'POST'])
def booking():
    form = AppointmentForm()
    if form.validate_on_submit():
        # Create a new appointment
        appointment = Appointment(
            name=form.name.data,
            email=form.email.data,
            date=form.date.data,
            time=form.time.data
        )

        # Save the appointment to the database
        db.session.add(appointment)
        db.session.commit()

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('views.booking'))

    return render_template('booking.html', form=form)



@views.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@views.route('/appointment')
@login_required
def appointment():
    # Retrieve all appointments from the database
    appointments = Appointment.query.all()

    return render_template('appointment.html', appointments=appointments)



@views.route('/admin/appointment/<int:appointment_id>/delete', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Delete the appointment from the database
    db.session.delete(appointment)
    db.session.commit()

    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('views.admin_dashboard'))