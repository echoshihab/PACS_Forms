import textwrap
import os
import datetime
from django.shortcuts import render, redirect
from .forms import TechNoteForm, QueryWorklistForm
from PIL import Image, ImageFont, ImageDraw
from helper_files.jpeg_to_dicom import generate_dicom_from_image
from pydicom import dcmread
from pydicom.uid import UID
from pynetdicom import AE
from pydicom.dataset import Dataset
from pynetdicom.sop_class import ModalityWorklistInformationFind
from server_configs.models import DestinationConfigs, WorklistConfigs, WorkstationConfigs, UIDvalues


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

    # get uid root values from database
    uid_values = UIDvalues.objects.get(id=1)
    # make the uids
    study_instance_uid = uid_values.study_instance_uid + \
        '.' + str(uid_values.uid_counter + 1)
    series_instance_uid = uid_values.series_instance_uid + \
        '.' + str(uid_values.uid_counter + 1)
    sop_instance_uid = uid_values.series_instance_uid + \
        '.1.' + str(uid_values.uid_counter + 1)
    implementation_class_uid = uid_values.implementation_class_uid

    # get time values
    date_of_capture = datetime.datetime.now().strftime('%Y%m%d')
    time_of_capture = datetime.datetime.now().strftime('%H%M%S')

    # convert jpeg to DICOM
    output = generate_dicom_from_image('tech_note.jpg', modality=request.POST['modality'], patient_id=request.POST['patient_id'],
                                       patient_name=request.POST['patient_name'], procedure=request.POST[
                                           'procedure'], tech_initials=request.POST['tech_initials'], accession=request.POST['accession'],
                                       study_instance_uid=study_instance_uid, series_instance_uid=series_instance_uid, sop_instance_uid=sop_instance_uid, implementation_class_uid=implementation_class_uid,
                                       date_of_capture=date_of_capture, time_of_capture=time_of_capture)
    # update UID values in database
    uid_values.uid_counter = uid_values.uid_counter + 1
    uid_values.save()

    output.save_as("tech_note.dcm")


# send to PACS

    scu_ae = WorkstationConfigs.objects.get(id=1).workstation_ae

    destination_configs = DestinationConfigs.objects.get(id=1)

    dest_ae = destination_configs.destination_ae
    dest_ip = destination_configs.destination_ip
    dest_port = destination_configs.destination_port

    ae = AE(ae_title=scu_ae)
    # uid for secondary image capture
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
        scu_ae = WorkstationConfigs.objects.get(id=1).workstation_ae

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
        scp = WorklistConfigs.objects.get(id=1)
        scp_ip = scp.worklist_ip
        scp_ae = scp.worklist_ae
        scp_port = scp.worklist_port
        assoc = ae.associate(scp_ip, scp_port, ae_title=scp_ae)

        if assoc.is_established:
            responses = assoc.send_c_find(
                ds, ModalityWorklistInformationFind)

            for(status, identifier) in responses:
                if status:
                    print(
                        'C-FIND query status: 0x{0:04x}'.format(status.Status))

                    if status.Status in (0xFF00, 0xFF01) and identifier:
                        study_data = identifier

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
                            'query_form': query_form,

                        }

                        return render(request, 'tech_forms/query_worklist.html', context)

                    else:
                        error = 'No match found'

                else:
                    error = "Connection timed out, was aborted or receieved invalid response"
            assoc.release()
        else:
            error = 'Associated rejected, aborted or never connected'

        context = {
            'error': error,
        }

        return render(request, 'tech_forms/query_worklist_error.html', context)

    else:

        form = QueryWorklistForm()

        context = {
            "form": form
        }

        return render(request, 'tech_forms/query_worklist.html', context)


def worklist_form_submit(request):
    if request.method == 'POST':

        modality = f"Modality: {request.POST['modality']}"
        patient_id = f"Patient ID: {request.POST['patient_id']}"
        patient_name = f"Patient Name: {request.POST['patient_name']}"
        exam_date = f"Exam Date: {request.POST['study_date']}"
        accession = f"Accession#: {request.POST['accession']}"
        procedure = f"Procedure: {request.POST['study_description']}"
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

        # get uid root values from database
        uid_values = UIDvalues.objects.get(id=1)
        # make the uids
        study_instance_uid = request.POST['study_instance_uid']
        series_instance_uid = uid_values.series_instance_uid + \
            '.' + str(uid_values.uid_counter + 1)
        sop_instance_uid = uid_values.series_instance_uid + \
            '.1.' + str(uid_values.uid_counter + 1)
        implementation_class_uid = uid_values.implementation_class_uid

        # get time values
        date_of_capture = datetime.datetime.now().strftime('%Y%m%d')
        time_of_capture = datetime.datetime.now().strftime('%H%M%S')

        # patient_name clean
        patient_name_clean = (
            request.POST['patient_name']).replace('^', ' ').rstrip()
        # convert jpeg to DICOM
        output = generate_dicom_from_image('tech_note.jpg', modality=request.POST['modality'], patient_id=request.POST['patient_id'],
                                           patient_name=patient_name_clean, procedure=request.POST[
                                               'study_description'], tech_initials=request.POST['tech_initials'], accession=request.POST['accession'],
                                           study_instance_uid=study_instance_uid, series_instance_uid=series_instance_uid, sop_instance_uid=sop_instance_uid, implementation_class_uid=implementation_class_uid,
                                           date_of_capture=date_of_capture, time_of_capture=time_of_capture)

        uid_values.uid_counter = uid_values.uid_counter + 1
        uid_values.save()

        output.save_as("tech_note.dcm")

    # send to PACS

        scu_ae = WorkstationConfigs.objects.get(id=1).workstation_ae

        destination_configs = DestinationConfigs.objects.get(id=1)

        dest_ae = destination_configs.destination_ae
        dest_ip = destination_configs.destination_ip
        dest_port = destination_configs.destination_port

        ae = AE(ae_title=scu_ae)
        # uid for secondary image capture
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
            "dicom_message": dicom_message
        }

        return render(request, 'tech_forms/form_submitted.html', context)
    else:
        errors = "Forbidden"

        context = {
            "errors": errors
        }
        return render(request, 'tech_forms/form_submitted.html', context)
