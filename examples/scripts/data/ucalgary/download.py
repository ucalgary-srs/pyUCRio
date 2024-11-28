import pyucrio
import datetime
import pprint

rio = pyucrio.PyUCRio()

start_dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_dt = datetime.datetime(2023, 1, 5, 23, 59, 59)

print()
res = rio.data.ucalgary.download("NORSTAR_RIOMETER_K0_TXT", start_dt, end_dt, site_uid="gill", overwrite=True)

print()
print(res)
print()
pprint.pprint(res.__dict__)
print()
