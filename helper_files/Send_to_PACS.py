import os
from pydicom import dcmread
from pydicom.uid import UID
from pynetdicom import AE
import logging

logging.basicConfig(filename='pynetdicom.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger('pynetdicom')
LOGGER.setLevel(logging.DEBUG)


#AEs & IP
scu_ae = os.environ.get('AE_TITLE')
dest_ae = os.environ.get('DEST_AE')
dest_ip = os.environ.get('DEST_IP')
print(scu_ae, dest_ae, dest_ip)


ae = AE(ae_title=scu_ae)
# this uid is for secondary image capture
uid = UID('1.2.840.10008.5.1.4.1.1.7')
ae.add_requested_context(uid)


ds = dcmread('tester2.dcm')


# work in progress, still not working with PACS
assoc = ae.associate(dest_ip, 5000, ae_title=dest_ae)

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
