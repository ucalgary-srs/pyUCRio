import pyucrio

# init
rio = pyucrio.PyUCRio()

# get list
datasets = rio.data.ucalgary.list_supported_read_datasets()

print()
print(datasets)
