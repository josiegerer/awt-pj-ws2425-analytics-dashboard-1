LTI Integration Testing Guide

You can test the LTI integration with Moodle either by using Docker locally or by connecting to an external Moodle instance. Below are the steps for both methods:

1. Testing LTI Integration with Moodle Using Docker Locally

If you want to run Moodle locally using Docker, follow these steps:

1.1 Start Moodle and Required Services

Launch Moodle along with its dependencies, including PostgreSQL and the Learning Record Store, by running:

docker-compose -f docker-compose-with-local-docker-LMS.yml up

This starts Moodle and all necessary services except Django.

1.2 Install Django Dependencies

Navigate to your Django application directory (e.g., analyticDashboardDjangoApp) and install dependencies:

pip install -r requirements.txt

1.3 Start the Django Development Server

Run the Django server in a new terminal window:

python3 manage.py runserver 0.0.0.0:8000

Ensure that the database settings in settings.py use "localhost" as the host.

1.4 Apply Database Migrations

Update the database schema by executing:

python manage.py migrate

1.5 Access Moodle

Moodle will be available at http://localhost:8081.

Login credentials:

Username: user

Password: bitnami

1.6 Configure the LTI Tool in Moodle

Navigate to Site Administration > Plugins > Manage Tools.

Select Configure a Tool Manually and enter the following details:

Tool Name: Adaptive Analytic Dashboard

Tool URL: http://localhost:8000/lti/launch/

LTI Version: LTI 1.3

Public Key Type: Keyset URL

Keyset URL: http://localhost:8000/lti/jwks/

Initiate Login URL: http://localhost:8000/lti/login/

Redirection URIs: http://localhost:8000/lti/launch/

Tool Configuration Usage: Show in activity chooser and as a preconfigured tool.

Supports Deep Linking: Yes

Privacy Settings:

Share launcher’s name with tool: Always

Share launcher’s email with tool: Always

Save the configuration.

1.7 Create and Test a Course in Moodle

Navigate to Site Administration > Courses > Add a New Course.

Fill in the necessary course details and save.

Go to My Courses, select the newly created course, and enable Edit Mode.

Under More > LTI External Tools, ensure the Adaptive Analytics Dashboard is available.

Add the tool as an activity/resource in your course.

1.8 Add Users to the Course

In your course, go to Participants.

Click Enrol Users.

Select the appropriate role:

If the user is an instructor, choose Teacher.

If the user is a learner, choose Student.

Confirm the enrolment.

1.9 Verify Deployment ID and Client ID

Go to Manage Tools in Moodle.

Click Tool Configuration Details to find the Client ID and Deployment ID.

Update the configuration file located at:

analyticDashboardDjangoApp/configs/config.json

Example snippet:

"http://localhost:8081": [{
    "default": false,
    "client_id": "aX2hJ5kFnsptQj",
    "auth_login_url": "http://localhost:8081/mod/lti/auth.php",
    "auth_token_url": "http://localhost:8081/mod/lti/token.php",
    "key_set_url": "http://localhost:8081/mod/lti/certs.php",
    "deployment_ids": ["2"]
}]

Save the changes.

2. Testing LTI Integration with an External Moodle Instance

If you are using an external Moodle instance, follow these steps:

2.1 Start the Django Server

Run the necessary backend services using:

docker-compose up

Ensure settings.py is configured to use "postgresdb" as the database host.

2.2 Set Up the Database and Initialize Django

Run migrations:

./run migrate

or inside the backend container:

python manage.py migrate

2.3 Configure the LTI Tool in Moodle

Follow the same Moodle setup steps as in 1.6, ensuring URLs point to your external Django server (e.g., http://your-django-server:8000).

2.4 Verify Deployment and Client ID

Ensure that the Client ID and Deployment ID are correct in Moodle and update config.json accordingly.

2.5 Test the Integration

Create a course in Moodle.

Add the Adaptive Analytics Dashboard as an activity.

Verify that the tool launches correctly.

User Creation in Moodle

Navigate to Site Administration > Users > Add a New User.

Fill in the required user details.

Save the new user.

Assign the user to a course as described in 1.8 Add Users to the Course.

Conditions for Using the Tool

Tracking Course Progress with xAPI Statements

Each sub-course must send at least one xAPI statement.

Every xAPI statement must include the parent course as context.

xAPI statements should be sent to the Learning Record Store (LRS).

Sub-courses can be updated but can only be removed if their corresponding xAPI statements are deleted from the LRS. Otherwise, the course analytics will not show 100% completion.

Using the Tool as an Instructor

To enable instructor functionality, include the instructor’s email in the xAPI statement context.

Required Database Data and User Emails

The database must contain user emails for authentication.

Use the save_data_in_lrs.py script in xapi/ to store xAPI statements.

New data can be generated using main.py, but paths must be adjusted in save_data_in_lrs.py.

The generated user emails will be stored in user_mails.txt.
Use these emails when creating user accounts.

Instructor Emails:

instructor3@example.com

instructor1@example.com

instructor2@example.com