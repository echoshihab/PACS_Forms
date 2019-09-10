import os
from pydicom import dcmread
from pynetdicom import AE, build_context
from pynetdicom.sop_class import UltrasoundImageStorage

# SCU

scu_ae = os.environ.get('AE_TITLE')
ae = AE(ae_title=scu_ae)
ae.add_requested_context(UltrasoundImageStorage)


ds = dcmread('IM000001')

# work in progress, still not working with PACS
assoc = ae.associate('scu_ip', port, ae_title='aetitle')

if assoc.is_established:
    print('Associated')
    status = assoc.send_c_store(ds)

    if status:
        print('C-STORE request status: 0x{0:04x}'.format(status.Status))
    else:
        print('Connection timed out, was aborted or received invalid resposne')

    assoc.release()
else:
    print('Association rejected, aborted or never connected')
