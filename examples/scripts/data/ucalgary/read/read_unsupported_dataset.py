import pyucrio
import datetime

# init
rio = pyucrio.PyUCRio()

# get dataset
print("\n[%s] Getting dataset ..." % (datetime.datetime.now()))
dataset = rio.data.ucalgary.list_datasets("THEMIS_ASI_RAW")[0]

# download data
print("\n[%s] Downloading data ..." % (datetime.datetime.now()))
start_dt = datetime.datetime(2023, 1, 1, 6, 0, 0)
end_dt = datetime.datetime(2023, 1, 1, 6, 4, 59)
site_uid = "gill"
download_obj = rio.data.ucalgary.download(dataset.name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)

# set list of files (we could do this using a glob too)
file_list = download_obj.filenames

# read data
print("\n[%s] Reading data ..." % (datetime.datetime.now()))
try:
    data = rio.data.ucalgary.read(dataset, file_list, n_parallel=1)
    print()
    print(data)
except pyucrio.PyUCRioUnsupportedReadError as e:
    print("Expected error occurred\n\n[pyucrio.PyUCRioUnsupportedReadError]: %s\n" % (str(e)))
