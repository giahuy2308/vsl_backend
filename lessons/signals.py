from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Question, Choice, Content, Animation, Image

@receiver(post_save, sender=Question)
def create_or_update_choice(sender, instance, created, **kwargs):
    if created:
        Choice.objects.create(question=instance, title=instance.answer)
    else:    
        try:
            choice = Choice.objects.get(question=instance)
            choice.title = instance.answer
            choice.save(update_fields=["title"])
        except Choice.DoesNotExist:
            Choice.objects.create(question=instance, title=instance.answer)

def update_no(instance, is_update):
    sec = instance.section
    scl = list(Content.objects.filter(section=sec)) + list(Image.objects.filter(section=sec)) + list(Animation.objects.filter(section=sec))
    if is_update:
        scl.remove(instance)
        scl = scl[0:instance.no-1] + [instance] + scl[instance.no-1:]
    for i in range(len(scl)):
        # Sử dụng update() thay vì save() để tránh kích hoạt signal
        scl[i].__class__.objects.filter(pk=scl[i].pk).update(no=i+1)

    # Cập nhật lại số lượng nội dung cho section
    sec.save(update_fields=["content_quantity"])

def delete_section_content(instance):
    instance.section.content_quantity -= 1
    update_no(instance, False)

def create_or_update_section_content(instance,created):
    if created:
        instance.section.content_quantity += 1
    update_no(instance, True)


@receiver(post_save, sender=Content)
@receiver(post_save, sender=Image)
@receiver(post_save, sender=Animation)
def handle_content_image_animation(sender, instance, created, **kwargs):
    create_or_update_section_content(instance,created)


@receiver(post_delete, sender=Content)
@receiver(post_delete, sender=Image)
@receiver(post_delete, sender=Animation)
def handle_content_image_animation(sender, instance, **kwargs):
    delete_section_content(instance)