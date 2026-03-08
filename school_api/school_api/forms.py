from django import forms
from .models import Student, SchoolClass  # ✅ Zid SchoolClass hna

class StudentForm(forms.ModelForm):
    class_name = forms.ChoiceField(label='Classe')

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'class_name', 'badge_number', 'code_id', 'cndp']
        
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'class_name': 'Classe',
            'badge_number': 'Numéro de Badge (Short ID)',
            'code_id': 'Code QR (Long ID)',
            'cndp': 'Code Massar / CNDP'
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        
        # ... (code d badge baqi kif ma howa) ...

        if school:
            # 1. Njibo ga3 classes (Students + Config)
            classes_from_students = set(Student.objects.filter(school=school)
                                        .exclude(class_name__isnull=True).exclude(class_name__exact='')
                                        .values_list('class_name', flat=True))
            
            classes_from_config = set(SchoolClass.objects.filter(school=school)
                                      .values_list('name', flat=True))

            all_classes_list = list(classes_from_students.union(classes_from_config))

            # === ✅ HNA TARTIB PERSO DYAL L-MADRASSA ===
            saved_order_str = school.class_order # "PS,MS,GS"
            
            if saved_order_str:
                # Nradoha liste: ['PS', 'MS', 'GS']
                saved_order = [x.strip() for x in saved_order_str.split(',') if x.strip()]
                
                # Nsawbo kharita: {'PS': 0, 'MS': 1, 'GS': 2}
                order_map = {name: i for i, name in enumerate(saved_order)}
                
                # Nrttbo: li kayna f map takhod nmra, li makaynach takhod 999
                all_classes_list.sort(key=lambda x: order_map.get(x, 999))
            else:
                # Ila l-madrassa ma dayrach tartib, ndiro alphabétique
                all_classes_list.sort()
            # ===========================================
 
            choices = [(c, c) for c in all_classes_list if c]
            choices.insert(0, ('', '-- Sans Classe --'))

            self.fields['class_name'].choices = choices
            self.fields['class_name'].widget.attrs.update({'class': 'form-select'})