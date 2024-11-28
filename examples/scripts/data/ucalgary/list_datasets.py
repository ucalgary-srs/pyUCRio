import pyucrio
import pprint

rio = pyucrio.PyUCRio()

datasets = rio.data.ucalgary.list_datasets()

print("\nFound %d datasets" % (len(datasets)))

print("\nExample dataset:\n------------------------------")
print(datasets[0])
print()

print("\nExample dataset in dict format:\n------------------------------")
pprint.pprint(datasets[0].__dict__)
print()
