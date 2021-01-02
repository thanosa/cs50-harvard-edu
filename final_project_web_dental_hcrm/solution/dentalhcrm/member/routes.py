from flask import render_template, url_for, redirect, abort, request, flash, Blueprint
from flask_login import login_required, current_user
from dentalhcrm import db
from dentalhcrm.member.forms import PatientForm, AppointmentForm
from dentalhcrm.member.models import Patient, Appointment
from dentalhcrm.errors.handlers import apology
from datetime import datetime


member = Blueprint('member', __name__)


@member.route("/member/home")
@login_required
def home():
    return render_template('member/home.html', title="Home", username=current_user.username)


@member.route("/member/patients/all", methods=['GET'])
@login_required
def patients_all():
    if request.method == 'GET':
        patients = Patient.query.filter(Patient.user_id == current_user.id).all()
        return render_template('member/patients_list.html', title="Patients", patients=patients)


@member.route("/member/patients/add", methods=['GET', 'POST'])
@login_required
def add_patient():

    form = PatientForm()
    
    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data,
            surname=form.surname.data,
            referral=form.referral.data,
            gender=form.gender.data,
            year_of_birth=form.year_of_birth.data,
            medical_history=form.medical_history.data,
            dental_history=form.dental_history.data,
            notes=form.notes.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            address=form.address.data,
            user_id=current_user.id)

        db.session.add(patient)
        db.session.commit()
        flash(f'Patient added with ID: {patient.id}')
        return redirect(url_for('member.patients_all'))
    else:
        return render_template('member/patient_card.html', title="Add Patient", form=form, delete_button=False)


@member.route("/member/patients/<int:patient_id>/update", methods=['GET', 'POST'])
@login_required
def update_patient(patient_id):

    # Validate the patient
    patient = Patient.query.get_or_404(patient_id)
    
    # Checks if the patient belongs to the current user.
    if patient.user_id != current_user.id:
        abort(404)

    form = PatientForm()
    if form.validate_on_submit():

        patient.name = form.name.data
        patient.surname = form.surname.data
        patient.referral = form.referral.data
        patient.gender = form.gender.data
        patient.year_of_birth = form.year_of_birth.data
        patient.medical_history = form.medical_history.data
        patient.dental_history = form.dental_history.data
        patient.notes = form.notes.data
        patient.phone_number = form.phone_number.data
        patient.email = form.email.data
        patient.address = form.address.data

        db.session.commit()
        flash(f'Patient ({patient.id}) {patient.name} {patient.surname} has been updated', 'success')
        return redirect(url_for('member.patients_all'))

    elif request.method == 'GET':
        
        age = None
        if len(str(patient.year_of_birth)) > 0:
            if isinstance(patient.year_of_birth, int):
                age = (datetime.now().year - patient.year_of_birth)

        form.id.data = patient.id
        form.name.data = patient.name
        form.surname.data = patient.surname
        form.referral.data = patient.referral
        form.gender.data = patient.gender
        form.year_of_birth.data = patient.year_of_birth
        form.age.data = age
        form.medical_history.data = patient.medical_history
        form.dental_history.data = patient.dental_history
        form.notes.data = patient.notes
        form.phone_number.data = patient.phone_number
        form.email.data = patient.email
        form.address.data = patient.address

    return render_template('member/patient_card.html', title='Update patient',
                           form=form, legend='Update patient', delete_button=True)


@member.route("/member/patients/<int:patient_id>/delete", methods=['GET'])
@login_required
def delete_patient(patient_id):
    
    patient = Patient.query.get_or_404(patient_id)
    patient_details = f"{patient.name} {patient.surname} ({patient.id})"

    if patient.user_id != current_user.id:
        abort(404)

    db.session.delete(patient)
    db.session.commit()
    flash(f'Patient has been deleted: {patient_details}', 'success')
    return redirect(url_for('member.patients_all'))


@member.route("/member/patients/all/appointments/all", methods=['GET'])
@login_required
def patients_all_appointments():
    if request.method == 'GET':
        patients_subquery = db.session.query(Patient.id).filter(Patient.user_id == current_user.id).subquery()
        appointments = db.session.query(Appointment).filter(Appointment.patient_id.in_(patients_subquery)).order_by(Appointment.date.desc()).all()

        return render_template('member/appointments_list.html', title="Appointments", appointments=appointments)


