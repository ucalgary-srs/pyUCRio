import pyucrio

# init
rio = pyucrio.PyUCRio()

# check
print()
print("NORSTAR_RIOMETER_K0_TXT supported: %s" % (rio.data.ucalgary.is_read_supported("NORSTAR_RIOMETER_K0_TXT")))
print("SOME_BAD_DATASET supported: %s" % (rio.data.ucalgary.is_read_supported("SOME_BAD_DATASETASI_RAW")))
print()
