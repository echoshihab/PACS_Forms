from django.shortcuts import render, redirect
from .forms import TechNoteForm

# Create your views here.


def tech_form(request):
    form = TechNoteForm()
    context = {
        "form": form,
    }
    return render(request, 'tech_forms/tech_form.html', context)


def tech_form_submit(request):
    form = TechNoteForm(request.POST)

    if form.is_valid():
        return render(request, 'tech_forms/form_submitted.html')
    else:
        return render(request, 'tech_forms/form_submitted.html')
