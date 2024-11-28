import pyucrio
import datetime
import pprint

rio = pyucrio.PyUCRio()

start_dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_dt = datetime.datetime(2023, 1, 31, 23, 59, 59)

# get urls
file_listing_obj = rio.data.ucalgary.get_urls("NORSTAR_RIOMETER_K0_TXT", start_dt, end_dt, site_uid="gill")

# do fewer urls
file_listing_obj.urls = file_listing_obj.urls[0:10]

# download urls
print()
res = rio.data.ucalgary.download_using_urls(file_listing_obj, overwrite=True)

print()
print(res)
print()
pprint.pprint(res.__dict__)
print()
