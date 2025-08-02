from django.db.models.signals import post_save ,pre_save,post_delete
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
@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    if not instance.pk:
        return  # It's a new message, no edit yet

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Mark message as edited
        instance.edited = True

        # Log the old content
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.edited_by  # Assumes edited_by is set in the view
        )

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
