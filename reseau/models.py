from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author'))
    title = models.CharField(_('Title'), max_length=255, blank=False, null=False) 
    text = models.TextField(_('Text'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    created_at = models.DateTimeField(_('Creation Date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update Date'), auto_now=True)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f"{self.author} - {self.title}"

class PostChannel(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    channel_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    channel_object = GenericForeignKey('channel_type', 'object_id')

    class Meta:
        verbose_name = _('Post Channel')
        verbose_name_plural = _('Post Channels')

    def __str__(self):
        return f"{self.post.title} - {self.channel_type}"

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

class PostAttachment(models.Model):
    post = models.ForeignKey(Post, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_attachments/', validators=[validate_file_extension])

    def __str__(self):
        return f"{self.post.title} attachment"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    content = models.TextField(_('Content'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f"{self.user} - {self.content[:20]}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('haha', '😂'),
        ('wow', '😮'),
        ('sad', '😢'),
        ('angry', '😠'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    reaction = models.CharField(_('Reaction'), max_length=5, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Reaction')
        verbose_name_plural = _('Reactions')

    def __str__(self):
        return f"{self.user} - {self.post} - {self.reaction}"
