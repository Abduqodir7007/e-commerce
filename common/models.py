from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class Media(models.Model):
    MEDIA_TYPE = (
        ("image", "image"),
        ("file", " file"),
        ("music", "music"),
        ("video", "video"),
    )
    type = models.CharField(max_length=255, choices=MEDIA_TYPE)
    file = models.FileField(
        upload_to="files/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "heic",
                    "heif",
                    "doc",
                    "pdf",
                    "mp3",
                    "mp4",
                    "flac",
                ]
            )
        ],
    )

    def __str__(self) -> str:
        return self.file.name

    class Meta:
        verbose_name_plural = "Media Files"

    def clean(self) -> None:
        if self.type == "image":
            if not self.file.name.endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError("wrong format")
        elif self.type == "file":
            if not self.file.name.endswith((".pdf", ".doc")):
                raise ValidationError("wrong format")
        elif self.type == "music":
            if not self.file.name.endswith((".mp3", ".flac")):
                raise ValidationError("wrong format")
        elif self.type == "video":
            if not self.file.name.endswith(("mp4")):
                raise ValidationError("wrong")
        else:
            raise ValidationError("File type is not valid")




class Settings(models.Model):
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.title[:10])

    class Meta:
        verbose_name_plural = "Settings"


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Region(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="regions"
    )

    def __str__(self) -> str:
        return self.name


class InstagramStory(models.Model):
    image = models.ForeignKey(
        Media, on_delete=models.CASCADE, related_name="instagram_story"
    )
    link = models.URLField()

    def __str__(self):
        return f"{self.image.file.name}"

    class Meta:
        verbose_name_plural = "Instagram Stories"


class CustomerFeedback(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    review = models.TextField()
    rank = models.IntegerField()
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedbacks"
