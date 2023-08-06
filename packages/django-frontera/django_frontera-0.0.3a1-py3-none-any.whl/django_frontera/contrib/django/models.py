from django.db import models
from django.utils.translation import ugettext_lazy

class AbstractModel(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=ugettext_lazy('Creation date'))
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=ugettext_lazy('Edition date'))
    hidden = models.BooleanField(
        default=False,
        verbose_name=ugettext_lazy('Hidden'))

    class Meta:
        abstract = True

class BaseModel(AbstractModel):
    name = models.CharField(
        max_length=80,
        verbose_name=_('Title'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class SelectableModel(BaseModel):
    class Meta:
        abstract = True

    @classmethod
    def get_list(cls, showHidden=False):
        return cls.objects.filter(hidden=not showHidden).order_by('-id')

    def get_absolute_url(self):
        return '/'
