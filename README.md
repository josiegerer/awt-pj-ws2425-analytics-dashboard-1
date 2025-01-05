# AWT Project WS24/25: **Adaptive Learning Analytics Dashboard**

## **Project Overview**

The **Adaptive Learning Analytics Dashboard** is designed to provide valuable insights into the teaching and learning process. It aims to empower educators, administrators, and students by offering an interactive dashboard with the following features:

- **Track Key Learning Indicators:** Measure knowledge levels, learning progress, and learning needs.
- **Provide Actionable Recommendations:** Offer tailored recommendations to optimize learning outcomes based on user data.
- **Ensure Interoperability:** Adhere to industry standards to ensure smooth integration across various platforms.

The project will deliver a working prototype that equips stakeholders with data-driven insights to enhance the educational experience.

---

## **Setup and Requirements**

To set up and run the project, you can use **WSL (Windows Subsystem for Linux)** or **Ubuntu**. Additionally, you may use **Docker Desktop** for simplified management and containerized environments.

---

### **Running the Project**

1. **Start the Database and Backend Services:**

   Launch the necessary services for the database and backend by executing the following command:

   ```bash
   docker-compose up
   ```

2. **Set Up the Database and Initialize Django:**

   To configure the backend and create the necessary database tables, execute one of the following commands:

   - **Direct Command-Line Execution:**
     ```bash
     ./run migrate
     ```

   - **Within the Backend Container:**
     ```bash
     python manage.py migrate
     ```

---

### **Testing LTI Integration**

1. **Set Up Services:**

   - Start the PostgreSQL database and Learning Record Store (LRS) with the following command:
     ```bash
     docker-compose -f docker-compose-without-django.yml up
     ```

2. **Install Django Dependencies:**

   Navigate to the Django application directory (e.g., `analyticDashboardDjangoApp`) and install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Django Service:**

   To start the Django development server, run:

   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

   **Note:** You may need to update the database settings in the `settings.py` file to use the host `"localhost"`.

4. **Apply Database Migrations:**

   To ensure the database schema is up-to-date, run:

   ```bash
   python manage.py migrate
   ```

5. **Start the LMS (Moodle):**

   - Navigate to the Moodle directory and start the Moodle container with:
     ```bash
     docker-compose up
     ```

   - Access Moodle at: [localhost:8081](http://localhost:8081)
     - **Login credentials:**
       - **Username:** `user`
       - **Password:** `bitnami`

6. **Configure LTI Tool in Moodle:**

   - Go to **Site Administration** > **Plugins** > **Manage Tools**.
   - Select **Configure a Tool Manually** and enter the following details:

     - **Tool Name:** Adaptive Analytic Dashboard
     - **Tool URL:** `http://localhost:8000/lti/launch/`
     - **Tool Description:** [Add description here]
     - **LTI Version:** LTI 1.3
     - **Public Key Type:** Keyset URL
       - **Keyset URL:** `http://localhost:8000/lti/jwks/`
     - **Initiate Login URL:** `http://localhost:8000/lti/login/`
     - **Redirection URIs:** `http://localhost:8000/lti/launch/`
     - **Custom Parameters:** [Add if necessary]
     - **Tool Configuration Usage:** Show in activity chooser and as a preconfigured tool.
     - **Default Launch Container:** (Leave as default).
     - **Supports Deep Linking:** Yes
       - **Content Selection URL:** [Add URL if necessary]

   - **Privacy Settings:**
     - **Share launcher’s name with tool:** **Always**
     - **Share launcher’s email with tool:** **Always**

   - Save the configuration.

7. **Create and Test a Course in Moodle:**

   - Navigate to **My Courses** and create a course.
   - Enable **Edit Mode** and go to **More** > **LTI External Tools**.
   - Ensure the tool is visible in the activity chooser by enabling: **Show in Activity Chooser**.
   - Add the tool to your course as an activity or resource.

   To verify the deployment ID and client ID:

   1. Go to **Manage Tools** in Moodle.
   2. Click on **Tool Configuration Details** (represented by a magnifying glass with a plus).
   3. Check the **client ID** and **deployment ID** for accuracy.
   4. Open the configuration file located at:
   
      ```
      analyticDashboardDjangoApp/configs/config.json
      ```

   5. Locate the tool settings section:

      ```json
      "http://localhost:8081": [{
          "default": false,
          "client_id": "aX2hJ5kFnsptQj",
          "auth_login_url": "http://localhost:8081/mod/lti/auth.php",
          "auth_token_url": "http://localhost:8081/mod/lti/token.php",
          "key_set_url": "http://localhost:8081/mod/lti/certs.php",
          "key_set": null,
          "private_key_file": "private.key",
          "public_key_file": "public.key",
          "deployment_ids": ["2"]
      }]
      ```

   6. Update the **client_id** and **deployment_ids** to match the correct values from Moodle.
   7. Save the changes to the configuration file.

---

### **Database Interaction**

Use the following commands to interact with the project’s database:

```bash
<Insert specific database command here>
```

---

### **Backend Commands**

For backend operations, utilize the following commands as necessary:

```bash
<Insert backend command here>
```

--- 
