from django.shortcuts import render, get_object_or_404
from .models import Website

def qr_code_list(request):
    websites = Website.objects.all()
    return render(request, 'qr_list.html', {'websites': websites})


def website_detail(request, slug):
    website = get_object_or_404(Website, slug=slug)
    return render(request, 'qrgenerator/website_detail.html', {'website': website})