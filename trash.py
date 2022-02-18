# from settings.setting import BaseSettings

print('HAHAH')
from utils.exceptions.system_exit_exception import SystemExitException

from settings import SettingsFactory, EmojiLogger, Environments

wxsettings = SettingsFactory(environment=Environments.LOCALHOST).get_settings()
print(wxsettings)
from services.mongoclient import MongoDBClient
from services.elastic import ElasticClient
mg = MongoDBClient(wxsettings)
es = ElasticClient(wxsettings)
mg.collections()

# attributes = [attr for attr in dir(settings)
#               if not attr.startswith('__')]

# {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
# now dump this in some way or another
# print(', '.join("%s: %s" % item for item in attrs.items()))


for att in dir(wxsettings):
    if not att.startswith('__'):
        print(att, getattr(wxsettings, att))
