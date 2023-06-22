from django.conf import settings
from  django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_activated
from Profile.models import Person , CommenPeople , Organization , TourLeader

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_person_for_new_user(sender , **kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        person = Person.objects.create(user_id = instance)
        if instance.role == "C":
            CommenPeople.objects.create(Id = person)
        elif instance.role == "O":
            Organization.objects.create(person_id = instance , name_org = instance.username)#i assign name otherwise for second value we get two time null (this field is unique)
        elif instance.role == "T":
            TourLeader.objects.create(person_id = person)


    

# connect the create_person function to the user_registered signal
user_activated.connect(create_person_for_new_user)