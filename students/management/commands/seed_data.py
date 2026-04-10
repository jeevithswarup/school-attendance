import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

fake = Faker('en_IN')

CLASSES   = [str(i) for i in range(1, 13)]
SECTIONS  = ['A', 'B', 'C']
GENDERS   = ['M', 'F']
EXAM_TYPES = ['unit1', 'unit2', 'midterm', 'final']
FEE_TYPES  = ['Tuition Fee', 'Library Fee', 'Sports Fee', 'Lab Fee']


class Command(BaseCommand):
    help = 'Seed fake students, attendance, fees, marks data'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=60,
                            help='Number of students to create (default 60)')
        parser.add_argument('--clear', action='store_true',
                            help='Clear existing data before seeding')

    def handle(self, *args, **options):
        from accounts.models import User
        from students.models import Student
        from attendance_app.models import Attendance
        from fees.models import FeeStructure, FeePayment
        from marks.models import Subject, Mark

        count = options['students']

        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Mark.objects.all().delete()
            FeePayment.objects.all().delete()
            FeeStructure.objects.all().delete()
            Attendance.objects.all().delete()
            Student.objects.all().delete()
            User.objects.filter(role__in=['student', 'teacher', 'parent']).delete()
            Subject.objects.all().delete()

        # ── Teachers ──────────────────────────────────────────
        self.stdout.write('Creating teachers...')
        teachers = []
        for i in range(1, 6):
            uname = f'teacher{i}'
            if not User.objects.filter(username=uname).exists():
                t = User.objects.create_user(
                    username=uname,
                    password='teacher123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    role='teacher',
                    phone=fake.phone_number()[:15],
                )
                teachers.append(t)
                self.stdout.write(f'  Teacher: {uname} / teacher123')

        # ── Subjects ──────────────────────────────────────────
        self.stdout.write('Creating subjects...')
        subject_data = [
            ('MATH', 'Mathematics'), ('SCI', 'Science'), ('ENG', 'English'),
            ('HIN', 'Hindi'), ('SST', 'Social Studies'), ('CS', 'Computer Science'),
        ]
        subjects = {}
        for code, name in subject_data:
            for cls in CLASSES:
                full_code = f'{code}{cls}'
                subj, _ = Subject.objects.get_or_create(
                    code=full_code,
                    defaults={'name': name, 'student_class': cls}
                )
                subjects.setdefault(cls, []).append(subj)

        # ── Fee structures ────────────────────────────────────
        self.stdout.write('Creating fee structures...')
        fee_structures = {}
        for cls in CLASSES:
            for fee_type in FEE_TYPES:
                amount = random.choice([500, 750, 1000, 1500, 2000])
                fs, _ = FeeStructure.objects.get_or_create(
                    student_class=cls, fee_type=fee_type,
                    defaults={'amount': amount, 'academic_year': '2024-25'}
                )
                fee_structures.setdefault(cls, []).append(fs)

        # ── Students ──────────────────────────────────────────
        self.stdout.write(f'Creating {count} students...')
        roll_counter = 1000

        for i in range(count):
            cls     = random.choice(CLASSES)
            section = random.choice(SECTIONS)
            gender  = random.choice(GENDERS)
            roll    = f'R{roll_counter}'
            roll_counter += 1

            first = fake.first_name_male() if gender == 'M' else fake.first_name_female()
            last  = fake.last_name()
            uname = f'student_{roll.lower()}'

            # Create linked user
            user = None
            if not User.objects.filter(username=uname).exists():
                user = User.objects.create_user(
                    username=uname,
                    password='student123',
                    first_name=first,
                    last_name=last,
                    email=fake.email(),
                    role='student',
                )

            dob = fake.date_of_birth(minimum_age=5, maximum_age=18)

            student = Student.objects.create(
                user=user,
                roll_number=roll,
                first_name=first,
                last_name=last,
                date_of_birth=dob,
                gender=gender,
                student_class=cls,
                section=section,
                address=fake.address(),
                phone=fake.phone_number()[:15],
                is_active=True,
            )

            # ── Attendance (last 30 days) ──────────────────
            for day_offset in range(30):
                att_date = date.today() - timedelta(days=day_offset)
                if att_date.weekday() >= 5:   # skip weekends
                    continue
                status = random.choices(
                    ['present', 'absent', 'late'],
                    weights=[75, 18, 7]
                )[0]
                Attendance.objects.get_or_create(
                    student=student, date=att_date,
                    defaults={'status': status, 'marked_by': 'seed'}
                )

            # ── Fees ──────────────────────────────────────
            for fs in fee_structures.get(cls, []):
                status = random.choices(['paid', 'pending', 'partial'], weights=[55, 30, 15])[0]
                paid   = float(fs.amount) if status == 'paid' else (
                         round(float(fs.amount) * random.uniform(.3, .7), 2) if status == 'partial' else 0
                )
                FeePayment.objects.create(
                    student=student,
                    fee_structure=fs,
                    amount_due=fs.amount,
                    amount_paid=paid,
                    status=status,
                    payment_date=fake.date_between(start_date='-6m', end_date='today') if status != 'pending' else None,
                    receipt_number=f'RCP{random.randint(10000,99999)}' if status != 'pending' else '',
                )

            # ── Marks ─────────────────────────────────────
            for subj in subjects.get(cls, []):
                for exam in random.sample(EXAM_TYPES, k=random.randint(2, 4)):
                    obtained = round(random.uniform(30, 100), 1)
                    Mark.objects.get_or_create(
                        student=student, subject=subj,
                        exam_type=exam, academic_year='2024-25',
                        defaults={'marks_obtained': obtained, 'max_marks': 100}
                    )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done! Created {count} students with attendance, fees & marks.'
        ))
        self.stdout.write('   Login: admin / admin123')
        self.stdout.write('   Student login: student_r1000 / student123')
        self.stdout.write('   Teacher login: teacher1 / teacher123')
