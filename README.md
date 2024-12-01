# AWT Project WS24/25: Adaptive Learning Analytics Dashboard

## Project Overview

This project, developed as part of the AWT course for the WS24/25 academic year, aims to create an Adaptive Learning Analytics Dashboard. The primary objective is to design metrics and indicators that provide valuable insights for stakeholders involved in the teaching and learning process. These insights will cover aspects such as knowledge levels, learning progress, and learning needs. The project will culminate in a dashboard prototype that generates actionable instructions and recommendations based on these metrics, tailored to the user's context. Interoperable standards will be employed throughout the development.

---

## Setup and Requirements

To run the project, you can use either WSL (Windows Subsystem for Linux) or Ubuntu. For managing the commands, you can use the terminal in either environment or use Docker Desktop to execute Python commands.

### Running the Project

1. **Start the Database and Backend:**
   Use the following command to start both the database and the backend:
   ```bash
   docker-compose up
   ```

2. **Setting Up the Database and default functions of Django:**
   To initialize the backend and create necessary tables in the database, run:
   - On the command line:
     ```bash
     ./run migrate
     ```
   - Alternatively, you can go into the backend container and run:
     ```bash
     python manage.py migrate
     ```

---

## Usage Instructions

### Database

To interact with the database, use the following command:
```bash
<Insert specific command here>
```

### Backend

To start or use the backend, run the following:
```bash
<Insert specific command here>
```

---

This version organizes the content more clearly, uses consistent formatting, and provides a more user-friendly guide. Let me know if you need further adjustments!
