from django.db import models


class Media(models.Model):
    MEDIA_TYPE = (
        ("image", "image"),
        ("file", " file"),
        ("music", "music"),
        ("video", "video"),
    )
    file = models.FileField(upload_to="files/", choices=MEDIA_TYPE)

    def __str__(self) -> str:
        return self.id


class Settings(models.Model):
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.id


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
        return f"{self.id}"


class CustomerFeedback(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    review = models.TextField()
    rank = models.IntegerField()
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
