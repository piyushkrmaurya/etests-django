from datetime import timedelta, datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from api.utils import (
    SessionEvaluation,
    generate_ranks,
    get_unique_slug,
    random_key,
    unique_random_key,
)
from etests.storage_backends import MediaStorage, PrivateMediaStorage

class EmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super(EmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, *args, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password", random_key())
        self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff member.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be a staff member.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=100, default=random_key)
    email = EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    image = models.CharField(max_length=2048, null=True, blank=True)
    site = models.CharField(max_length=250, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(_("active"), default=True)
    is_student = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = MyUserManager()

    def __str__(self):
        return self.name


class Institute(models.Model):
    def extras_default():
        return dict(banner=None)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(unique=True, max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    current_credits = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    show = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    about = models.CharField(max_length=1024, null=True, blank=True)
    settings = models.JSONField(default=dict, null=True, blank=True)
    carousel = models.JSONField(default=list, null=True, blank=True)
    notifications = models.JSONField(default=list, null=True, blank=True)
    features = models.JSONField(default=list, null=True, blank=True)
    team = models.JSONField(default=list, null=True, blank=True)
    toppers = models.JSONField(default=list, null=True, blank=True)
    downloads = models.JSONField(default=list, null=True, blank=True)
    questions = models.JSONField(default=list, null=True, blank=True)
    gallery = models.JSONField(default=list, null=True, blank=True)
    faqs = models.JSONField(default=list, null=True, blank=True)
    courses = models.JSONField(default=list, null=True, blank=True)
    centers = models.JSONField(default=list, null=True, blank=True)
    contacts = models.JSONField(default=dict, null=True, blank=True)
    faculty = models.JSONField(default=list, null=True, blank=True)
    links = models.JSONField(default=list, null=True, blank=True)
    forms = models.JSONField(default=list, null=True, blank=True)
    extras = models.JSONField(default=extras_default, null=True, blank=True)

    def __str__(self):
        return self.user.name

    @property
    def name(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_institute = True
        super(Institute, self).save(*args, **kwargs)


class Batch(models.Model):
    joining_key = models.CharField(max_length=8, default=random_key)
    name = models.CharField(max_length=100)
    institute = models.ForeignKey(
        Institute, related_name="batches", on_delete=models.CASCADE
    )

    def students(self):
        return Student.objects.filter(enrollment__batch=self)

    def __str__(self):
        if self.name == "Common Batch":
            return f"{self.name} ({self.institute.name})"
        else:
            return self.name

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "Batches"


class Enrollment(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    batch = models.ForeignKey(
        Batch,
        blank=True,
        null=True,
        related_name="enrollments",
        on_delete=models.CASCADE,
    )
    roll_number = models.CharField(max_length=25)
    student = models.ForeignKey(
        "Student", related_name="enrollment", null=True, on_delete=models.SET_NULL
    )
    date_joined = models.DateField(default=datetime.now)

    def __str__(self):
        if self.roll_number:
            return self.roll_number
        elif self.student:
            return self.student.user.name
        else:
            return str(self.pk)

    @property
    def joining_key(self):
        return self.batch.joining_key

    def save(self, *args, **kwargs):
        errors = {}
        if self.batch not in self.institute.batches.all():
            errors["batch"] = ("This batch does not belong to the institute.",)
            raise ValidationError(errors)
        else:
            super(Enrollment, self).save(*args, **kwargs)


class Contact(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    description = models.CharField(max_length=250)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description


class Student(models.Model):
    GENDERS = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    institutes = models.ManyToManyField(
        Institute, related_name="students", through=Enrollment, blank=True
    )

    def __str__(self):
        return self.user.name

    def batches(self):
        return Batch.objects.filter(enrollments__student=self)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_student = True
        super(Student, self).save(*args, **kwargs)


class Employee(models.Model):
    qualification = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)


class Subject(models.Model):
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("position", "name")


class Topic(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(
        Subject, related_name="topics", on_delete=models.CASCADE
    )
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("subject", "position", "name")


class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField("position")
    name = models.CharField(max_length=200)
    countries = CountryField(multiple=True, blank=True)
    slug = models.SlugField(unique=False, editable=False)
    image = models.CharField(
        default="exam.png", max_length=20 * 1024, blank=True, null=True
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ("position",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Exam, self).save(*args, **kwargs)


class TestSeries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, editable=False)
    visible = models.BooleanField(default=False)
    exams = models.ManyToManyField(Exam, related_name="test_series", blank=True)
    discount = models.IntegerField(default=0)
    institute = models.ForeignKey(
        Institute,
        related_name="test_series",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    registered_students = models.ManyToManyField(Student, blank=True)
    tests = models.ManyToManyField("Test", related_name="test_series", blank=True)

    class Meta:
        ordering = ("-date_added",)
        verbose_name = "Test Series"
        verbose_name_plural = "Test Series"

    def __str__(self):
        return self.name

    def free(self):
        return self.price == 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(TestSeries, self).save(*args, **kwargs)


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    registered_students = models.ManyToManyField(
        Student, related_name="tests", blank=True
    )
    registered_batches = models.ManyToManyField(Batch, related_name="tests", blank=True)
    name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute, related_name="tests", blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(unique=True, editable=False)
    exam = models.ForeignKey(
        Exam, related_name="tests", blank=True, null=True, on_delete=models.SET_NULL
    )
    aits = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    activation_time = models.DateTimeField(blank=True, null=True)
    closing_time = models.DateTimeField(blank=True, null=True)
    time_alotted = models.DurationField(default=timedelta(hours=3))
    sections = models.JSONField(blank=True, null=True)
    questions = models.JSONField(blank=True, null=True)
    answers = models.JSONField(blank=True, null=True)
    stats = models.JSONField(blank=True, null=True)
    corrected = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    free = models.BooleanField(default=False)
    marks_list = models.JSONField(blank=True, null=True)
    syllabus = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ("-date_added",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Test, self).save(*args, **kwargs)

    @property
    def status(self):
        if not self.activation_time or timezone.now() < self.activation_time:
            return 0
        elif (
            not self.closing_time
            or self.activation_time <= timezone.now()
            and timezone.now() < self.closing_time
        ):
            return 1
        elif self.closing_time <= timezone.now():
            if not self.corrected and not self.finished:
                return 2
            elif not self.finished:
                return 3
            else:
                return 4

    def __str__(self):
        return self.name

    def evaluate_sessions(self, include_practice=False, include_evaluated=False):
        sessions = self.sessions
        if not include_evaluated:
            sessions = sessions.exclude(marks__isnull=False)
        if not include_practice:
            sessions = sessions.exclude(practice=True)
        for session in sessions:
            session.evaluate(commit=False)
        Session.objects.bulk_update(sessions, ["marks", "result", "completed"])

    def generate_ranks(self):
        sessions = self.sessions.filter(practice=False, completed=True)
        if len(sessions) > 0:
            generated = generate_ranks(sessions)
            if generated:
                Session.objects.bulk_update(generated.get("sessions", None), ["ranks"])
                self.marks_list = generated.get("marks_list", None)
                self.stats = generated.get("stats", None)
        self.finished = True
        self.save()


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, related_name="sessions", on_delete=models.CASCADE
    )
    test = models.ForeignKey(
        Test, related_name="sessions", null=True, on_delete=models.CASCADE
    )
    practice = models.BooleanField(default=False)
    checkin_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(hours=3))
    completed = models.BooleanField(default=False)
    response = models.JSONField(blank=True, null=True)
    result = models.JSONField(default=list, blank=True, null=True)
    current = models.JSONField(blank=True, null=True)
    marks = models.JSONField(blank=True, null=True)
    ranks = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ("practice", "checkin_time", "test", "student")

    def __str__(self):
        return self.student.user.name + " " + self.test.name

    def expired(self):
        return self.checkin_time + self.test.time_alotted <= timezone.now()

    def evaluate(self, commit=True):
        SessionEvaluation(self).evaluate()
        if commit:
            self.save()

    def save(self, *args, **kwargs):
        duration = max(
            self.test.time_alotted - (timezone.now() - self.checkin_time), timedelta(0)
        )
        duration -= timedelta(microseconds=duration.microseconds)
        self.duration = duration
        if self.pk is None:
            self.completed = False
            self.current = {"question_index": 0, "section_index": 0}
            response = list()
            for i, question in enumerate(self.test.questions):
                response.append(
                    {
                        "answer": [[], [], [], []] if question["type"] == 3 else [],
                        "status": 1 if i == 0 else 0,
                        "time_elapsed": 0,
                    }
                )
            self.response = response
            self.practice = self.test.status > 1

        super(Session, self).save(*args, **kwargs)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=200)
    receipt = models.FileField(storage=PrivateMediaStorage(), null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    student = models.ForeignKey(
        Student,
        related_name="payments",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    amount = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    test_series = models.ForeignKey(
        TestSeries, blank=True, null=True, on_delete=models.SET_NULL
    )
    show = models.BooleanField(default=False)

    def __str__(self):
        if self.student:
            return self.student.user.name
        else:
            return self.transaction_id

    def save(self, *args, **kwargs):
        if self.student and self.verified:
            self.test_series.registered_students.add(self.student)
            for test in self.test_series.tests.all():
                test.registered_students.add(self.student)

        super(Payment, self).save(*args, **kwargs)


class Variable(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTIONS_TYPE_CHOICES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("NETBANKING", "Netbanking"),
        ("PAYTM", "PayTM"),
        ("OTHERS", "Others"),
    )
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    credits_added = models.IntegerField(default=0)
    transaction_id = models.CharField(
        max_length=200, null=True, blank=True, unique=True
    )
    mode = models.CharField(max_length=10, choices=TRANSACTIONS_TYPE_CHOICES)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return (
            self.institute.user.name + " / " + self.mode + " / " + self.transaction_id
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                self.credits_added = (
                    self.amount * Variable.objects.get(name="CREDITS_PER_RUPEE").value
                )
            except:
                self.credits_added = 0
            institute = self.institute
            institute.current_credits += self.credits_added
            institute.save()
        super().save(*args, **kwargs)


class CreditUse(models.Model):
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    credits_used = models.IntegerField(default=0)

    def __str__(self):
        return (
            self.institute.user.name
            + " / "
            + str(self.date_added)
            + " / "
            + str(self.credits_used)
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            institute = self.institute
            # Later: calculate credits_used using fixed rate
            institute.current_credits -= self.credits_used
            institute.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Credits Usage"


class ResetCode(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name="codes", blank=True, null=True, on_delete=models.SET_NULL
    )
    reset_code = models.CharField(max_length=6)
    date_added = models.DateField(auto_now_add=True)
    done = models.BooleanField(default=False)


class TestSeriesTransaction(models.Model):
    TRANSACTIONS_TYPE_CHOICES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("NETBANKING", "Netbanking"),
        ("PAYTM", "PayTM"),
        ("OTHERS", "Others"),
    )
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=200, null=True, blank=True, unique=True
    )
    mode = models.CharField(max_length=10, choices=TRANSACTIONS_TYPE_CHOICES)
    amount = models.IntegerField(default=0)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    test_series = models.ManyToManyField(
        TestSeries, related_name="aits_transactions", blank=False
    )
    receipt = models.FileField(storage=PrivateMediaStorage(), null=True, blank=True)

    def __str__(self):
        return f"{self.institute.user.name} / {self.mode} / {self.transaction_id}"

    class Meta:
        verbose_name_plural = "Test Series Transactions"


class Question(models.Model):
    TYPES = (
        (0, "Single Correct"),
        (1, "Multiple Correct"),
        (2, "Numerical"),
        (3, "Matrix Match"),
        (4, "Paragraph"),
    )
    LEVELS = (
        (0, "Very Easy"),
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
        (4, "Very Hard"),
    )
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=20000)
    answer = models.JSONField()
    solution = models.CharField(max_length=20000, null=True, blank=True)
    type = models.IntegerField(choices=TYPES)
    difficulty = models.IntegerField(choices=LEVELS, null=True, blank=True)
    exam = models.ForeignKey(Exam, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(
        Subject, null=True, blank=True, on_delete=models.SET_NULL
    )
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL)
    test = models.ForeignKey(Test, null=True, blank=True, on_delete=models.SET_NULL)
    institute = models.ForeignKey(
        Institute, null=True, blank=True, on_delete=models.SET_NULL
    )
    correct_marks = models.FloatField(default=4)
    partial_marks = models.FloatField(default=0)
    incorrect_marks = models.FloatField(default=1)
    option_count = models.IntegerField(default=4)
    tags = models.JSONField(default=list, null=True, blank=True)
    parent = models.ForeignKey(
        "self", related_name="parts", null=True, blank=True, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.type:
            if self.type == 1:
                self.incorrect_marks = 2
            elif self.type == 2:
                self.correct_marks = 3
                self.incorrect_marks = 0
            elif self.type == 3:
                self.partial_marks = 2
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("subject", "topic", "type", "difficulty")


def validate_file_size(file):
    if file.size > 256000:
        raise ValidationError("The maximum image size is 250 KB.")
    else:
        return file


class QuestionImage(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField(
        storage=MediaStorage(), validators=[validate_file_size]
    )

    def __str__(self):
        if self.file:
            return str(self.file)
        else:
            str(self.id)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField(
        storage=MediaStorage(), validators=[validate_file_size]
    )

    def __str__(self):
        if self.file:
            return str(self.file)
        else:
            str(self.id)
