# About

This is a REST API created using Flask. This application is developed using Python in the MVC framework.

## Setup

First, we need to install all dependencies.
In the root directory, run -
`pip install -r requirements.txt`

### Run the app

Run the command `python app.py` to get started. This will keep the application running on `localhost:5000`

## Using the app (Documentation)

This app has 4 endpoints in total -

1. Getting all appointments

    `/api/all`
    This endpoint returns all appointments of all doctors and patients
    <br>

2. Getting appointments by doctor name or patient name

    `/api/get`
    Returns appointments belonging to a specific patient or doctor on a given date

    - URL parameters
        - name
        - date
        - entity_type
    <br>

3. Creating an appointment

    `/api/add`
    Creates an appointment with a doctor given the doctor's name, patient name, date and time

    - URL parameters
        - date
        - time
        - doctor_name
        - patient_name
    <br>

4. Cancelling an appointment

    `/api/cancel`
    Cancels an existing appointment of a doctor or a patient. Can be triggered either as a doctor or as a patient. 
    - URL parameters
        - doctor_name _(optional if patient_name is given)_
        - patient_name _(optional if doctor_name is given)_
        - date (in YYYY-MM-DD format)
        - time (in HH-MM-00 format)
