from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, TextAreaField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from dentalhcrm.member.models import Patient
from datetime import datetime


class PatientForm(FlaskForm):
    id = IntegerField('ID')
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])
    referral = StringField('Referral', validators=[Length(max=60)])
    year_of_birth = IntegerField('Year')
    age = IntegerField('Age')
    gender = SelectField('Gender', choices=[('empty', 'gender'), ('male', 'male'), ('female', 'female'), ('other', 'other')])
    medical_history = TextAreaField('Medical history', validators=[Length(max=300)])
    dental_history = TextAreaField('Dental history', validators=[Length(max=300)])
    notes = TextAreaField('Notes', validators=[Length(max=300)])
    phone_number = StringField('Phone number', validators=[Length(max=20)])
    email = StringField('Email', validators=[])
    address = StringField('Address', validators=[Length(max=50)])
    
    # Submit
    submit = SubmitField('Save')

    #
    # Validations
    #
    def validate_phone_number(form, field):

        if field.data:
            if not field.data.isdigit():
                raise ValidationError('Phone number is invalid')
            
            if len(field.data) != 10:
                raise ValidationError('Invalid phone number length')


    def validate_age(form, field):
        min_age = 0
        max_age = 120

        if field.data:
            if not isinstance(field.data, int):
                raise ValidationError('Age should be integer')
            
            if field.data < min_age or field.data > max_age:
                raise ValidationError('Invalid age')
            

    def validate_year_of_birth(form, field):
        min_age = 0
        max_age = 120

        if field.data:
            if not isinstance(field.data, int):
                raise ValidationError('Year of birth should be integer')
            
            year_entered = field.data
            current_year = datetime.now().year

            if year_entered < current_year - max_age or year_entered > current_year:
                raise ValidationError('Invalid age')


class AppointmentForm(FlaskForm):
    # Appointment fields
    id = IntegerField('ID')
    date = DateField('Date', validators=[DataRequired()], 
        format="%Y-%m-%d",
        default=datetime.today,)
    complaint = TextAreaField('Complaint', validators=[Length(max=300)])
    treatment_plan = TextAreaField('Treatment Plan', validators=[Length(max=300)])
    actions_done = TextAreaField('Actions Done', validators=[Length(max=300)])
    advice = TextAreaField('Advice', validators=[Length(max=300)])
    next_visit = TextAreaField('Next Visit', validators=[Length(max=300)])
    transaction_notes = TextAreaField('TransTransaction Notes', validators=[Length(max=300)])
    cost = DecimalField('Cost', places=2, rounding=None)
    receipt = DecimalField('Receipt', places=2, rounding=None)
    
    # Relationship(s)
    patient_id = IntegerField('Patient ID')
    user_id = IntegerField('User ID')
    
    # Joined non-editable fields
    name = StringField('Name')
    surname = StringField('Surname')
    medical_history = TextAreaField('Medical History')
    dental_history = TextAreaField('Dental History')
    notes = TextAreaField('Notes')

    # Submit
    submit = SubmitField('Save')

    # 
    # Validations
    #
    def validate_date(form, field):
        if (field.data.year < 2020) or (field.data.year > 2050):
            raise ValueError('Date is incorrect')
        

    def validate_cost(form, field):
        try:
            if field.data < 0:
                raise ValueError('Cost must be positive')
        except:
            raise ValueError('')


    def validate_receipt(form, field):
        try:
            if field.data < 0:
                raise ValueError('Receipt must be positive')
        except:
            raise ValueError('')