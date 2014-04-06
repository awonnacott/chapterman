import pickle

def db_save(filename, db):
    file = open(filename, 'wb')
    pickle.dump(db, file)
    file.close()

def db_load(filename):
    file = open(filename, 'rb')
    db = pickle.load(file)
    file.close()
    return db

def db_same(filename, db): # VERY BAD
    return False