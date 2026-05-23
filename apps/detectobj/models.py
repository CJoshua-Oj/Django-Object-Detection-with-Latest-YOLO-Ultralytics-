import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from config.models import CreationModificationDateBase


class InferencedImage(CreationModificationDateBase):
    orig_image = models.ForeignKey(
        "images.ImageFile",
        on_delete=models.CASCADE,
        related_name="detectedimages",
        help_text="Main Image",
        null=True,
        blank=True
    )

    inf_image_path = models.CharField(max_length=250,
                                      null=True,
                                      blank=True
                                      )

    custom_model = models.ForeignKey("modelmanager.MLModel",
                                     verbose_name="Custom ML Models",
                                     on_delete=models.DO_NOTHING,
                                     null=True,
                                     blank=True,
                                     related_name="detectedimages",
                                     help_text="Machine Learning model for detection",
                                     )
    detection_info = models.JSONField(null=True, blank=True)

    YOLOMODEL_CHOICES = [
        ('yolo26n.pt', 'yolo26n.pt - latest/default'),
        ('yolo26s.pt', 'yolo26s.pt'),
        ('yolo11n.pt', 'yolo11n.pt - stable fallback'),
        ('yolo11s.pt', 'yolo11s.pt'),
        ('yolov8n.pt', 'yolov8n.pt - compatibility fallback'),
    ]

    yolo_model = models.CharField(_('Ultralytics YOLO Models'),
                                  max_length=250,
                                  null=True,
                                  blank=True,
                                  choices=YOLOMODEL_CHOICES,
                                  default=YOLOMODEL_CHOICES[0][0],
                                  help_text="Selected Ultralytics YOLO model will download. \
                                 Requires an active internet connection."
                                  )

    model_conf = models.DecimalField(_('Model confidence'),
                                     decimal_places=2,
                                     max_digits=4,
                                     null=True,
                                     blank=True)
