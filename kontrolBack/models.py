from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


control_status = [
    (0, 'w przygotowaniu'),
    (1, 'w trakcie'),
    (2, 'w procesie zgłaszania uwag do wyniku'),
    (3, 'zakończona'),
]

answer_choices = [
    (0, 'tak'),
    (1, 'nie'),
    (2, 'nie dotyczy')
]


class Institution (models.Model):
    programme = models.CharField(max_length=10)  # todo: add programme model
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=512)
    is_coordinator = models.BooleanField(default=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'instytucje'


class InstitutionEmployee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    institution = models.ForeignKey(to=Institution, on_delete=models.CASCADE)


class Project(models.Model):
    programme = models.CharField(max_length=10)  # todo: add programme model
    code = models.CharField(max_length=512)
    name = models.CharField(max_length=512)
    beneficiary_name = models.CharField(max_length=512)
    beneficiary_nip = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class QuestionBlock(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='blok')
    # block_order = models.IntegerField(default=99, null=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'bloki pytań'


class Question (models.Model):
    name = models.CharField(max_length=500, unique=True)
    block = models.ForeignKey(
        to=QuestionBlock, related_name='questions', on_delete=models.PROTECT)
    order_in_block = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'pytania'


# założenie: 1 checklista do 1 kontroli w 1 podmiocie

class Checklist(models.Model):
    name = models.CharField(max_length=255, verbose_name='nazwa')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        to=InstitutionEmployee, related_name='checklists',
        on_delete=models.PROTECT, null=True)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('checklist_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Control (models.Model):
    name = models.CharField(max_length=2000, verbose_name='nazwa')
    project = models.ForeignKey(
        to=Project, related_name="controls_at_project",
        on_delete=models.PROTECT, verbose_name='projekt')
    controlling = models.ForeignKey(
        to=Institution, related_name="controls_by",
        verbose_name='instytucja kontrolująca', on_delete=models.PROTECT)
    date_start = models.DateTimeField(verbose_name='początek')
    date_end = models.DateTimeField(verbose_name='koniec')
    checklist = models.ForeignKey(
        to=Checklist, null=True, blank=True, on_delete=models.PROTECT,
        related_name='controls', verbose_name='lista sprawdzająca')
    status = models.IntegerField(choices=control_status, default=0)


# pytanie wybrane do listy jest dla niej "mrożone"
# tj. nie zmienia się po zmianie pytania bazowego w modelu Question
# i tak samo jest z blokiem

class QuestionInList (models.Model):
    question_name = models.CharField(max_length=500)
    block_name = models.CharField(max_length=255)
    checklist = models.ManyToManyField(to=Checklist, related_name='questions')


class QuestionInControl (models.Model):
    question_name = models.CharField(max_length=500)
    block_name = models.CharField(max_length=255)
    control = models.ForeignKey(
        to=Control, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question_name

    def __repr__(self):
        return self.question_name


class Answer(models.Model):
    question = models.OneToOneField(
        to=QuestionInControl, on_delete=models.PROTECT, verbose_name="pytanie")
    content = models.IntegerField(
        choices=answer_choices, verbose_name="odpowiedź")
    comment = models.CharField(
        max_length=10000, null=True, blank=True, verbose_name="komentarz")


class ResultInfo (models.Model):
    control = models.OneToOneField(to=Control, on_delete=models.PROTECT)


class Finding(models.Model):
    result_info = models.ForeignKey(
        to=ResultInfo, related_name='findings', on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)


class Recommendation (models.Model):
    result_info = models.ForeignKey(
        to=ResultInfo, related_name='recommendations',
        on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)
