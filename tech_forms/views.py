from django.shortcuts import render

# Create your views here.


def tech_form(request):
    return render(request, 'tech_forms/tech_form.html')
