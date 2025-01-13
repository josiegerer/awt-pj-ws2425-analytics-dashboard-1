### **Testing LTI Integration**

You can test the LTI integration with Moodle either by **using Docker locally** or by **without using Docker** (using an external Moodle instance). Below are the steps for both approaches:

---

#### **1. Testing with Moodle Using Docker Locally**

If you prefer to run Moodle locally using Docker, follow these steps:

1. **Start Services:**
   Launch the necessary services (PostgreSQL database and Learning Record Store) by running:
   ```bash
   docker-compose -f docker-compose-with-local-docker-LMS.yml up
   ```

2. **Install Django Dependencies:**
   Navigate to your Django application directory (e.g., `analyticDashboardDjangoApp`) and install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Django Server:**
   In a separate terminal window, run the Django development server:
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```
   **Note:** Ensure that the database settings in `settings.py` are configured to use `"localhost"` as the host.

4. **Apply Database Migrations:**
   Run the following command to update the database schema:
   ```bash
   python manage.py migrate
   ```

5. **Start Moodle:**
   Navigate to the Moodle directory and start the Moodle container:
   ```bash
   docker-compose up
   ```
   Access Moodle at: [http://localhost:8081](http://localhost:8081)

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
     - **Custom Parameters:** [Optional]
     - **Tool Configuration Usage:** Show in activity chooser and as a preconfigured tool.
     - **Supports Deep Linking:** Yes
   - **Privacy Settings:**
     - **Share launcher’s name with tool:** **Always**
     - **Share launcher’s email with tool:** **Always**
   - Save the configuration.

7. **Create and Test a Course in Moodle:**
   - Go to **My Courses**, create a course, and enable **Edit Mode**.
   - Under **More** > **LTI External Tools**, verify that the Adaptive Analytics Dashboard tool is visible in the activity chooser.
   - Add the tool as an activity/resource to your course.

8. **Verify Deployment ID and Client ID:**
   - Go to **Manage Tools** in Moodle.
   - Click on **Tool Configuration Details** to view the **client ID** and **deployment ID**.
   - Open the configuration file located at:
     ```bash
     analyticDashboardDjangoApp/configs/config.json
     ```
   - Ensure that the **client_id** and **deployment_ids** match the values from Moodle.

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

#### **2. Testing with Moodle Without Docker (External Moodle Instance)**

If you're testing with an external Moodle instance (not using Docker locally), follow these steps:

1. **Start the Django Server:**
   Use `docker-compose up` to start the necessary backend services. Ensure that the database settings in `settings.py` are configured to use `"postgresdb"` as the host.

2. **Configure the LTI Tool in Moodle:**
   - Access your external Moodle instance and follow the steps to configure the LTI tool.
   - Ensure that the **Tool URL**, **Keyset URL**, and **Redirection URIs** point to your online Django server (e.g., `http://your-django-server:8000`).

3. **Check Deployment and Client ID:**
   - As in the local setup, confirm that the **client ID** and **deployment ID** are correctly configured in Moodle.
   - Update the `config.json` file with the correct values for **client_id** and **deployment_ids**.

4. **Test the Integration:**
   After configuring the LTI tool in Moodle, create a course, add the Adaptive Analytics Dashboard as an activity, and verify that the integration functions as expected.

---

### **Frontend Testing**

For frontend testing, ensure that the user interface (UI) elements load correctly and that the interactions between the LTI tool and the Moodle instance are working as expected. Check the following:

- The LTI tool should open successfully when launched from within a Moodle course.
- The user should be correctly redirected to the appropriate dashboard.
- Course and user data should display in the dashboard (if configured to pull such information).