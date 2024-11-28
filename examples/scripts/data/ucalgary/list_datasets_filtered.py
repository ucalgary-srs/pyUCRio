import pyucrio
import pprint

rio = pyucrio.PyUCRio()

datasets = rio.data.ucalgary.list_datasets(name="NORSTAR_RIOMETER")

print("\nFound %d datasets matching the name filter\n------------------------------\n" % (len(datasets)))
pprint.pprint(datasets)

print("\nExample record in dict format:\n------------------------------\n")
pprint.pprint(datasets[0].__dict__)
print()
