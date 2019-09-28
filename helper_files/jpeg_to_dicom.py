import pydicom
import tempfile
import datetime
from PIL import Image
from pydicom.dataset import Dataset, FileDataset


def generate_dicom_from_image(image_file, **kwargs):
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    image_name = image_file
    img = Image.open(image_name)

    # required data elements

# File meta info data elements
    file_meta = Dataset()
    file_meta.FileMetaInformationGroupLength = 190
    file_meta.FileMetaInformationVersion = b'\x00\x01'
    # secondary capture image storage
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'
    file_meta.MediaStorageSOPInstanceUID = kwargs['sop_instance_uid']
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'  # explicit VR Little-endian
    file_meta.ImplementationClassUID = '1.2.840.000000.1.1'  # old - '1.2.840.114202.5.2'
    file_meta.ImplementationVersionName = 'PF.1.0.0'

    ds = FileDataset(filename_little_endian, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # kwargs so far = accession, modality, procedure, tech initia, patient
    # name, patient id

    # Main data elements
    ds.ImageType = ['ORIGINAL', 'SECONDARY']
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.7'
    ds.SOPInstanceUID = kwargs['sop_instance_uid']
    ds.StudyDate = kwargs['date_of_capture']
    ds.SeriesDate = kwargs['date_of_capture']
    ds.AcquisitionDate = kwargs['date_of_capture']
    ds.StudyTime = kwargs['time_of_capture']
    ds.SeriesTime = kwargs['time_of_capture']
    ds.AcquisitionTime = kwargs['time_of_capture']
    ds.AccessionNumber = kwargs['accession']
    ds.Modality = kwargs['modality']
    ds.ConversionType = 'WSD'
    ds.Manufacturer = 'PACSFORM'
    ds.InstitutionName = 'LXA'
    ds.ReferringPhysicianName = ''
    ds.StationName = 'PACS-FORM-PC01'
    ds.StudyDescription = kwargs['procedure']
    ds.SeriesDescription = 'PACS FORM'
    ds.InstitutionalDepartmentName = 'US'
    ds.OperatorsName = kwargs['tech_initials']
    ds.ManufacturerModelName = ''
    ds.PatientName = kwargs['patient_name']
    ds.PatientID = kwargs['patient_id']
    ds.PatientBirthDate = '19850112'
    ds.PatientSex = ''
    ds.BodyPartExamined = ''
    ds.DeviceSerialNumber = ''
    ds.DateOfSecondaryCapture = kwargs['date_of_capture']
    ds.TimeOfSecondaryCapture = kwargs['time_of_capture']
    ds.SecondaryCaptureDeviceManufacturer = 'Shihab'
    ds.SecondaryCaptureDeviceManufacturerModelName = 'PACSFORM'
    ds.SecondaryCaptureDeviceSoftwareVersions = '1.0.0'
    ds.SoftwareVersions = 'V1.0.0'
    ds.DigitalImageFormatAcquired = ''
    ds.StudyInstanceUID = kwargs['study_instance_uid']
    ds.SeriesInstanceUID = kwargs['series_instance_uid']
    ds.StudyID = ''
    ds.SeriesNumber = "999"
    ds.InstanceNumber = "1"
    ds.PatientOrientation = ''
    ds.SamplesPerPixel = 3  # 1 for grayscale #3 for color
    ds.PhotometricInterpretation = 'RGB'
    ds.Rows = img.size[1]
    ds.Columns = img.size[0]
    ds.BitsAllocated = 8
    ds.BitsStored = 7  # NEED TO FIX THIS
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = img.tobytes()
    ds.is_implicit_VR = False
    ds.is_little_endian = True

    return ds


#filename = input('Enter file name: ')
#output = generate_dicom_from_image(filename)
# output.save_as("tech_note.dcm")
