from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind
import os

scu_ae = os.environ.get('AE_TITLE')

ae = AE(ae_title=scu_ae)  # SCU

ae.add_requested_context(ModalityWorklistInformationFind)

ds = Dataset()
ds.PatientName = '*'
ds.AccessionNumber = os.environ.get('ACCESSION')
ds.PatientID = ''
ds.StudyInstanceUID = ''
ds.QueryRetrieveLevel = 'STUDY'
ds.ScheduledProcedureStepSequence = [Dataset()]
item = ds.ScheduledProcedureStepSequence[0]
item.modality = 'CR'

# associate with SCP
scp_ip = os.environ.get('SCP_IP')
scp_ae = os.environ.get('SCP_AE')
assoc = ae.associate(scp_ip, 5010, ae_title=scp_ae)


if assoc.is_established:
    responses = assoc.send_c_find(
        ds, ModalityWorklistInformationFind)

    for(status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))
            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
            else:
                print('Connection timed out, was aborted or receieved invalid response')

    assoc.release()
else:
    print('Associated rejected, aborted or never connected')
