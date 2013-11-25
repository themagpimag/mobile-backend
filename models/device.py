from google.appengine.ext import ndb

class Device(ndb.Model):
    id_gcm = ndb.StringProperty()
    language = ndb.StringProperty()
    os = ndb.StringProperty()

    @classmethod
    def generate_key(cls, id_device):
        return ndb.Key(cls, id_device)

