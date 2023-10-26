import numpy as np

booked_transfers = np.array([[0,0]])
refunded_transfers_booked = np.array([[0,0]])
unmatched_transfer_ids = np.array([0])
np.save('booked_transfers.npy', booked_transfers)
np.save('refunded_transfers_booked.npy', refunded_transfers_booked)
np.save('unmatched_transfers_handled.npy', unmatched_transfer_ids)

