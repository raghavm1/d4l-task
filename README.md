# About

This is a REST API created using Flask. This application is developed using Python in MVC architecture.

## Setup

First, we need to install all dependencies.
In the root directory, run -
`pip install -r requirements.txt`

## Why a REST API?

As I was solving this problem, I realised how in a proper setting this can be advantageous as a REST API. Any kind of a frontend - be it a web app or a mobile app can be easily created and this API can be utilised to complete a fullstack application. Also, I added functionality to various endpoints via URL params because while I did my testing and debugging using Postman, this API can be used from any browser.

Apart from the requirements, I have added some extra endpoints like adding and removing doctor/patient details, since I could see the benefits of MVC in easily implementing it (separation of concerns and modularity make adding/removing/debugging features easy), and thought this would be a good exercise for me to apply it and learn more.

## Q1. Entities and Relations

Here, there are 3 entities -

1. Doctor
2. Patient
3. Appointment

While Doctor and Patient are kernels (strong independent entities), Appointment is a weak/dependent entity that requires the existence of both Doctor and Patient entities

Here, the Doctors work on/have appointments, and the working on/having is the relation
Similarly, patients attend to appointments to get cured.

There is a 1:M relationship between Doctors and Appointments, as well as Patient and appointments.

### Run the app

Run the command `python app.py` to get started. This will keep the application running on `localhost:5000`

## Using the app (Documentation)

This app has 13 endpoints in total.

URL parameters are used as follows-  

For example, getting appointments by doctor_name is done as `http://localhost:5000/api/get?name=<name>&date=<date>&entity_type=<entity_type>`

1. Getting all appointments

    `/api/all`
    This endpoint returns all appointments of all doctors and patients
    <br>

2. (Q2) Getting appointments by doctor name or patient name

    `/api/get`
    Returns appointments belonging to a specific patient or doctor on a given date

    - URL parameters
        - name
        - date
        - entity_type
    <br>

3. (Q3) Creating an appointment

    `/api/add`
    Creates an appointment with a doctor given the doctor's name, patient name, date and time

    - URL parameters
        - date
        - time
        - doctor_name
        - patient_name
    <br>

4. (Q4) Cancelling an appointment

    `/api/cancel`
    Cancels an existing appointment of a doctor or a patient. Can be triggered either as a doctor or as a patient. 
    - URL parameters
        - doctor_name _(optional if patient_name is given)_
        - patient_name _(optional if doctor_name is given)_
        - date (in YYYY-MM-DD format)
        - time (in HH-MM-00 format)
    <br>
5. Fetch appointments by either doctor or patient ID

    `/api/get_by_id`
    - URL parameters
        - date
        - id
        - entity_type
    <br>
6. Get all doctor details by ID

    `/api/get/doctor`
    - URL parameters
        - id
    <br>
7. Add a new doctor 

    `/api/add/doctor`
    - URL parameters
        - name
    <br>
8. Delete doctor by ID

    `/api/delete/doctor`
    - URL parameters
        - id
    <br>
9. Get patient details by ID

    `/api/get/patient`
    - URL parameters
        - id
    <br>
10. Add patient

    `/api/add/patient`
    - URL parameters
        - name
        - gender
        - age
    <br>
11. Delete patient

    `/api/delete/patient`
    - URL parameters
        - id
    <br>
12. View all doctors
    `/api/get/doctors`
    <br>
13. View all patients
    `/api/get/patients`


### Possible further improvements

- Currently appointment details can be retrieved by name instead of ID. It was done this way to make the program more user-friendly or if IDs are just for DB's primary key purpose, and if this product is client-facing. However, if one would use this API as an admin, retreival by ID would be better. To showcase this, I have retreived all patient and doctor details via IDs only, since these can be typically tasks done by an administrator and not a general user.
Another way of having useful IDs could be like a person having NRICs or FINs for identification. In that case, using IDs can be better even in client-facing apps.

- Having a DB or dataframes for facilitating quick retrieval when filtering patient/doctor details. (use of dataframes is done on the df-approach branch)
