import os
import io
from PIL import Image as I
import torch
import collections

from .yolo_utils import load_model, result_to_records, save_result_image

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator

from images.models import ImageFile
from .models import InferencedImage
from .forms import InferencedImageForm, YoloModelForm
from modelmanager.models import MLModel


class InferenceImageDetectionView(LoginRequiredMixin, DetailView):
    model = ImageFile
    template_name = "detectobj/select_inference_image.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img_qs = self.get_object()
        imgset = img_qs.image_set
        images_qs = imgset.images.all()

        # For pagination GET request
        self.get_pagination(context, images_qs)

        if is_inf_img := InferencedImage.objects.filter(
            orig_image=img_qs
        ).exists():
            inf_img_qs = InferencedImage.objects.get(orig_image=img_qs)
            context['inf_img_qs'] = inf_img_qs

        context["img_qs"] = img_qs
        context["form1"] = YoloModelForm()
        context["form2"] = InferencedImageForm()
        return context

    def get_pagination(self, context, images_qs):
        paginator = Paginator(
            images_qs, settings.PAGINATE_DETECTION_IMAGES_NUM)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["is_paginated"] = (
            images_qs.count() > settings.PAGINATE_DETECTION_IMAGES_NUM
        )
        context["page_obj"] = page_obj

    def post(self, request, *args, **kwargs):
        img_qs = self.get_object()
        img_bytes = img_qs.image.read()
        img = I.open(io.BytesIO(img_bytes)).convert("RGB")

        # Get form data
        modelconf = self.request.POST.get("confidence") or self.request.POST.get("model_conf")
        modelconf = float(modelconf) if modelconf else settings.MODEL_CONFIDENCE
        custom_model_id = self.request.POST.get("custom_model")
        yolo_model_name = self.request.POST.get("yolo_model") or settings.NEWEST_YOLO_MODEL

        detection_model = None
        if custom_model_id:
            detection_model = MLModel.objects.get(id=custom_model_id)
            model = load_model(detection_model.pth_filepath)
            selected_model_label = detection_model.name
        else:
            model = load_model(yolo_model_name)
            selected_model_label = yolo_model_name

        predictions = model.predict(source=img, conf=modelconf, imgsz=640, verbose=False)
        result = predictions[0]
        results_list = result_to_records(result)
        classes_list = [item["name"] for item in results_list]
        results_counter = collections.Counter(classes_list)

        if results_list == []:
            messages.warning(
                request,
                f'Model "{selected_model_label}" did not detect any object. Try another image or lower the confidence.'
            )
        else:
            media_folder = settings.MEDIA_ROOT
            inferenced_img_dir = os.path.join(media_folder, "inferenced_image")
            if not os.path.exists(inferenced_img_dir):
                os.makedirs(inferenced_img_dir)

            output_path = os.path.join(inferenced_img_dir, str(img_qs))
            save_result_image(result, output_path)

            # Create/update the inferencedImage instance
            inf_img_qs, created = InferencedImage.objects.get_or_create(
                orig_image=img_qs,
                defaults={"inf_image_path": f"{settings.MEDIA_URL}inferenced_image/{img_qs.name}"},
            )
            inf_img_qs.inf_image_path = f"{settings.MEDIA_URL}inferenced_image/{img_qs.name}"
            inf_img_qs.detection_info = results_list
            inf_img_qs.model_conf = modelconf
            if custom_model_id:
                inf_img_qs.custom_model = detection_model
                inf_img_qs.yolo_model = None
            else:
                inf_img_qs.yolo_model = yolo_model_name
            inf_img_qs.save()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # set image is_inferenced to true
        img_qs.is_inferenced = True
        img_qs.save()
        # Ready for rendering next image on same html page.
        imgset = img_qs.image_set
        images_qs = imgset.images.all()

        # For pagination POST request
        context = {}
        self.get_pagination(context, images_qs)

        context["img_qs"] = img_qs
        context["inferenced_img_dir"] = f"{settings.MEDIA_URL}inferenced_image/{img_qs}"
        context["results_list"] = results_list
        context["results_counter"] = results_counter
        context["form1"] = YoloModelForm()
        context["form2"] = InferencedImageForm()
        return render(self.request, self.template_name, context)
