import pyucrio
import pprint
import datetime

rio = pyucrio.PyUCRio()

start_dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_dt = datetime.datetime(2023, 1, 5, 23, 59, 59)

res = rio.data.ucalgary.get_urls("NORSTAR_RIOMETER_K0_TXT", start_dt, end_dt, site_uid="chur")

print()
print(res)
print()
pprint.pprint(res.__dict__)
print()
