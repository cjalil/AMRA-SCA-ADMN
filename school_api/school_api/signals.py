from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PickupRequest, PickupRequestBackup


@receiver(post_save, sender=PickupRequest)
def create_pickup_backup(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        PickupRequestBackup.objects.create( 
            original_pickup_id=instance.id,
            student_name=f"{instance.student.first_name} {instance.student.last_name}",
            class_name=instance.student.class_name or "",
            badge_number=instance.student.badge_number or "",
            school_name=instance.student.school.name,
            is_completed=instance.is_completed,
            porte_label=instance.porte_label,
            porte=instance.porte,
            device_id=instance.device_id,
            created_at_original=instance.created_at
        )
        print("✅ Backup created in DB")
    except Exception as e:
        print("❌ Backup signal error (ignored):", e)
        return
