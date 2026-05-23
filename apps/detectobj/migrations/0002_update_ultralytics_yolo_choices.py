from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ('detectobj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inferencedimage',
            name='yolo_model',
            field=models.CharField(
                _('Ultralytics YOLO Models'),
                blank=True,
                choices=[
                    ('yolo26n.pt', 'yolo26n.pt - latest/default'),
                    ('yolo26s.pt', 'yolo26s.pt'),
                    ('yolo11n.pt', 'yolo11n.pt - stable fallback'),
                    ('yolo11s.pt', 'yolo11s.pt'),
                    ('yolov8n.pt', 'yolov8n.pt - compatibility fallback'),
                ],
                default='yolo26n.pt',
                help_text='Selected Ultralytics YOLO model will download. Requires an active internet connection.',
                max_length=250,
                null=True,
            ),
        ),
    ]
