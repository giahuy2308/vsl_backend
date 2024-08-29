from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Question, Choice, Content, Animation, Image, Lesson, Section, Topic, Chapter

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

def get_foreign_key_related_objects(instance):
    foreign_key_field = None
    for field in instance._meta.get_fields():
        if isinstance(field, ForeignKey):
            foreign_key_field = field  # Gán giá trị cho foreign_key_field
            related_field_name = field.name
            break

    if foreign_key_field is None:
        raise ValueError("Instance không có liên kết ForeignKey nào.")


    return type(instance).objects.filter(
        **{related_field_name: getattr(instance, related_field_name)}
    )

    

def update_obj_no(instance, is_insert_instance):
    all_objs = list(get_foreign_key_related_objects(instance))
    
    if is_insert_instance:
        all_objs.remove(instance)
        all_objs.insert(instance.no, instance)

    for i, obj in enumerate(all_objs):
        if obj.no != i:
            obj.no = i 
            obj.save(update_fields=['no'])

@receiver(post_save, sender=Topic)
@receiver(post_save, sender=Chapter)
@receiver(post_save, sender=Section)
@receiver(post_save, sender=Lesson)
def create_or_update_obj(sender, instance, created, **kwargs):
    if created:
        if instance.no == -1:    
            instance.no = len(get_foreign_key_related_objects(instance)) + 1
            instance.save(update_fields=['no'])
    update_obj_no(instance, True)
        
@receiver(post_save, sender=Topic)
@receiver(post_save, sender=Chapter)
@receiver(post_delete, sender=Section)
@receiver(post_delete, sender=Lesson)
def update_obj_no_after_delete(sender, instance, **kwargs):
    update_obj_no(instance, False)


def update_section_content_no(instance, is_insert_instance):
    sec = instance.section
    scl = list(sec.contents.all()) + list(sec.images.all()) + list(sec.animations.all())
    scl.sort(key=lambda obj: obj.no)
    if is_insert_instance:
        scl.remove(instance)
        scl.insert(instance.no, instance)

    for i, v in enumerate(scl):
        if v.no != i:
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
        if instance.no == -1:
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
