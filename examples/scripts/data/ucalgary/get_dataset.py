import pyucrio
import pprint

rio = pyucrio.PyUCRio()

dataset = rio.data.get_dataset("NORSTAR_RIOMETER_K2_TXT")

print()
print(dataset)
print()

print("Example record in dict format:\n------------------------------\n")
pprint.pprint(dataset.__dict__)
