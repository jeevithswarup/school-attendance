<div align="center">

<img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

<br/><br/>

<h1>🎓 EduTrack — School Management System</h1>

<p><strong>A production-ready, full-stack Django application for managing students, attendance, fees, and academics — built with zero JavaScript frameworks, pure Django templates and Bootstrap 5.</strong></p>

<br/>

![EduTrack Dashboard Preview](https://placehold.co/900x420/0f172a/0ea5e9?text=EduTrack+%E2%80%94+School+Management+System&font=raleway)

</div>

---

## ✨ What is EduTrack?

EduTrack started as a hackathon attendance tracker and evolved into a **complete school management platform**. It handles everything a school needs day-to-day — from marking attendance by roll number to generating PDF report cards — all through a clean, role-aware Django interface.

No React. No Vue. No separate frontend. Just Django doing what Django does best.

---

## 🚀 Features at a Glance

| Module | What it does |
|---|---|
| 🔐 **Authentication** | Custom user model with 4 roles — Admin, Teacher, Student, Parent |
| 🏠 **Dashboards** | Role-specific dashboards with live stats for each user type |
| 👨‍🎓 **Students** | Full CRUD — add, edit, search, filter by class/section, soft delete |
| 📋 **Attendance** | Mark by roll numbers in bulk, QR code scan, per-student history |
| 💰 **Fees** | Fee structures, payment tracking, paid/partial/pending status |
| 📊 **Marks** | Enter marks per subject/exam, auto grade calculation, report cards |
| 📄 **PDF Export** | Generate and download report cards as PDF via ReportLab |
| 🔲 **QR Attendance** | Generate QR codes — students scan to mark themselves present |
| 🌱 **Seed Data** | One command to populate 60 students with realistic fake data |

---

## 🖥️ Screenshots

<table>
  <tr>
    <td align="center"><b>Login Page</b></td>
    <td align="center"><b>Admin Dashboard</b></td>
  </tr>
  <tr>
    <td><img src="https://placehold.co/420x260/0f172a/0ea5e9?text=Login+Page&font=raleway" width="420"/></td>
    <td><img src="https://placehold.co/420x260/f1f5f9/0f172a?text=Admin+Dashboard&font=raleway" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><b>Attendance — Roll Number Entry</b></td>
    <td align="center"><b>Student Report Card</b></td>
  </tr>
  <tr>
    <td><img src="https://placehold.co/420x260/f1f5f9/0f172a?text=Attendance+Module&font=raleway" width="420"/></td>
    <td><img src="https://placehold.co/420x260/f1f5f9/0f172a?text=Report+Card+PDF&font=raleway" width="420"/></td>
  </tr>
</table>

---

## 🏗️ Project Architecture

```
school-attendance/
│
├── accounts/               # Custom User model, login, profile, user management
│   ├── models.py           # AbstractUser with role field (admin/teacher/student/parent)
│   ├── views.py            # Login, logout, profile, user CRUD
│   ├── dashboard_views.py  # Role-based dashboard routing
│   └── forms.py
│
├── students/               # Student management
│   ├── models.py           # Student model with class, section, roll number
│   ├── views.py            # List, detail, create, update, soft-delete
│   └── management/
│       └── commands/
│           └── seed_data.py  # 🌱 Faker-powered data seeder
│
├── attendance_app/         # Attendance system
│   ├── models.py           # Attendance + QRAttendanceSession
│   └── views.py            # Bulk roll-number marking, QR generate & scan
│
├── fees/                   # Fee management
│   ├── models.py           # FeeStructure + FeePayment
│   └── views.py            # Fee list, create, update, per-student view
│
├── marks/                  # Marks & academics
│   ├── models.py           # Subject + Mark with auto grade calculation
│   ├── views.py            # Marks CRUD, report card HTML + PDF
│   └── urls.py
│
├── templates/              # All Django templates (zero JS frameworks)
│   ├── base.html           # Sidebar + topbar layout
│   ├── accounts/
│   ├── dashboards/         # admin, teacher, student, parent
│   ├── students/
│   ├── attendance/
│   ├── fees/
│   └── marks/
│
├── settings.py
├── urls.py
└── requirements.txt
```

---

## ⚡ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/jeevithswarup/school-attendance.git
cd school-attendance
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

Or use the pre-built seed command which creates one automatically:

```bash
python manage.py seed_data --students 60
```

### 6. Start the server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — done.

---

## 🌱 Seed Fake Data

Populate the entire database with realistic fake data in one command:

```bash
python manage.py seed_data --students 60
```

This creates:
- ✅ 5 teachers across all classes
- ✅ 60 students with photos, addresses, DOB
- ✅ 72 subjects (6 per class × 12 classes)
- ✅ 30 days of attendance per student (weekdays, 75% present rate)
- ✅ Fee records with paid / partial / pending mix
- ✅ Marks for 2–4 exam types per subject with auto grades

**To wipe and re-seed cleanly:**

```bash
python manage.py seed_data --students 60 --clear
```

---

## 🔑 Demo Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Teacher | `teacher1` | `teacher123` |
| Student | `student_r1000` | `student123` |

---

## 👥 Role-Based Access

```
Admin     → Full access to everything
Teacher   → Mark attendance, enter marks, view students
Student   → View own dashboard, attendance %, marks, fee status
Parent    → View linked children's attendance, fees, report cards
```

Each role gets its own dashboard and sees only what's relevant to them. Unauthorized access attempts redirect gracefully.

---

## 📋 Attendance — Roll Number Mode

Instead of clicking dropdowns for every student, just type the roll numbers of students who are **present**:

```
101, 102, 105, 110
```

or one per line:

```
101
102
105
```

Hit submit — everyone in the selected class/section is marked. Present students get ✅, the rest get ❌ automatically. Invalid roll numbers are flagged with a warning.

---

## 📄 PDF Report Cards

Navigate to any student → Report Card → **Download PDF**

Generated with ReportLab — includes student info, all subjects, marks, percentage, grade, and attendance percentage on a clean A4 layout.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 |
| Frontend | Django Templates + Bootstrap 5.3 |
| Font | Inter (Google Fonts) |
| Icons | Bootstrap Icons 1.11 |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| QR Codes | `qrcode[pil]` |
| PDF | ReportLab |
| Fake Data | Faker (`en_IN` locale) |

---

## 🔧 Environment & Configuration

Key settings in `settings.py`:

```python
AUTH_USER_MODEL = 'accounts.User'   # Custom user model
LOGIN_URL       = '/accounts/login/'
LOGIN_REDIRECT_URL  = '/dashboard/'
TIME_ZONE       = 'Asia/Kolkata'
```

To switch to PostgreSQL, update `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edutrack',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📦 Dependencies

```
Django>=5.2
qrcode[pil]>=8.0
Pillow>=11.0
reportlab>=4.0
faker>=20.0
```

---

## 🗺️ Roadmap

- [ ] Timetable / schedule management
- [ ] SMS / email notifications for low attendance
- [ ] Razorpay fee payment integration
- [ ] Parent portal with child progress charts
- [ ] Bulk student import via CSV
- [ ] Dark mode toggle

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** — use it, fork it, build on it.

---

<div align="center">

Built with ❤️ using Django &nbsp;|&nbsp; Started as a hackathon project, grown into something real

⭐ **Star this repo if you found it useful!**

</div>
