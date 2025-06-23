# 🧠 EduPlatform Backend – Flask + OpenAI + JWT

This is the backend service for the **EduPlatform** full-stack application. It provides secure APIs for student and instructor dashboards, integrates OpenAI GPT for AI chat assistance, and uses a modular blueprint structure with SQLAlchemy ORM and JWT-based authentication.

---

## 🚀 Tech Stack

- **Python 3.10+**
- **Flask** (Web Framework)
- **Flask-JWT-Extended** (Authentication)
- **Flask-SQLAlchemy** (ORM)
- **Flask-Migrate** (Database Migrations)
- **OpenAI API** (GPT-based chat integration)
- **CORS**, **dotenv**, **blueprints**, etc.

---

## ⚙️ Features

- ✅ **User Auth**: Register/Login with JWT tokens
- 🧑‍🏫 **Instructor Panel**: Add/View course content, students enrolled in course and due dates
- 🎓 **Student Panel**: Update progress, view course details
- 🤖 **AI Chatbot**: Integrated with OpenAI GPT-3.5
- 🗂️ **Blueprint Modules**: Separated concerns by `auth`, `student`, `instructor`, `chat`, `courses`
- 🔐 **Protected Endpoints** with role-based access

---

## 📁 Project Structure

```bash
student_dashboard/
│
├── app/
│   ├── auth/               # Auth routes & utils
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── chat/               # Chatbot endpoints
│   │   └── routes.py
│   │
│   ├── courses/            # Course endpoints
│   │   └── routes.py
│   │
│   ├── instructor/         # Instructor-specific routes
│   │   └── routes.py
│   │
│   ├── student/            # Student-specific routes
│   │   ├── routes.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── main.py         # Flask app entry
│   │
│   ├── models/             # SQLAlchemy models
│   │   └── models.py
│   │
│   └── routes/             # Aggregator for all blueprints
│       ├── auth.py
│       ├── instructor.py
│       └── student.py
│
├── migrations/             # Flask-Migrate files
├── .env                    # Environment variables
├── requirements.txt
└── README.md
```

# 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
https://github.com/Yash1thvs/student_dashboard.git
cd student_dashboard
```

### 2. Create & Activate Virtual Environment
```bash
- python -m venv venv
- source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory:
- SECRET_KEY = YOUR_SECRET_KEY
- SQLALCHEMY_DATABASE_URI = mysql+pymysql://root:<password@localhost>/db_name
- JWT_SECRET_KEY = YOUR_JWT_SECRET_KEY
- OPENAI_API_KEY = YOUR_OPENAI_API_KEY

### 5. Run Database Migrations
```bash
flask db init      # Only first time
flask db migrate -m "Initial tables"
flask db upgrade
```
### 6. Run the Flask App
```bash
cd app
python main.py
```
Server runs at:
📍 http://localhost:5000

# 🔐 API Overview
| Endpoint              | Method | Role       | Description                   |
| --------------------- | ------ | ---------- |-------------------------------|
| `/auth/register`      | POST   | Any        | Register a new user           |
| `/auth/login`         | POST   | Any        | JWT login                     |
| `/student/dashboard`  | GET    | Student    | Student course progress       |
| `/instructor/courses` | POST   | Instructor | Create and View a course      |
| `/chat`               | POST   | Student    | Ask AI assistant (OpenAI GPT) |
| `/chat/history`       | GET    | Student    | View chat history             |

# 🧠 Approach & Implementation
* Modular Blueprints: Each domain (auth, chat, courses) is modularized for scalability.
* AI Chat: Messages are saved in the database and paired by timestamp for clean history retrieval.
* Security: JWT protects all sensitive endpoints with role-based access control.
* ChatGPT Integration: Uses openai.ChatCompletion.create to respond to student doubts.

# ⚠️ Challenges I Faced
* ❌ OpenAI Key Quota Error: Initially received insufficient_quota, resolved via API key re-generation.
* 🔁 Chat Duplication on Frontend: Fixed a logic error in the history render function.
* ⚙️ Modular Routing: Refactored into reusable blueprints for clarity and testability.
* 🔐 Token Handling: Carefully validated tokens across protected views.

# 📌 Enhancement
*  Add support for instructors to reply to student questions
*  Admin panel with analytics
*  CI/CD setup and deployment to Render 
*  Add Swagger documentation