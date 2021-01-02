from dentalhcrm import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    referral = db.Column(db.String(60))
    gender = db.Column(db.Integer)
    year_of_birth = db.Column(db.Integer)
    medical_history = db.Column(db.Text)
    dental_history = db.Column(db.Text)
    notes = db.Column(db.Text)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointments = db.relationship('Appointment', cascade="all,delete", backref='patient')

    def __repr__(self):
        return f'[{self.id}] {self.name} {self.surname}'


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date = db.Column(db.DateTime)
    complaint = db.Column(db.String(512))
    treatment_plan = db.Column(db.String(512))
    actions_done = db.Column(db.String(512))
    advice = db.Column(db.String(512))
    next_visit = db.Column(db.String(512))
    transaction_notes = db.Column(db.String(512))
    cost = db.Column(db.Float)
    receipt = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __repr__(self):
        return f'[{self.id}] {self.user_id} {self.patient_id} {self.date}'