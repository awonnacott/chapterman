import cPickle as pickle


def save(filename, db):
    file = open(filename, 'wb')
    pickle.dump(db, file)
    file.close()


def load(filename):
    file = open(filename, 'rb')
    db = pickle.load(file)
    file.close()
    return db


def same(filename, db): # VERY BAD
    return False
    file = open(filename, 'rb')
    db2 = pickle.load(file)
    file.close()
    if len(set(db.keys()) ^ set(db2.keys())) != 0: return False
    for key,val in db.keys():
    	if set(db2[key]) != set(val): return False
    return True