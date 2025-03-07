# LTI Integration Testing Guide

This guide provides step-by-step instructions for testing the LTI integration with Moodle. You can test using a local Docker environment or an external Moodle instance.

---

## 1. Testing LTI Integration with Moodle Using Docker Locally

### 1.1 Start Moodle and Required Services
Launch Moodle and its dependencies (PostgreSQL, Learning Record Store) with:
```sh
docker-compose -f docker-compose-with-local-docker-LMS.yml up
```
This starts all necessary services except Django.

### 1.2 Install Django Dependencies
Navigate to your Django application directory (e.g., `analyticDashboardDjangoApp`) and install dependencies:
```sh
pip install -r requirements.txt
```

### 1.3 Start the Django Development Server
Run the Django server in a new terminal:
```sh
python3 manage.py runserver 0.0.0.0:8000
```
Ensure the database settings in `settings.py` use `"localhost"` as the host.

### 1.4 Apply Database Migrations
Update the database schema with:
```sh
python manage.py migrate
```

### 1.5 Save Data in Database
- The database must contain **user emails** for authentication.
- Use the `save_data_in_lrs.py` script in `xapi/` to store xAPI statements.
- Generate new data using `main.py`, ensuring paths are correctly set in `save_data_in_lrs.py`.
- Generated user emails will be stored in `user_mails.txt`. Use these emails when creating user accounts.

**Instructor Emails:**
- `instructor1@example.com`
- `instructor2@example.com`
- `instructor3@example.com`

### 1.6 Access Moodle
Moodle is available at [http://localhost:8081](http://localhost:8081).

**Login Credentials:**
- **Username:** `user`
- **Password:** `bitnami`

### 1.7 Configure the LTI Tool in Moodle
1. Navigate to **Site Administration > Plugins > Manage Tools**.
2. Select **Configure a Tool Manually** and enter the following details:
   - **Tool Name:** Adaptive Analytic Dashboard
   - **Tool URL:** `http://localhost:8000/lti/launch/`
   - **LTI Version:** LTI 1.3
   - **Public Key Type:** Keyset URL
   - **Keyset URL:** `http://localhost:8000/lti/jwks/`
   - **Initiate Login URL:** `http://localhost:8000/lti/login/`
   - **Redirection URIs:** `http://localhost:8000/lti/launch/`
   - **Tool Configuration Usage:** Show in activity chooser and as a preconfigured tool.
   - **Supports Deep Linking:** Yes

**Privacy Settings:**
- **Share launcher’s name with tool:** Always
- **Share launcher’s email with tool:** Always

Save the configuration.

### 1.8 Create and Test a Course in Moodle
1. Navigate to **Site Administration > Courses > Add a New Course**.
2. Fill in course details and save.
3. Go to **My Courses**, select the new course, and enable **Edit Mode**.
4. Under **More > LTI External Tools**, verify that **Adaptive Analytics Dashboard** is available.
5. Add the tool as an **activity/resource** in your course.

### 1.9 User Creation in Moodle
1. Navigate to **Site Administration > Users > Add a New User**.
2. Use the emails stored in `user_mails.txt`.
3. Fill in the required details.
4. Save the new user.
5. Assign the user to a course.

### 1.10 Add Users to the Course
1. In your course, go to **Participants**.
2. Click **Enrol Users**.
3. Assign the appropriate role:
   - **Teacher** for instructors
   - **Student** for learners
4. Confirm the enrolment.

### 1.11 Verify Deployment ID and Client ID
1. Navigate to **Manage Tools** in Moodle.
2. Click **Tool Configuration Details** to find the **Client ID** and **Deployment ID**.
3. Update the configuration file located at:
```sh
analyticDashboardDjangoApp/configs/config.json
```
4. Example snippet:
```json
"http://localhost:8081": [{ "default": false, "client_id": "aX2hJ5kFnsptQj", "auth_login_url": "http://localhost:8081/mod/lti/auth.php", "auth_token_url": "http://localhost:8081/mod/lti/token.php", "key_set_url": "http://localhost:8081/mod/lti/certs.php", "deployment_ids": ["2"] }]
```
5. Save the changes.

---

## 2. Testing LTI Integration with an External Moodle Instance

### 2.1 Start the Django Server
Run the necessary backend services:
```sh
docker-compose up
```
Ensure `settings.py` is configured to use `"postgresdb"` as the database host.

### 2.2 Set Up the Database and Initialize Django
Apply migrations:
```sh
./run migrate
```
or inside the backend container:
```sh
python manage.py migrate
```

### 2.3 Configure the LTI Tool in Moodle
Follow the same setup steps as in **1.7**

### 2.4 Verify Deployment and Client ID
Ensure the **Client ID** and **Deployment ID** match the Moodle settings and update `config.json` accordingly.

### 2.5 Test the Integration
1. Create a Moodle course.
2. Add the **Adaptive Analytics Dashboard** as an activity.
3. Verify that the tool launches correctly.

---

## 3. Conditions for Using the Tool

### 3.1 Tracking Course Progress with xAPI Statements
- Each sub-course must send at least **one xAPI statement**.
- Every xAPI statement must include the **parent course** in context.
- xAPI statements should be sent to the **Learning Record Store (LRS)**.
- Sub-courses can be updated but can only be removed if their corresponding xAPI statements are deleted from the LRS.

### 3.2 Using the Tool as an Instructor
- To enable instructor functionality, include the instructor’s email in the xAPI statement context.

---

