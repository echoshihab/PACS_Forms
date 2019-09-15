import pydicom
import tempfile
import datetime
from PIL import Image
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import UID


def generate_dicom_from_image(image_file):
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    image_name = image_file
    img = Image.open(image_name)

    # required data elements

# File meta info data elements
    file_meta = Dataset()
    file_meta.FileMetaInformationGroupLength = 190
    file_meta.FileMetaInformationVersion = b'\x00\x01'
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'
    file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.23849.1394177094.11.1637038637959083360.2.2.1'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
    file_meta.ImplementationClassUID = '1.2.840.000000.1.1'  # old - '1.2.840.114202.5.2'
    file_meta.ImplementationVersionName = 'PF.1.0.0'

    ds = FileDataset(filename_little_endian, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # Main data elements
    ds.ImageType = ['ORIGINAL', 'SECONDARY']
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.7'
    ds.SOPInstanceUID = '1.3.6.1.4.1.23849.1394177094.11.1637038637959083360.2.2.1'
    ds.StudyDate = '20190912'
    ds.SeriesDate = '20190912'
    ds.AcquisitionDate = '20190912'
    ds.StudyTime = '054219'
    ds.SeriesTime = '054219'
    ds.AcquisitionTime = '054316'
    ds.AccessionNumber = ''
    ds.Modality = 'OT'
    ds.ConversionType = 'WSD'
    ds.Manufacturer = 'PACSFORM'
    ds.InstitutionName = 'LXA'
    ds.ReferringPhysicianName = ''
    ds.StationName = 'DUN-DIUS-PC01'
    ds.StudyDescription = 'PACS FORM'
    ds.SeriesDescription = 'PACS FORM'
    ds.InstitutionalDepartmentName = 'US'
    ds.OperatorsName = ''
    ds.ManufacturerModelName = ''
    ds.PatientName = 'TestShihab'
    ds.PatientID = 'T00159'
    ds.PatientBirthDate = '19850112'
    ds.PatientSex = ''
    ds.BodyPartExamined = ''
    ds.DeviceSerialNumber = ''
    ds.DateOfSecondaryCapture = '20190912'
    ds.TimeOfSecondaryCapture = '054316'
    ds.SecondaryCaptureDeviceManufacturer = 'Shihab'
    ds.SecondaryCaptureDeviceManufacturerModelName = 'PACSFORM'
    ds.SecondaryCaptureDeviceSoftwareVersions = '1.0.0'
    ds.SoftwareVersions = 'V1.0.0'
    ds.DigitalImageFormatAcquired = ''
    ds.StudyInstanceUID = '1.3.6.1.4.1.23849.869756260.11.1637038637957989484'
    ds.SeriesInstanceUID = '1.3.6.1.4.1.23849.1394177094.11.1637038637959083360.2.2'
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


filename = input('Enter file name: ')
output = generate_dicom_from_image(filename)
output.save_as("tester2.dcm")
