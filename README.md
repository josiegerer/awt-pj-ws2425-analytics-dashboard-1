### **LTI Integration Testing Guide**

You can test the LTI integration with Moodle either by **using Docker locally** or by **connecting to an external Moodle instance**. Below are the updated steps for both methods:

---

#### **1. Testing LTI Integration with Moodle Using Docker Locally**

If you'd like to run Moodle locally using Docker, follow the steps below:

1. **Start Services (Moodle and Dependencies):**
   Launch the necessary services, including the PostgreSQL database and Learning Record Store, using the following command:
   ```bash
   docker-compose -f docker-compose-with-local-docker-LMS.yml up
   ```
   This will start Moodle and all required services, excluding Django.

2. **Install Django Dependencies:**
   Navigate to your Django application directory (e.g., `analyticDashboardDjangoApp`) and install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Django Development Server:**
   In a new terminal window, start the Django server:
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```
   Ensure that the database settings in the `settings.py` file are configured to use `"localhost"` as the host.

4. **Apply Database Migrations:**
   Run the following command to update the database schema:
   ```bash
   python manage.py migrate
   ```

5. **Access Moodle:**
   Moodle is already running as part of the `docker-compose` setup. You can access Moodle at: [http://localhost:8081](http://localhost:8081)

   **Login credentials:**
   - **Username:** `user`
   - **Password:** `bitnami`

6. **Configure the LTI Tool in Moodle:**
   - Go to **Site Administration** > **Plugins** > **Manage Tools**.
   - Select **Configure a Tool Manually** and enter the following details:
     - **Tool Name:** Adaptive Analytic Dashboard
     - **Tool URL:** `http://localhost:8000/lti/launch/`
     - **LTI Version:** LTI 1.3
     - **Public Key Type:** Keyset URL
       - **Keyset URL:** `http://localhost:8000/lti/jwks/`
     - **Initiate Login URL:** `http://localhost:8000/lti/login/`
     - **Redirection URIs:** `http://localhost:8000/lti/launch/`
     - **Custom Parameters:** (Optional)
     - **Tool Configuration Usage:** Show in activity chooser and as a preconfigured tool.
     - **Supports Deep Linking:** Yes
   - **Privacy Settings:**
     - **Share launcher’s name with tool:** **Always**
     - **Share launcher’s email with tool:** **Always**
   - Save the configuration.

7. **Create and Test a Course in Moodle:**
   - Go to **My Courses**, create a new course, and enable **Edit Mode**.
   - Under **More** > **LTI External Tools**, verify that the Adaptive Analytics Dashboard tool is visible in the activity chooser.
   - Add the tool as an activity/resource in your course.

8. **Verify Deployment ID and Client ID:**
   - Go to **Manage Tools** in Moodle.
   - Click on **Tool Configuration Details** to view the **Client ID** and **Deployment ID**.
   - Open the configuration file located at:
     ```bash
     analyticDashboardDjangoApp/configs/config.json
     ```
   - Ensure the **client_id** and **deployment_ids** match the values from Moodle.

     Example configuration snippet:
     ```json
     "http://localhost:8081": [{
         "default": false,
         "client_id": "aX2hJ5kFnsptQj",
         "auth_login_url": "http://localhost:8081/mod/lti/auth.php",
         "auth_token_url": "http://localhost:8081/mod/lti/token.php",
         "key_set_url": "http://localhost:8081/mod/lti/certs.php",
         "deployment_ids": ["2"]
     }]
     ```

   - Save the changes to the `config.json` file.

---

#### **2. Testing LTI Integration with an External Moodle Instance**

For testing with an external Moodle instance (not using Docker locally), follow these steps:

1. **Start the Django Server:**
   Run the necessary backend services by executing `docker-compose up` (if not using Docker, set up the required services manually). Ensure that the database settings in `settings.py` are configured to use `"postgresdb"` as the host.

2. **Set Up the Database and Initialize Django:**
   If necessary, configure the backend and create the required database tables by executing the following command:
   - **Direct Command-Line Execution:**
     ```bash
     ./run migrate
     ```
   - **Within the Backend Container:**
     ```bash
     python manage.py migrate
     ```

3. **Configure the LTI Tool in Moodle:**
   - Access your external Moodle instance and follow the steps to configure the LTI tool.
   - Ensure that the **Tool URL**, **Keyset URL**, and **Redirection URIs** point to your online Django server (e.g., `http://your-django-server:8000`).

4. **Verify Deployment and Client ID:**
   - As in the local setup, confirm that the **Client ID** and **Deployment ID** are correctly configured in Moodle.
   - Update the `config.json` file with the correct values for **client_id** and **deployment_ids**.

5. **Test the Integration:**
   - After configuring the LTI tool in Moodle, create a course, add the Adaptive Analytics Dashboard as an activity, and verify that the integration is functioning as expected.

---

### **Frontend Testing**

For frontend testing, ensure that the user interface (UI) elements load properly and that interactions between the LTI tool and the Moodle instance are working as expected. Specifically, check the following:

- The LTI tool should launch correctly when accessed from within a Moodle course.
- Users should be correctly redirected to the appropriate dashboard.
- Course and user data should display in the dashboard if configured to do so.

## Conditions for using the Tool

You have to min. send one time each sub course as an xapi statement and give each xapi statement the parent class as context. With this you can track the progress of the cours. You have to send these xapi statements to the LRS. There are different methods for this (link).

To use the function for Instructors you have to send the instructor email as context.

Structure can update with new subcourses but subcourses can be just removed under the condition to delete each xapi statement in the lrs with the corresponding subcours. if not cours can be 100% in the analytics.

Problem where is information of whole Course