from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Author

@receiver(post_save, sender=Author)
def after_author_save(sender, instance, created, **kwargs):
    if created:
        print(f"Author '{instance.name}' was created!")
    else:
        print(f"Author '{instance.name}' was updated!")

@receiver(pre_save, sender=Author)
def before_author_save(sender, instance, **kwargs):
    if not instance.pk:
        print(f"About to create a new Author '{instance.name}'")
    else:
        print(f"About to update Author '{instance.name}'")

@receiver(pre_delete, sender=Author)
def before_author_delete(sender, instance, **kwargs):
    print(f"Author '{instance.name}' is about to be deleted!")

@receiver(post_delete, sender=Author)
def after_author_delete(sender, instance, **kwargs):
    print(f"Author '{instance.name}' has been deleted!")
