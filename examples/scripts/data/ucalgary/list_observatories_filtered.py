import pyucrio

rio = pyucrio.PyUCRio()

observatories = rio.data.ucalgary.list_observatories("norstar_riometer", uid="fs")

print("\nFound %d observatories matching the uid filter\n" % (len(observatories)))
for o in observatories:
    print(o)
print()
