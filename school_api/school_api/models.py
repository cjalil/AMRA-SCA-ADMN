from django.db import models
from django.contrib.auth.models import User

# 1. الموديل الجديد للمدرسة
# 1. Table jdida: Hna fin ghatsjel "Garde Maternelle", "Garde Primaire"...


        
class School(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    api_key = models.CharField(max_length=100, unique=True, blank=True)
    radius = models.IntegerField(default=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    admin_badge_code = models.CharField(max_length=255, default="111111111111111111111111111111")
    security_pin = models.CharField(max_length=4, default="1111")
    active_admin_scan = models.BooleanField(default=False, verbose_name="Activer Scan Badge Admin")
    class_order = models.TextField(blank=True, default="")
    

    def __str__(self):
        return self.name


class SchoolPort(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="ports")
    key = models.CharField(max_length=20)          # "port1" / "port2" / ...
    label = models.CharField(max_length=50)        # "Porte 1" / "باب الرئيسية"
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("school", "key")
        ordering = ["order"]
        
class GardeCategory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Ex: "Garde Maternelle"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Ila bghiti tzid taman mn b3d 

    def __str__(self):
        return f"{self.name} ({self.school.name})"
        
class SchoolClass(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=50) # Ex: PS-A
    # ✅ Hna fin kanrebto l 9issm b la Garde dyalo
    garde_category = models.ForeignKey(GardeCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="classes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'name')

    def __str__(self):
        return self.name

# 2. موديل التلميذ (مع التعديلات)
class Student(models.Model):
    # الربط بالمدرسة (Nullable باش يدوز الميغراسيون)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    
    # المعلومات العادية (تأكد أنك كاتب max_length)
    code_id = models.CharField(max_length=100) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    group = models.CharField(max_length=50, blank=True, null=True)
    cndp = models.CharField(max_length=50, blank=True, null=True)
    badge_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        # التلميذ فريد داخل نفس المدرسة فقط
        # (يعني ممكن يكون تلميذ عندو كود 100 فمدرسة A وتلميذ عندو 100 فمدرسة B)
        unique_together = ('school', 'code_id')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ... (باقي الموديلات بحال PickupRequest خليها كيما هي)
class PickupRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    porte_label = models.CharField(max_length=50, blank=True, null=True)

    
    porte = models.CharField(max_length=20, blank=True, null=True)      # Porte1..Porte4
    device_id = models.CharField(max_length=80, blank=True, null=True)  # ID ثابت للتليفون

    def __str__(self):
        return f"Pickup: {self.student} - {self.created_at}"
    
class PickupRequestBackup(models.Model):
    original_pickup_id = models.IntegerField()
    
    student_name = models.CharField(max_length=150)
    class_name = models.CharField(max_length=50, blank=True, null=True)
    badge_number = models.CharField(max_length=50, blank=True, null=True)

    school_name = models.CharField(max_length=150)

    is_completed = models.BooleanField(default=False)
    porte_label = models.CharField(max_length=50, blank=True, null=True)
    porte = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=80, blank=True, null=True)

    created_at_original = models.DateTimeField()
    backup_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backup {self.original_pickup_id} - {self.student_name}"


    

        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    is_parent_account = models.BooleanField(default=False)
    is_prof_account = models.BooleanField(default=False) # ✅ الحقل الجديد للأستاذ

    def __str__(self):
        if self.is_prof_account:
            role = "PROFESSEUR"
        elif self.is_parent_account:
            role = "PARENT"
        else:
            role = "GARDIEN"
        return f"{self.user.username} - {self.school.name} ({role})"
        
        
class AllStudents(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50) # القسم اللي جاي من CSV
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.class_name})"
        
        
class StudentPresence(models.Model):
    # Les choix dyal l'état
    PRESENCE_CHOICES = [
        ('PRESENT', 'Présent'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Retard'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="presences")
    student = models.ForeignKey(AllStudents, on_delete=models.CASCADE, related_name="presences")
    
    # Bla mat3awd t-stoki smya o l-nasab hit rah l-student ForeignKey m3ah kolchi
    # Ghir ila bghiti t-affichihom f l'interface, kat-accédi lihom b student.first_name
    
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=PRESENCE_CHOICES, default='PRESENT')
    remarque = models.TextField(blank=True, null=True)
    
    # Chkoun l-prof li sjel had l'absence (Optional)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    retard_minutes = models.IntegerField(default=0, null=True, blank=True) # الحقل الجديد

    class Meta:
        # Bach t-eviter t-marqui l'absence l-nefs l-student mra f nhar
        unique_together = ('student', 'date')
        verbose_name = "Présence Etudiant"
        verbose_name_plural = "Présences Etudiants"

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
        

