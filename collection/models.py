from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.


# class CollectionManager(models.Manager):
#     def active(self, *args, **kwargs):
#         return super(CollectionManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    privacy = models.NullBooleanField(default=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # objects = CollectionManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("collection:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-update", "-id"]


class Tag(models.Model):
	name = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["-timestamp"]


class Link(models.Model):
    title = models.CharField(max_length=120)
    link = models.TextField()
    domain = models.CharField(max_length=300)
    img = models.CharField(max_length=300)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
    	return self.title

    def __str__(self):
    	return self.title

    class Meta:
	   ordering = ["-timestamp"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs = Collection.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug= new_slug)
    return slug


def pre_save_collection_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_collection_receiver, sender=Collection)
