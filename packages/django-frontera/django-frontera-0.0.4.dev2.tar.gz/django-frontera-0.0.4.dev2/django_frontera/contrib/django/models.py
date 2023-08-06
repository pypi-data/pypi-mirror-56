from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel,\
    StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

class AbstractModel(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'))
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Edition date'))
    hidden = models.BooleanField(
        default=False,
        verbose_name=_('Hidden'))

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
    slug = models.SlugField(
        editable=False,
        max_length=80,
        verbose_name=_('Slug'))
    url_reverse_name = 'undefined'

    class Meta:
        abstract = True

    @classmethod
    def get_list(cls, showHidden=False, limit=5, desc=False):
        query = cls.objects
        if not showHidden:
            query = query.filter(hidden=False)
        if not desc:
            query = query.order_by('-id')
        return query[:limit]


    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug }
        return reverse(self.url_reverse_name, kwargs=kwargs)


    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
