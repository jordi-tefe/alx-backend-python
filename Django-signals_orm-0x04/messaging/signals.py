from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification ,MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
@receiver(post_save, sender=Message)
def log_message_update(sender, instance, created, **kwargs):
    if not created:
        print(f"[LOG] Message ID {instance.id} was updated. New content: {instance.content}")

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                # Log to MessageHistory
                MessageHistory.objects.create(
                    message=old_instance,
                    previous_content=old_instance.content,
                    edited_by=instance.edited_by
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
