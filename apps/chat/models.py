from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User

from shared.mixins.model_utils import CreatedUpdateMixins


class Room(CreatedUpdateMixins):
    name = models.CharField(
        max_length=64,
        verbose_name=_('name'),
        help_text=_('room name')
    )
    readers = models.ManyToManyField(
        User,
        verbose_name=_('readers'),
        help_text=_('room readers')
    )
    private = models.BooleanField(
        default=True,
        verbose_name=_('private'),
        help_text=_('room privacy')
    )

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('Rooms')

        def __str__(self) -> str:
            if self.private:
                return '/'.join(map(lambda user: user, self.readers))
            return self.name


class Message(CreatedUpdateMixins):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('author'),
        help_text=_('message author')
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('room'),
        help_text=_('discussion room')
    )
    content = models.CharField(
        max_length=500,
        verbose_name=_('content'),
        help_text=_('message content')
    )
    status = models.BooleanField(
        default=False,
        verbose_name=_('status'),
        help_text=_('read message status')
    )

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('Messages')

        def __str__(self) -> str:
            return self.author
