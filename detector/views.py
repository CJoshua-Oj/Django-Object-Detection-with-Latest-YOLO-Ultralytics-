import os
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseServerError, StreamingHttpResponse
from django.shortcuts import render

from .forms import ImageUploadForm
from .yolo_camera import generate_frames
from .yolo_engine import load_yolo_model, result_to_detections, save_plotted_result


def home(request):
    return render(request, 'detector/home.html')


def video_feed(request):
    try:
        return StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as error:
        return HttpResponseServerError(f"Camera error: {error}")


def image_detection(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            image = request.FILES['image']
            upload_path = Path(settings.MEDIA_ROOT) / image.name

            with open(upload_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            model = load_yolo_model()
            result = model.predict(
                source=str(upload_path),
                conf=getattr(settings, "MODEL_CONFIDENCE", 0.45),
                imgsz=640,
                verbose=False,
            )[0]

            detected_name = f"detected_{image.name}"
            detected_path = Path(settings.MEDIA_ROOT) / detected_name
            save_plotted_result(result, detected_path)

            detections = result_to_detections(result)

            return render(request, 'detector/image_result.html', {
                'image_url': settings.MEDIA_URL + detected_name,
                'detections': detections,
            })
    else:
        form = ImageUploadForm()

    return render(request, 'detector/image_upload.html', {'form': form})
