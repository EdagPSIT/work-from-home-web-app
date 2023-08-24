from flask import Flask, render_template, request, redirect, url_for
from database import Session, WFHApplications, insert_wfh_application
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        emp_id = request.form['emp_id']
        wfh_date = datetime.datetime.strptime(request.form['wfh_date'], '%Y-%m-%d').date()

        insert_wfh_application(employee_name, emp_id, wfh_date)
        message = "Application submitted successfully!"
    
    return render_template('index.html', message=message)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    # Fetch only pending WFH applications from the database
    session = Session()
    applications = session.query(WFHApplications).filter_by(status='pending').all()
    session.close()

    if request.method == 'POST':
        application_id = int(request.form['application_id'])
        action = request.form['action']

        session = Session()
        application = session.query(WFHApplications).get(application_id)

        if action == 'approve':
            application.status = 'approved'
        elif action == 'reject':
            application.status = 'rejected'

        application.approval_date = datetime.datetime.now()
        session.commit()
        session.close()

        # Redirect back to the manager page
        return redirect(url_for('manager'))

    return render_template('manager.html', applications=applications)

# ... other code ...

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
