from django.shortcuts import render, redirect
from .forms import TechNoteForm
from PIL import Image, ImageFont, ImageDraw
from helper_files.jpeg_to_dicom import generate_dicom_from_image
import textwrap
import os
from pydicom import dcmread
from pydicom.uid import UID
from pynetdicom import AE


# Create your views here.


def tech_form(request):
    form = TechNoteForm()
    context = {
        "form": form,
    }
    return render(request, 'tech_forms/tech_form.html', context)


def tech_form_submit(request):
    form = TechNoteForm(request.POST)
    errors = form.errors

# form data
    modality = f"Modality: {request.POST['modality']}"
    patient_id = f"Patient ID: {request.POST['patient_id']}"
    patient_name = f"Patient Name: {request.POST['patient_name']}"
    exam_date = f"Exam Date: {request.POST['exam_date']}"
    accession = f"Accession#: {request.POST['accession']}"
    procedure = f"Procedure: {request.POST['procedure']}"
    comments = f"Comments: {request.POST['comments']}"
    tech_initials = f"Tech Initials: {request.POST['tech_initials']}"

    form_data = [modality, patient_id, patient_name, exam_date,
                 accession, procedure, comments, tech_initials]

# write form data to JPEG
    img = Image.new('RGB', (812, 1052), 'white')
    font = ImageFont.truetype("arial.ttf", 20)
    starting_height = 10

    for item in form_data:
        lines = textwrap.wrap(item, width=80)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw = ImageDraw.Draw(img)
            draw.text((10, starting_height), line, font=font, fill="black")
            starting_height += (line_height + 5)

    img.save('tech_note.jpg', "JPEG")

# convert jpeg to DICOM
    output = generate_dicom_from_image('tech_note.jpg', modality=request.POST['modality'], patient_id=request.POST['patient_id'],
                                       patient_name=request.POST['patient_name'], procedure=request.POST['procedure'], tech_initials=request.POST['tech_initials'], accession=request.POST['accession'])

    output.save_as("tech_note.dcm")

# send to PACS

    scu_ae = os.environ.get('AE_TITLE')
    dest_ae = os.environ.get('DEST_AE')
    dest_ip = os.environ.get('DEST_IP')

    ae = AE(ae_title=scu_ae)
    # this uid is for secondary image capture
    uid = UID('1.2.840.10008.5.1.4.1.1.7')
    ae.add_requested_context(uid)

    ds = dcmread('tech_note.dcm')

    assoc = ae.associate(dest_ip, 5000, ae_title=dest_ae)

    if assoc.is_established:
        print('Associated')
        status = assoc.send_c_store(ds)

        if status:
            dicom_message = 'C-STORE request status: 0x{0:04x}'.format(
                status.Status)
        else:
            dicom_message = 'Connection timed out, was aborted or received invalid resposne'

        assoc.release()
    else:
        dicom_message = 'Association rejected, aborted or never connected'

    context = {
        "errors": errors,
        "dicom_message": dicom_message
    }

    if form.is_valid():
        return render(request, 'tech_forms/form_submitted.html', context)
    else:
        return render(request, 'tech_forms/form_submitted.html', context)
