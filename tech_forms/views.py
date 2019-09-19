from django.shortcuts import render
from .forms import TechNoteForm

# Create your views here.


def tech_form(request):
    tech_note_form = TechNoteForm()
    context = {
        "tech_note_form": tech_note_form,
    }
    return render(request, 'tech_forms/tech_form.html', context)
