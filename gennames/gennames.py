import pickle, random

def read_names():
    with open('gennames/names.pk') as input:
        fnames = pickle.load(input)
        lnames = pickle.load(input)
    return fnames,lnames

fnames, lnames = read_names()



def gen_name():
    fname = random.choice(fnames)
    lname = random.choice(lnames)
    return fname+lname


if __name__ == '__main__':
    for i in range(100):
        print gen_name()