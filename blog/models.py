from django.db import models
from django_prose_editor.fields import ProseEditorField
from django.conf import settings
from django.utils import timezone
from datetime import datetime, time, timedelta


class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.slug})"


class PostManager(models.Manager):
    def published(self, published: bool = True):
        return self.filter(published=published)

    def recent_published(self, limit=10):
        last_week = timezone.localdate() - timedelta(days=7)
        last_week = timezone.make_aware(
            datetime.combine(last_week, time.min),
            timezone.get_current_timezone(),
        )
        now = timezone.now()
        return (
            self.published()
            .filter(published_at__lte=now, published_at__gte=last_week)
            .order_by("-published_at")[:limit]
        )

    def user_blogs(self, user):
        self.filter(author=user).order_by("-updated_at")


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="post_covers/")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = ProseEditorField(
        extensions={
            # Core text formatting
            "Bold": True,
            "Italic": True,
            "Strike": True,
            "Underline": True,
            "HardBreak": True,
            # Structure
            "Heading": {
                "levels": [1, 2, 3]  # Only allow h1, h2, h3
            },
            "BulletList": True,
            "OrderedList": True,
            "ListItem": True,  # Used by BulletList and OrderedList
            "Blockquote": True,
            # Advanced extensions
            "Link": {
                "enableTarget": True,  # Enable "open in new window"
                "protocols": ["http", "https", "mailto"],  # Limit protocols
            },
            "Table": True,
            "TableRow": True,
            "TableHeader": True,
            "TableCell": True,
            # Editor capabilities
            "History": True,  # Enables undo/redo
            "HTML": True,  # Allows HTML view
            "Typographic": True,  # Enables typographic chars
        },
        sanitize=True,
        config={"theme": "light"},
    )
    # content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)

    objects = PostManager()

    def save(self, *args, **kwargs):
        # Set value to published_at field if it's None & published field is enabled
        if self.published_at is None and self.published:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