@member.route("/member/patients/<int:patient_id>/appointments/all", methods=['GET'])
@login_required
def patients_appointments(patient_id):
    if request.method == 'GET':
        patients = Patient.query.filter(Patient.user_id == current_user.id).filter(Patient.id == patient_id).all()
        if len(patients) == 0:
            abort(404)
        patient = Patient.query.get_or_404(patient_id)
        
        patient_subquery = db.session.query(Patient.id).filter(Patient.user_id == current_user.id).filter(Patient.id == patient_id).subquery()
        appointments = db.session.query(Appointment).filter(Appointment.patient_id.in_(patient_subquery)).order_by(Appointment.date.desc()).all()

        return render_template('member/patients_appointments.html', title="Appointments", patient=patient, appointments=appointments)


@member.route("/member/patients/<int:patient_id>/appointments/add", methods=['GET', 'POST'])
@login_required
def add_patients_appointment(patient_id):

    form = AppointmentForm()

    if form.validate_on_submit():
        appointment = Appointment(

            date=form.date.data,
            complaint=form.complaint.data,
            treatment_plan=form.treatment_plan.data,
            actions_done=form.actions_done.data,
            advice=form.advice.data,
            next_visit=form.next_visit.data,
            transaction_notes=form.transaction_notes.data,
            cost=form.cost.data,
            receipt=form.receipt.data,
            patient_id=patient_id,
            user_id=current_user.id
        )

        db.session.add(appointment)
        db.session.commit()
        flash(f'Appointment added for date: {appointment.date}')
        return redirect(url_for('member.patients_appointments', patient_id=patient_id))

    else:
        patient = Patient.query.get_or_404(patient_id)

        form.patient_id.data = patient_id
        form.name.data = patient.name
        form.surname.data = patient.surname
        form.medical_history.data = patient.medical_history
        form.dental_history.data = patient.dental_history
        
        return render_template('member/appointment_card.html', title="Add Appointment", form=form, delete_button=False)


@member.route("/member/appointments/<int:appointment_id>/update", methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):

    # Validate the appointment
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.user_id != current_user.id:
        print("Checks if the appointment belongs to the current user")
        print(f"appointment.patient.id: {appointment.patient.id}")
        print(f"current_user.id: {current_user.id}")
        abort(404)

    form = AppointmentForm()

    if form.validate_on_submit():

        appointment.date=form.date.data
        appointment.complaint=form.complaint.data
        appointment.treatment_plan=form.treatment_plan.data
        appointment.actions_done=form.actions_done.data
        appointment.advice=form.advice.data
        appointment.next_visit=form.next_visit.data
        appointment.transaction_notes=form.transaction_notes.data
        appointment.cost=form.cost.data
        appointment.receipt=form.receipt.data

        db.session.commit()
        flash(f'Appointment has been updated for date: {appointment.date}')
        return redirect(url_for('member.patients_appointments', patient_id=appointment.patient.id))

    else:

        form.id.data = appointment.id
        form.date.data = appointment.date
        form.complaint.data = appointment.complaint
        form.treatment_plan.data = appointment.treatment_plan
        form.actions_done.data = appointment.actions_done
        form.advice.data = appointment.advice
        form.next_visit.data = appointment.next_visit
        form.transaction_notes.data = appointment.transaction_notes
        form.cost.data = appointment.cost
        form.receipt.data = appointment.receipt
        form.patient_id.data = appointment.patient.id
        form.name.data = appointment.patient.name
        form.surname.data = appointment.patient.surname
        form.medical_history.data = appointment.patient.medical_history
        form.dental_history.data = appointment.patient.dental_history

        return render_template('member/appointment_card.html', title="Update Appointment", form=form, delete_button=True)


@member.route("/member/appointments/<int:appointment_id>/delete", methods=['GET'])
@login_required
def delete_patients_appointment(appointment_id):

    # Validate the appointment
    print(f"appointment_id: {appointment_id}")
    appointment = Appointment.query.get_or_404(appointment_id)

    patient_id = appointment.patient.id

    if appointment.user_id != current_user.id:
        print("Checks if the appointment belongs to the current user")
        print(f"appointment.patient.id: {appointment.patient.id}")
        print(f"current_user.id: {current_user.id}")
        abort(404)

    db.session.delete(appointment)
    db.session.commit()
    flash(f'Appointment deleted for date: {appointment.date}')
        
    return redirect(url_for('member.patients_appointments', patient_id=patient_id))
