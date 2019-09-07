import pydicom
import tempfile
import datetime
from PIL import Image
from pydicom.dataset import Dataset, FileDataset


def generate_dicom_from_image(image_file):
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    image_name = image_file

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'
    file_meta.MediaStorageSOPInstanceUID = '2.16.840.1.114430.287196081618142314176776725491661159509.60.1'
    file_meta.ImplementationClassUID = '1.3.46.670589.50.1.8.0'

    ds = FileDataset(filename_little_endian, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # required data elements
    ds.modality = 'WSD'
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    ds.StudyInstanceUID = '1.3.6.1.4.1.9590.100.1.1.124313977412360175234271287472804872093'
    ds.SeriesInstanceUID = '1.3.6.1.4.1.9590.100.1.1.369231118011061003403421859172643143649'
    ds.SOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    ds.SOPClassUID = 'Secondary Capture Image Storage'
    ds.SecondaryCaptureDeviceManufctur = 'Python 3.7.0'
    ds.PatientName = "Tester"
    ds.PatientId = "123456"
    ds.PixelRepresentation = 0
    ds.BitsAllocated = 8
    ds.SamplesPerPixel = 1  # 1 for grayscale #3 for color
    ds.NumberofFrames = 1

    img = Image.open(image_name)
    print(img.size)
    ds.Columns = img.size[0]
    ds.Rows = img.size[1]

    ds.PixelData = img.tobytes()

    ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')
    ds.ContentTime = timeStr

    return ds


filename = input('Enter file name: ')
output = generate_dicom_from_image(filename)
output.save_as("tester.dcm")
ds = pydicom.dcmread('tester.dcm')
print(ds)
