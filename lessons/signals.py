from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Question, Choice, Content, Animation, Image, Lesson, Section

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

def update_obj_no(instance, model, is_insert_instance):
    all_objs = list(model.objects.all())
    if is_insert_instance:
        all_objs.remove(instance)
        all_objs.insert(instance.no - 1, instance)

    for i, obj in enumerate(all_objs, 1):
        if obj.no != i :
            obj.no = i 
            obj.save(update_fields=['no'])

@receiver(post_save, sender=Section)
@receiver(post_save, sender=Lesson)
def create_or_update_obj(sender, instance, created, **kwargs):
    if created:
        if instance.no == 0:
            instance.no = len(sender.objects.all()) + 1
            instance.save(update_fields=['no'])
    update_obj_no(instance, sender, True)
        
@receiver(post_delete, sender=Section)
@receiver(post_delete, sender=Lesson)
def delete_lesson(sender, instance, **kwargs):
    update_obj_no(instance, sender, False)


def update_section_content_no(instance, is_insert_instance):
    sec = instance.section
    scl = list(sec.contents.all()) + list(sec.images.all()) + list(sec.animations.all())
    scl.sort(key=lambda obj: obj.no)
    if is_insert_instance:
        scl.remove(instance)
        scl.insert(instance.no - 1, instance)

    for i, v in enumerate(scl, 1):
        if v.no != i :
            v.no = i 
            v.save(update_fields=['no'])

    # Cập nhật lại số lượng nội dung cho section
    sec.save(update_fields=["content_quantity"])

def delete_section_content(instance):
    instance.section.content_quantity -= 1
    update_section_content_no(instance, False)

def create_or_update_section_content(instance,created):
    if created:
        instance.section.content_quantity += 1
        if instance.no == 0:
            instance.no = instance.section.content_quantity
            instance.save(update_fields=['no'])
    update_section_content_no(instance, True)

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
