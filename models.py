from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.db import IntegrityError, transaction
from apps.images.models import Image
from pure.apps.froala_editor.fields import FroalaField
# from wadibyte.wadicore.models import Image
# from wadibyte.wadimaps.models import City
from taggit.managers import TaggableManager
# from alfuhigi.hash import AlphaID
from alfuhigi import CodeGenerator
from alfuhigi.mixin import QuerySetMixin
from alfuhigi.models import ActiveAbstract, UUIdAbstract
from .choices import KIND_CHOICES

# Create your models here.
#.

class SehhaQuerySet(models.QuerySet, QuerySetMixin):
    pass
    # def disp(self):
    #     return self.filter(kind=1)
    # def hosp(self):
    #     return self.filter(kind=2)


class Organization(ActiveAbstract, UUIdAbstract):
    objects = SehhaQuerySet.as_manager()
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(null=True, editable=False, unique=True)

    phone = models.CharField(max_length=100, null=True,)
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    images = GenericRelation(Image)
    address = models.CharField(max_length=100, null=True)
    lat = models.CharField(max_length=20, null=True)
    lng = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True, blank=True)
    working_time = models.CharField(max_length=100, null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        pass
        # app_label = 'org'
        permissions = (
            ('can_view_odd_ids', 'can_view_odd_ids'),
            ('can_view_even_ids', 'can_view_even_ids'),
         )

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = self.code_generate(Organization, size=9)
            self.slug = slugify(self.name, allow_unicode=True)

        super(Organization, self).save(*args, **kwargs)
    #  with transaction.atomic():
    # super(Organization,self).save(*args,**kwargs)
    def as_dic(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'phone': self.phone,
            'fax': self.fax,
            'email': self.email,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'content': self.content,
            'working_time': self.working_time
            }
            
    def get_list_url(self):
        return reverse('org-list')

    def get_create_url(self):
        return reverse('org-create')

    def get_absolute_url(self):
        return reverse('org-detail', kwargs={'slug': self.slug, 'uuid': self.uuid})

    def get_update_url(self):
        return reverse('org-update', kwargs={'uuid': self.uuid})

    def get_delete_url(self):
        return reverse('org-delete', kwargs={'uuid': self.uuid})

    def __str__(self):
        return '{} '.format(self.name) or None


class Unit(models.Model):

    organization = models.ForeignKey(to='Organization', blank=True,
                                        related_name='unit')

    name = models.CharField(max_length=100, null=True, blank=True)

    image = models.ForeignKey(Image, null=True, blank=True)
    working_time = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return 'Organization:{}, Unit:{}'.format(self.organization.name,
                                                 self.name)


class Page(ActiveAbstract, UUIdAbstract):
    objects = SehhaQuerySet.as_manager()
    title = models.CharField(max_length=100, null=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    thumbnail = models.ForeignKey(Image, null=True, blank=True)
    org = models.ForeignKey(to='Organization', null=True, blank=True,
                            related_name='page_org')
    tags = TaggableManager()
    body = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = self.code_generate(model=Page, size=4,
                                           mod='mixcase_digits')
        self.slug = slugify(self.title, allow_unicode=True)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_list_url(self):
        return reverse('news-list')

    def get_create_url(self):
        return reverse('news-create')

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('news-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('news-delete', kwargs={'pk': self.pk})
