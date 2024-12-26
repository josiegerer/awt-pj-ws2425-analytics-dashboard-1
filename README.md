# AWT Project WS24/25: Adaptive Learning Analytics Dashboard  

## **Project Overview**  

The **Adaptive Learning Analytics Dashboard** project, part of the AWT course for the WS24/25 academic year, aims to provide valuable insights into the teaching and learning process through an interactive dashboard. This dashboard will:  
- Measure key indicators like knowledge levels, learning progress, and learning needs.  
- Generate actionable recommendations tailored to user contexts.  
- Adhere to interoperable standards throughout development.  

The project will deliver a working prototype capable of empowering stakeholders with data-driven insights and recommendations.  

---

## **Setup and Requirements**  

The project can be run using **WSL (Windows Subsystem for Linux)** or **Ubuntu**. You may execute commands directly from the terminal in these environments or use **Docker Desktop** for easier management.  

---

### **Running the Project**  

1. **Start the Database and Backend:**  
   Launch both the database and backend services using:  
   ```bash  
   docker-compose up  
   ```  

2. **Set Up the Database and Initialize Django:**  
   To configure the backend and create necessary database tables, execute one of the following:  
   - **Direct command-line execution:**  
     ```bash  
     ./run migrate  
     ```  
   - **Within the backend container:**  
     ```bash  
     python manage.py migrate  
     ```  

---

### **Testing LTI Integration**  

1. **Set Up Services:**  
   - Start the PostgreSQL database and LRS (Learning Record Store) with:  
     ```bash  
     docker-compose -f docker-compose-without-django.yml up  
     ```  
   - Start the Django service separately in a terminal:  
     ```bash  
     python3 manage.py runserver 0.0.0.0:8000  
     ```  
     *Note:* You may need to update the database settings in `settings.py` to use the host `"localhost"`.  

2. **Apply Migrations:**  
   Run the following command to ensure the database schema is up-to-date:  
   ```bash  
   python manage.py migrate  
   ```  

3. **Start the LMS (Moodle):**  
   - Navigate to the LMS folder and start Moodle with:  
     ```bash  
     docker-compose up  
     ```  
   - Access Moodle at: [localhost:8081](http://localhost:8081)  
     - **Login credentials:**  
       - **Username:** `user`  
       - **Password:** `bitnami`  

4. **Configure LTI Tool in Moodle:**  
   - Go to **Site Administration** > **Plugins** > **Manage Tools**.  
   - Select **Configure a Tool Manually** and enter the following:  
     - **Tool Name:** Adaptive Analytic Dashboard  
     - **Tool URL:** `http://localhost:8000/lti/launch/`  
     - **Tool Description:**  
     - **LTI Version:** LTI 1.3  
     - **Public Key Type:** Keyset URL  
       - **Keyset URL:** `http://localhost:8000/lti/jwks/`  
     - **Initiate Login URL:** `http://localhost:8000/lti/login/`  
     - **Redirection URIs:** `http://localhost:8000/lti/launch/`  
     - **Custom Parameters:**  
     - **Tool Configuration Usage:** Show in activity chooser and as a preconfigured tool.  
     - **Default Launch Container:** (Leave as default).  
     - **Supports Deep Linking:** Yes  
       - **Content Selection URL:**  

   - **Privacy Settings:**  
     - Share launcher’s name with tool: **Always**  
     - Share launcher’s email with tool: **Always**  

   - Save the configuration.  

5. **Create and Test a Course in Moodle:**  
   - Go to **My Courses** and create a course.  
   - Enable **Edit Mode** and navigate to **More** > **LTI External Tools**.  
   - Ensure the tool is visible in the activity chooser by activating: **Show in Activity Chooser**.  
   - Add the tool to your course as an activity or resource.  

---

### **Database Commands**  

Use the following commands to interact with the database:  
```bash  
<Insert specific command here>  
```  

### **Backend Commands**  

To start or interact with the backend, use:  
```bash  
<Insert specific command here>  
```  

---

This version now includes the database migration step under **Testing LTI Integration** for clarity and completeness. Let me know if you need further refinements!  