from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from modelcluster.tags import ClusterTaggableManager
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
    title = models.CharField(
        max_length=80,
        verbose_name=_('Title'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class PageModel(BaseModel):
    seo_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("SEO Title"),
        help_text=_("Optional. 'Search Engine Friendly' title. This will appear at the top of the browser window."))
    slug = models.SlugField(
        allow_unicode=True,
        max_length=255,
        verbose_name=_("Slug"),
        help_text=_("The name of the page as it will appear in URLs e.g http://domain.com/blog/[my-slug]/"))
    search_description = models.TextField(
        verbose_name=_('Search Description'),
        blank=True)
    keywords = ClusterTaggableManager(
        through=settings.WAGTAIL_KEYWORD_MODEL,
        blank=True,
        related_name='%(class)s+',
        verbose_name=_('Keywords'))
    include_in_sitemap = models.BooleanField(
        default=True,
        help_text=_('Should this page appear in the sitemap'))
    show_in_menus = models.BooleanField(
        default=False,
        verbose_name=_('Show in menus'),
        help_text=_("Whether a link to this page will appear in automatically generated menus"))
    # url_path = models.TextField(verbose_name=_('URL path'), blank=True, editable=False)
    url_reverse_name = None


    class Meta:
        abstract = True

    def get_url(self, kwargs={}):
        url = '/'
        if self.url_reverse_name and self.slug:
            props = {
                'pk': self.id,
                'slug': self.slug,
            }
            url = reverse(self.url_reverse_name, kwargs=dict(kwargs, **props))
        return url

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class SelectableModel(PageModel):
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

