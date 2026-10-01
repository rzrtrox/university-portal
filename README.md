# 🎓 OnnCampus

### Your University, Connected.

**OnnCampus** is a social platform designed to bring university students together in one digital space — making it easier to discover people, share content, explore events, connect with clubs, and engage with campus life.

> Built with the idea of making university life more **social, interactive, and connected**.

---

## ✨ What is OnnCampus?

Traditional university portals are mainly focused on academic information and announcements.

OnnCampus takes a different approach.

It focuses on the **student experience** — giving students a place to discover people, interact with content, explore campus activities, and build connections.

The goal is to create a digital environment that feels less like a university portal and more like a **social platform built specifically for campus life**.

---

## 🚀 Features

### 👤 Student Profiles

* Personal student profiles
* Profile picture and bio
* Program and semester information
* Relationship status
* Personal images
* Student discovery

### 📰 Social Feed

* Create posts
* Share images and videos
* Like posts
* Comment on posts
* Reply to comments
* Interactive feed experience

### 🔍 Discover

* Discover other students
* Explore profiles
* Find people across different programs and semesters
* Social discovery experience

### 🏆 University Leaderboard

* Student engagement-based rankings
* Interest and interaction-based scoring
* University Crush categories

### 🎉 Events

* Discover university events
* Explore campus activities
* Event-focused experience

### 🔔 Notifications

* Stay updated with interactions
* Friend and social activity notifications

### 📱 Responsive UI

* Desktop and mobile-friendly interface
* Responsive layouts
* Modern dark-themed interface
* Interactive components and animations

---

## 🛠️ Tech Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| **Django**       | Backend & application framework |
| **Python**       | Core backend development        |
| **PostgreSQL**   | Database                        |
| **Supabase**     | Database & media storage        |
| **HTML / CSS**   | Frontend                        |
| **JavaScript**   | Frontend interactions           |
| **Font Awesome** | Icons                           |

---



## 📸 Screenshots

### 🏠 Home Feed

<!-- Add screen<img width="1917" height="967" alt="Screenshot 2026-10-01 113635" src="https://github.com/user-attachments/assets/fd3cb72c-33c0-41ec-8101-52054c2b6f0e" />
shot here -->

![OnnCampus Home](screenshots/home.png)

### 👤 Student Profile

<!-- Add screenshot here -->

![OnnCampus Profile](screenshots/profile.png)

### 🔍 Discover

<!-- Add screenshot here -->

![OnnCampus Discover](screenshots/discover.png)

### 🎉 Events

<!-- Add screenshot here -->

![OnnCampus Events](screenshots/events.png)

---

## 🏗️ Project Structure

```text
OnnCampus/
│
├── templates/
│   ├── components/
│   ├── home/
│   ├── profiles/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── media/
│
├── manage.py
└── requirements.txt
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required database and Supabase configuration.

```env
DATABASE_URL=your_database_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
```

> Never commit your `.env` file or private credentials to GitHub.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 📈 Project Status

🚧 **OnnCampus is currently under active development.**

The project is continuously evolving with new features, UI improvements, performance optimizations, and experiments around the student social experience.

---

## 🎯 Vision

The long-term goal of OnnCampus is to build a platform where university students can:

**Discover → Connect → Share → Participate**

all within one campus-focused social ecosystem.

---

## 👨‍💻 Built By

**[Your Name]**

BCA (Honours) — Machine Learning & Artificial Intelligence

Interested in building products, experimenting with technology, and turning ideas into working applications.

---

⭐ If you find the project interesting, consider giving the repository a star!
