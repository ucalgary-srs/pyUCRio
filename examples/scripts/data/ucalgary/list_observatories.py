import pyucrio

rio = pyucrio.PyUCRio()

observatories = rio.data.ucalgary.list_observatories("norstar_riometer")

print("\nFound %d observatories\n" % (len(observatories)))
for o in observatories:
    print(o)
print()
