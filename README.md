# OC-P12-CRM-EpicEvents


# Epic Events CRM

A customer relationship management (CRM) system for Epic Events, a company specializing in corporate event organization.

### 🔹 **Why Use Epic Events CRM?**
✅ Secure authentication with **JWT**  
✅ Fully featured **command-line interface (CLI)**  
✅ Tracks issues and errors in real-time using **Sentry**  
✅ Supports **PostgreSQL database** for reliable data storage  
✅ Integrated **role-based access control (RBAC):** Assign permissions according to user roles  

🚀 **Get started in minutes!** Follow the guide below to set up and start using the application.

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#application-commands)
- [Roles and Permissions](#roles-and-permissions)
- [Data Models](#data-models)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Error Monitoring](#error-monitoring)

## Project Overview

Epic Events CRM is a command-line interface (CLI) application designed to manage clients, contracts, and events for an event management company. The application uses an MVC (Model-View-Controller) architecture and is built with Python, SQLAlchemy, and the Rich CLI interface.

The application manages different user roles (Sales, Support, Management) with specific permissions, allowing for separation of responsibilities and efficient business process management.

## Features

- **Secure Authentication**: JWT-based authentication system
- **Client Management**: Creation, updating, and viewing of clients
- **Contract Management**: Creation, updating, and viewing of contracts
- **Event Management**: Creation, updating, and viewing of events
- **User Management**: Creation and updating of employees with different roles
- **Interactive CLI Interface**: Interactive menu with clear commands
- **Permission Control**: Access to functionalities based on user roles
- **Data Validation**: Input validation to ensure data integrity
- **Error Logging**: Integration with Sentry for error monitoring
- **PostgreSQL Database**: Reliable data storage with PostgreSQL and psycopg2

## Project Architecture

```
EpicEventsCRM/
├── controllers/          # Controllers managing user interactions
├── models/               # SQLAlchemy data models
├── utils/                # Utilities (validation, permissions)
├── views/                # Views (user interface)
├── __init__.py           # Package initialization
db/                       # Database configuration and initialization
scripts/                  # Utility scripts
services/                 # Business services
tests/                    # Unit and integration tests
auth.py                   # Authentication management
config.py                 # Application configuration
epicevents.py             # Main entry point
```

## Installation

### 📌 Prerequisites

Ensure that you have the following installed:
- **Python 3.9+**
- **PostgreSQL and PgAdmin**
- **pip** (Python package manager)
- **Virtual Environment Support** (recommended)

### 📂 Setup Instructions

1️⃣ **Clone the repository:**
   ```bash
   git clone https://github.com/SalehTrissi/OC-P12-CRM-EpicEvents.git
   cd OC-P12-CRM-EpicEvents
   ```

2️⃣ **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate     # For Windows
   ```

3️⃣ **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The following sections will guide you through configuring your environment for Epic Events CRM.

## Database Setup

### **Step 1: Install PostgreSQL**
Download and install [PostgreSQL](https://www.postgresql.org/download/), and ensure the server is running.

### **Step 2: Create the Database**
Once you have PostgreSQL installed, you can create the database using the following steps:

1. Open the SQL Shell (psql) from your Start menu or applications folder
2. When prompted, provide your PostgreSQL server details (or press Enter to accept defaults)
3. After connecting, run:

```sql
CREATE DATABASE epic_events;
```

If you want to create a dedicated user (optional):
```sql
CREATE USER epic_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE epic_events TO epic_admin;
ALTER DATABASE epic_events OWNER TO epic_admin;
```

The last command is crucial as it sets the user as the owner of the database, which is necessary for proper access rights.

> **💡 Pro Tip:**  
> If using `pgAdmin`, you can create the database visually via the interface by right-clicking on "Databases" and selecting "Create > Database". Then, under the "Privileges" tab, you can assign the owner.

### **Step 3: Create and Begin Setting Up the .env File**

Now create a `.env` file in the root directory of the project and add your database connection information:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/epic_events
```

Make sure to replace `user:password` with your actual PostgreSQL username and password, and `epic_events` with your database name if you used a different name.

### **Step 4: Initialize the Database**

Now that your database connection is configured, run the initialization script to create the necessary tables:

```bash
python -m db.initialize_db
```

You should see a confirmation message:
```
✅ All tables have been created successfully.
```

### **Step 4: Generate a JWT Secret Key**

A JWT secret key is required for secure authentication. Generate a random key using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add the generated key to your `.env` file:

```
JWT_SECRET=your_generated_jwt_secret_key
```

Replace `your_generated_jwt_secret_key` with the actual key you just generated.

### **Step 5: Configure Sentry (Optional)**

If you want to use Sentry for error tracking:

1. Sign up at [Sentry.io](https://sentry.io/signup/)
2. Create a new project and select **Python** as the platform
3. Copy the DSN URL from **Project Settings > Client Keys (DSN)**
4. Add it to your `.env` file:

```
SENTRY_DSN=your_sentry_dsn_key
```

> **⚠️ Important:** Keep your secret keys **private** and never share them in public repositories!

### **Step 6: Create an Administrative User**

Create your first administrative user:
```bash
python -m scripts.create_employee
```

Follow the prompts to create a Management user who will have full access to the system.

## Application Commands

You can interact with Epic Events CRM in **two ways**:

### **1️⃣ Using Direct Commands**
Run specific commands directly:
```bash
python -m epicevents login
python -m epicevents create-client
python -m epicevents list-clients
python -m epicevents update-client 1
python -m epicevents logout
```

### **2️⃣ Using the Interactive Menu**
Launch an interactive session where you can choose commands:
```bash
python -m epicevents menu
```
You can stay in the menu and navigate through the available options.

### **3️⃣ Displaying Help**
To see a list of all available commands:
```bash
python -m epicevents help
```

### Command Table

| Command            | Description                              |
|--------------------|------------------------------------------|
| `create-client`    | Create a new client                      |
| `create-contract`  | Create a new contract                    |
| `create-employee`  | Create a new employee                    |
| `create-event`     | Create a new event                       |
| `list-clients`     | List all clients                         |
| `list-contracts`   | List all contracts                       |
| `list-events`      | List all events                          |
| `update-client`    | Update an existing client                |
| `update-contract`  | Update an existing contract              |
| `update-employee`  | Update an existing employee              |
| `update-event`     | Update an existing event                 |
| `login`            | Log in to the system                     |
| `logout`           | Log out of the system                    |
| `status`           | Show the current login status            |
| `menu`             | Display the interactive menu             |
| `help`             | Show help for all commands               |

## Roles and Permissions

The application has three main roles with specific permissions:

### Sales
- Client management (creation, updating)
- Contract modification
- Event creation
- Viewing lists (clients, contracts, events)

### Support
- Event updating
- Event filtering
- Viewing lists (clients, contracts, events)

### Management
- User management (creation, updating)
- Contract management (creation, modification)
- Event filtering
- Support contact assignment
- Viewing lists (clients, contracts, events)

The role-based access control (RBAC) system ensures that each user receives appropriate permissions according to their role. Administrators can adjust roles and permissions to align with internal security policies.

## Data Models

### Employee
- Personal information (first name, last name, email, phone)
- Department (Sales, Support, Management)
- Secure password (hashed with Argon2)

### Client
- Client information (name, email, phone, company)
- Assigned sales contact
- Creation and last contact dates

### Contract
- Total and remaining amounts
- Status (signed or not)
- Associated client
- Associated sales contact

### Event
- Event information (name, dates, location, attendees)
- Associated client
- Associated contract
- Assigned support contact

## Testing

To run all tests:

```bash
pytest
```

Individual tests:

```bash
python -m tests.test_database_connection
python -m tests.test_sentry
```

##
> **📌 Useful Debugging Tips:**  
> - Run `python -m epicevents status` to check authentication status.  
> - If you encounter permission errors, ensure PostgreSQL credentials are correct.

## Troubleshooting

To assist in resolving potential issues:

- **Database Connection Issues:** Verify that your `DATABASE_URL` is correct and that PostgreSQL is running.
- **Installation Problems:** Ensure that your virtual environment is active and all dependencies are installed.
- **Environment Variable Errors:** Double-check your `.env` file for typos or misconfigurations.

## Error Monitoring

The application uses Sentry for error monitoring. To activate it, add your Sentry DSN in the `.env` file:

```
SENTRY_DSN=https://your_key@sentry.io/your_project
```
---

🎉 **Enjoy using Epic Events CRM!**  
We welcome your feedback and contributions to help improve the project.

---

© Epic Events CRM - Developed for efficient corporate event management