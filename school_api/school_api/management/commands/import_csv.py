import csv
import os
from django.core.management.base import BaseCommand
from school_api.models import Student, School
from django.utils.text import slugify
import random
import string

class Command(BaseCommand):
    help = 'Import Intelligent: Met à jour une école sans toucher aux autres'

    def handle(self, *args, **kwargs):
        file_path = 'convertcsv.csv' 

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Fichier non trouvé: {file_path}'))
            return

        self.stdout.write('Lecture du fichier CSV...')
        
        # 1. نجمعو الداتا ونعرفو شمن مدارس كاينين فالملف
        students_to_create = []
        schools_in_csv = set()

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                school_name = row['school'].strip().replace('"', '').replace('\n', '')
                if not school_name: school_name = "Ecole Inconnue"
                
                schools_in_csv.add(school_name) # كنحفظو سمية المدرسة

                students_to_create.append({
                    'row': row,
                    'school_name': school_name
                })

        # 2. نمسحو ونعاودو غير المدارس لي كاينة فالملف (Mise à jour ciblée)
        for school_name in schools_in_csv:
            # نلقاو أو نكرييو المدرسة
            school, created = School.objects.get_or_create(
                name=school_name,
                defaults={
                    'slug': slugify(school_name) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
                    'api_key': ''.join(random.choices(string.digits, k=6))
                }
            )

            # 🛑 نمسحو تلاميذ هاد المدرسة فقط !! (ماشي كولشي)
            count_deleted, _ = Student.objects.filter(school=school).delete()
            self.stdout.write(self.style.WARNING(f'♻️ Mise à jour de "{school_name}": {count_deleted} anciens élèves supprimés.'))

            # نعاودو ندخلوهم
            count_added = 0
            for item in students_to_create:
                if item['school_name'] == school_name:
                    row = item['row']
                    Student.objects.create(
                        school=school,
                        code_id=row['num'],
                        first_name=row['prenom'],
                        last_name=row['nom'],
                        class_name=row['classe'],
                        group=row['groupe'],
                        cndp=row['CNDP'],
                        badge_number=row['BADGE']
                    )
                    count_added += 1
            
            self.stdout.write(self.style.SUCCESS(f'✅ "{school_name}": {count_added} élèves ajoutés.'))