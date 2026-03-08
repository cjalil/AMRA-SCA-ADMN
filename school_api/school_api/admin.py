from django.contrib import admin
# ✅ 1. Zidna GardeCategory w SchoolClass fl import
from .models import Student, PickupRequest, School, UserProfile, GardeCategory, SchoolClass, StudentPresence,AllStudents,PickupRequestBackup


admin.site.register(StudentPresence)

@admin.register(PickupRequestBackup)
class PickupRequestBackupAdmin(admin.ModelAdmin):
    # كنعطيو السميات ديال الحقول مباشرة حيت كاينين فالموديل
    list_display = ('student_name', 'created_at_original', 'is_completed', 'school_name')
    
    # من الأحسن تزيد الفيلتر باش يسهال عليك تعزل الداتا فـ Admin
    list_filter = ('is_completed', 'school_name', 'created_at_original')
    
    # هادي باش تزيد خانة ديال البحث الفوق، تقلب بيها بسمية التلميذ أو المدرسة
    search_fields = ('student_name', 'school_name', 'original_pickup_id')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'radius', 'slug','api_key', 'active_admin_scan') 
    search_fields = ('name',)
    list_editable = ('active_admin_scan',) 

admin.site.register(School, SchoolAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'is_parent_account','is_prof_account') # ✅ Zedt is_parent_account bach tban
    list_filter = ('school', 'is_parent_account')

admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(AllStudents) 
class AllStudentsAdmin(admin.ModelAdmin):
    list_display = ( 'school', 'first_name')

# ✅ 2. Configuration dyal GardeCategory
@admin.register(GardeCategory) 
class GardeCategoryAdmin(admin.ModelAdmin):
    # Bach iban lik l'asm, lmadrasa, w taman
    list_display = ('name', 'school', 'price')
    # Bach t9dar tfiltri b lmadrasa
    list_filter = ('school',)
    # Recherche b smiya
    search_fields = ('name',)

# ✅ 3. Configuration dyal SchoolClass
@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    # Bach iban lik l9issm, lmadrasa, w la garde (maternelle/primaire...)
    list_display = ('name', 'school', 'garde_category', 'created_at')
    # Filtre b lmadrasa w la garde
    list_filter = ('school', 'garde_category')
    # Recherche b smiyt l9issm
    search_fields = ('name',)

# إعدادات جدول التلاميذ
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('code_id', 'first_name', 'last_name', 'class_name', 'group','badge_number','school')
    search_fields = ('first_name', 'last_name', 'code_id')
    list_filter = ('school', 'class_name', 'group') # ✅ Zedt school hna bach tkon mndma ktar

# إعدادات جدول الطلبات

    

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    # كنزيدو السمية ديال الميتود اللي غتصاوب لتحت 'get_school_name'
    list_display = ('student', 'created_at', 'is_completed', 'get_school_name')
    
    # باش تأفيشي الفيلتر على اليمين (اختياري)
    list_filter = ('is_completed', 'created_at', 'student__school')

    # الميتود اللي كتجيب السمية ديال المدرسة
    def get_school_name(self, obj):
        if obj.student and obj.student.school:
            return obj.student.school.name
        return "بدون مدرسة"
    
    # باش تبدل السمية ديال الكولون (Column) فـ Admin
    get_school_name.short_description = 'École (School)'
    
    # باش تخدم الترتيب (Sorting) بهاد الكولون
    get_school_name.admin_order_field = 'student__school__name'