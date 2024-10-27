# Online Exam System

Welcome to the **Online Exam System**, a comprehensive web application built with Django for creating and managing online examinations. This project provides features for students to take exams online, and for administrators to manage exam content and users.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- **User Authentication**: Secure registration and login for both students and administrators.
- **Exam Management**: Create, edit, and delete exams with multiple-choice questions and different formats.
- **Timer Functionality**: Set time limits for each exam to enhance the testing experience.
- **Real-time Results**: Instant feedback on student performance with detailed results.
- **User Profiles**: Each user has a profile that tracks their exam history and performance.

## Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap (for styling)
- **Database**: SQLite (or any other supported database)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Wahidu1/Online-Exam.git
   cd Online-Exam
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the Online Exam System.
   - For admin access, go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Usage

- **Admin Dashboard**: Manage exams, questions, users, and view overall statistics.
- **Exam Taking**: Students can log in, view available exams, and take them online with timer support.
- **Results**: Students can view their results immediately after completing an exam.

## Project Structure

```plaintext
Online-Exam/
├── exams/                  # Django app containing exam models, views, and templates
├── static/                 # Static files (CSS, JavaScript, images)
├── templates/              # HTML templates for rendering views
├── manage.py               # Django management script
├── requirements.txt        # Python package requirements
└── README.md               # Project README
```

## License

This project is open source and available under the [MIT License](LICENSE).
```

Feel free to modify any sections or add specific details that are unique to your project!
