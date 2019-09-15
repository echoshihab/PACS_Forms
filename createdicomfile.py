# Coded version of DICOM file 'IM000001'
# Produced by pydicom codify utility script
from __future__ import unicode_literals  # Only for python2.7 and save_as unicode filename
import pydicom
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

# File meta info data elements
file_meta = Dataset()
file_meta.FileMetaInformationGroupLength = 190
file_meta.FileMetaInformationVersion = b'\x00\x01'
file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'
file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.23849.1394177094.11.1637038637959083360.2.2.1'
file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
file_meta.ImplementationClassUID = '1.2.840.114202.5.2'
file_meta.ImplementationVersionName = 'IMS4-17-1-P129'

# Main data elements
ds = Dataset()
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
ds.Manufacturer = 'PACSGEAR'
ds.InstitutionName = 'LXA'
ds.ReferringPhysicianName = ''
ds.StationName = 'DUN-DIUS-PC01'
ds.StudyDescription = 'SCAN NOTES'
ds.SeriesDescription = 'SCAN NOTES'
ds.InstitutionalDepartmentName = 'US'
ds.OperatorsName = ''
ds.ManufacturerModelName = ''
ds.PatientName = ''
ds.PatientID = 'WERWER'
ds.PatientBirthDate = '00021130'
ds.PatientSex = ''
ds.BodyPartExamined = ''
ds.DeviceSerialNumber = ''
ds.DateOfSecondaryCapture = '20190912'
ds.TimeOfSecondaryCapture = '054316'
ds.SecondaryCaptureDeviceManufacturer = 'Lexmark'
ds.SecondaryCaptureDeviceManufacturerModelName = 'PACSSCAN'
ds.SecondaryCaptureDeviceSoftwareVersions = '5.3.0.47'
ds.SoftwareVersions = 'V1.0'
ds.DigitalImageFormatAcquired = ''
ds.StudyInstanceUID = '1.3.6.1.4.1.23849.869756260.11.1637038637957989484'
ds.SeriesInstanceUID = '1.3.6.1.4.1.23849.1394177094.11.1637038637959083360.2.2'
ds.StudyID = ''
ds.SeriesNumber = "999"
ds.InstanceNumber = "1"
ds.PatientOrientation = ''
ds.SamplesPerPixel = 3
ds.PhotometricInterpretation = 'RGB'
ds.PlanarConfiguration = 0
ds.Rows = 1052
ds.Columns = 812
ds.BitsAllocated = 8
ds.BitsStored = 8
ds.HighBit = 7
ds.PixelRepresentation = 0
ds.SmallestImagePixelValue = 0
ds.LargestImagePixelValue = 255
ds.PixelData = # XXX Array of 2562672 bytes excluded

ds.file_meta = file_meta
ds.is_implicit_VR = False
ds.is_little_endian = True
ds.save_as(r'savename', write_like_original=False)