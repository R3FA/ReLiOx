# Backend and Frontend Setup Guide

## Backend Setup

Follow these steps to set up and run the backend:

### Step 1: Navigate to the Backend Folder
Open your terminal or command prompt and run:
```sh
cd Backend
```
This will move you into the backend folder.

### Step 2: Create a Virtual Environment
To create a virtual environment, run the following command:

- **For Windows:**
  ```sh
  py -m venv .venv
  ```
- **For Linux / Mac OS:**
  ```sh
  python3 -m venv .venv
  ```

This step creates a `.venv` (virtual environment), which helps isolate the backend dependencies from the global Python libraries.

### Step 3: Activate the Virtual Environment
Activate the virtual environment by running:

- **For Windows:**
  ```sh
  source .venv\Scripts\activate
  ```
- **For Linux / Mac OS:**
  ```sh
  source .venv/bin/activate
  ```

Activating the virtual environment ensures that dependencies are installed and used from within `.venv`.

### Step 4: Install Required Dependencies
Run the following command to install all necessary dependencies:
```sh
pip install -r requirements.txt
```

### Step 5: Run Database Migration
This step creates the database instance, tables, and inserts 300,000 records, which will be used by the agent for learning. Additionally, a trained model will be generated and saved as `trained-model.sav`.

Run the migration command:
- **For Windows:**
  ```sh
  py migration.py
  ```
- **For Linux / Mac OS:**
  ```sh
  python3 migration.py
  ```

After a successful migration, the terminal should display a confirmation message indicating that the database, tables, and agent data have been created.

### Step 6: Start the Backend Server
Run the following command to start the backend:
- **For Windows:**
  ```sh
  py main.py
  ```
- **For Linux / Mac OS:**
  ```sh
  python3 main.py
  ```

Upon successful execution, the terminal will confirm that the backend is running properly.

---

## Frontend Setup

### Prerequisite: Install Node.js
Ensure that Node.js is installed on your system before proceeding.

### Step 1: Install Angular CLI
Run the following command to install Angular CLI globally:
```sh
npm install -g @angular/cli@19.2.4
```
This command installs Angular version `19.2.4`, which is required for the ReLiOx – Gaming Session Manager project.

### Step 2: Navigate to the Frontend Folder
Move to the frontend folder by running:
```sh
cd Frontend
```

### Step 3: Install Required Dependencies
Run the following command to install all required frontend dependencies:
```sh
npm install
```
Once the dependencies are installed successfully, the terminal will display an output confirming the installation.

### Step 4: Start the Frontend Server
Run the following command to start the frontend:
```sh
ng serve
```

After running this command, the frontend should start successfully, and the terminal should confirm that the application is running.

---

## Troubleshooting
If you encounter any errors during setup, ensure that:
- All required dependencies are installed.
- The virtual environment is activated before running backend commands.
- Node.js is installed and the correct version of Angular CLI is used.

If issues persist, check the error messages in the terminal and resolve any missing dependencies accordingly.

---

This guide provides step-by-step instructions to set up and run the backend and frontend for the project successfully.
