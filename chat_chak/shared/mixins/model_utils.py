from datetime import datetime

from django.db import models
from slugify import slugify


class CreatedUpdateMixins(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageNameMixins:
    @staticmethod
    def get_image_name(name, filename):
        extension = filename.split('.')[-1]
        return f'{name}-{datetime.now()}.{extension}'

    def get_current_image_name(self, model):
        if self.pk is not None:
            orig = model.objects.get(pk=self.pk)
            if orig.image.name != self.image.name:
                if self.image:
                    name = self.get_image_name(name=self.name, filename=self.image.name)
                    return {'image_name': name, 'new': True}
            else:
                return {'new': False}
        else:
            name = self.get_image_name(name=self.name, filename=self.image.name)
            return {'image_name': name, 'new': True}


def get_image_name(name, filename):
    extension = filename.split('.')[-1]
    return f'{name}-{datetime.now()}.{extension}'


class SlugImageSaveMixin:

    def save_slug_and_image(self, model):
        self.slug = slugify(self.slug or self.name)
        if self.image:
            field_name_image = self.get_current_image_name(model=model)
            if field_name_image['new']:
                self.image.name = field_name_image['image_name']
            if not self.img_alt and self.image:
                self.img_alt = self.name
