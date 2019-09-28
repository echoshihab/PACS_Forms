from django.shortcuts import render, redirect
from .forms import TechNoteForm, QueryWorklistForm
from PIL import Image, ImageFont, ImageDraw
from helper_files.jpeg_to_dicom import generate_dicom_from_image
import textwrap
import os
from pydicom import dcmread
from pydicom.uid import UID
from pynetdicom import AE
from pydicom.dataset import Dataset
from pynetdicom.sop_class import ModalityWorklistInformationFind
from server_configs.models import DestinationConfigs, WorklistConfigs, WorkstationConfigs


def home_page(request):
    return render(request, 'tech_forms/home.html')


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

    scu_ae = WorkstationConfigs.objects.get(id=1).workstation_ae

    destination_configs = DestinationConfigs.objects.get(id=1)

    dest_ae = destination_configs.destination_ae
    dest_ip = destination_configs.destination_ip
    dest_port = destination_configs.destination_port

    ae = AE(ae_title=scu_ae)
    # this uid is for secondary image capture
    uid = UID('1.2.840.10008.5.1.4.1.1.7')
    ae.add_requested_context(uid)

    ds = dcmread('tech_note.dcm')

    assoc = ae.associate(dest_ip, dest_port, ae_title=dest_ae)

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


def query_worklist(request):

    if request.method == 'POST':
        accession = request.POST['accession']

        # Query Worklist by accession
        scu_ae = os.environ.get('AE_TITLE')

        # SCU
        ae = AE(ae_title=scu_ae)

        ae.add_requested_context(ModalityWorklistInformationFind)

        ds = Dataset()
        ds.PatientName = '*'
        ds.AccessionNumber = accession
        ds.PatientID = ''
        ds.StudyInstanceUID = ''
        ds.QueryRetrieveLevel = 'STUDY'
        ds.ScheduledProcedureStepSequence = [Dataset()]
        item = ds.ScheduledProcedureStepSequence[0]
        item.modality = 'US'

        # associate with SCP
        scp_ip = os.environ.get('SCP_IP')
        scp_ae = os.environ.get('SCP_AE')
        assoc = ae.associate(scp_ip, 5010, ae_title=scp_ae)

        if assoc.is_established:
            responses = assoc.send_c_find(
                ds, ModalityWorklistInformationFind)

            for(status, identifier) in responses:
                if status:
                    print(
                        'C-FIND query status: 0x{0:04x}'.format(status.Status))
                    if status.Status in (0xFF00, 0xFF01):
                        study_data = identifier
                        error = "No Errors"
                else:
                    error = "Connection timed out, was aborted or receieved invalid response"

            assoc.release()
        else:
            study_data = 'Associated rejected, aborted or never connected'

        query_form = TechNoteForm()

        context = {
            'study_data': study_data,
            'patient_name': study_data[0x10, 0x10].value,
            'patient_id': study_data[0x10, 0x20].value,
            'accession': study_data[0x08, 0x50].value,
            'StudyInstanceUID': study_data[0x20, 0x0d].value,
            'modality': study_data.ScheduledProcedureStepSequence[0][0x08, 0x60].value,
            'study_date': study_data.ScheduledProcedureStepSequence[0][0x40, 0x02].value,
            'study_description': study_data.ScheduledProcedureStepSequence[0][0x40, 0x07].value,
            'error': error,
            'query_form': query_form,

        }

        return render(request, 'tech_forms/query_worklist.html', context)

    else:

        form = QueryWorklistForm()

        context = {
            "form": form
        }

        return render(request, 'tech_forms/query_worklist.html', context)
