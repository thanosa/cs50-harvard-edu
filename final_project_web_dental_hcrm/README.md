The final project is a dentla healthcare CRM.

With this app a dentist can keep track of the appointments that have been done for their patients.

On the application there are mainly two areas. 
1. The public viewers are welcomed to register and uses the app 
2. The members area in where the registered user can manage their user account (login, logout, forgot password with secure token url sent to email, already have an account and remember me). Additionally, there has been added "maximum logins attended" to prevent any bruteforce password attacks.

As a member, the dentist can manage (add, update, delete) patient's profiles having information about: Name, Surname, Referral, Address, Phone, email, gender, year of birth / age, medical history and dental history. The user can either enter the year of birth or the age and the application will calculate the other one. The name and surname are the only mandatory fields for this entity.

For every patient, the dentist can manage (add, update, delete) their appointments by keeping information about their: Complaint, Treatment Plan, Actions Done, Advice, Next Visit, Transaction Notes, Appointment Date, Cost and Receipt. The Appointment Date is defaulted to the current date for convenience. There are validations on the cost and receipt fields and text limits to 300 characters.

The underlying technologies are: html, css, bootstrap, javascript, python, flask, flask-forms, Flask SQL-Alchemy and sqlite.
