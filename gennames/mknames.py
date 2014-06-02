import pickle

fnames = []
lnames = []

with open('names.lst') as input:
    for name in input:
        [fname, lname] = map(lambda n: n.strip(), name.split(" "))
        fnames.append(fname)
        lnames.append(lname)


with open('names.pk', 'wb') as output:
    pickle.dump(fnames,output)
    pickle.dump(lnames,output)

