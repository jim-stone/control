from django.contrib.auth.models import User
from .models import Institution, Control


def user_has_perm_to_object (user, obj):

    user_institution = Institution.objects.get(pk=user.institutionemployee.institution.pk)

    if isinstance(obj, Control):
        obj_institution = obj.controlling
        return user_institution.programme == obj_institution.programme