# 🌐 BlogWeb

A simple, responsive, and user-friendly blog web application built with **Flask** and **SQLite3**. BlogWeb allows users to securely register, log in, and manage their blog posts through an intuitive interface.

---

## ✨ Features

- 🔐 User Authentication (Sign Up & Login)
- ✍️ Create, edit, and delete blog posts
- 📖 Browse and read all published blogs
- 💾 SQLite3 database for lightweight data storage

---

## 🛠️ Tech Stack

**Backend**
- Flask (Python)

**Database**
- SQLite3
- Flask-SQLAlchemy

**Frontend**
- HTML5
- CSS3
- JavaScript

---

## 📁 Project Structure

```text
BlogWeb/
│
├── app/
├── static/
├── templates/
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/vaishali2005/BlogWeb.git
cd BlogWeb
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add:

```env
SECRET_KEY=your_secret_key_here
```

### 5. Run the application

```bash
python run.py
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

---
## ⚠️ Current Limitations

- User profile customization is not available.
- Password reset and email verification are not implemented.
- Blog search and advanced filtering features are not available.
- Rich text editing and image uploads within blog posts are not supported.
- User roles (e.g., Admin and Author) are not implemented.
- Pagination is not available for large numbers of blog posts.
- SQLite is used as the database, making the application more suitable for learning and small-scale projects rather than production environments.
- The application is designed for local development and is not deployed to a public hosting platform.
-not fully responsive
---