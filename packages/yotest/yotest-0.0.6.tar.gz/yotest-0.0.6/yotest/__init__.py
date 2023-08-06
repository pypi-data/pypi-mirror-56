import pickle
from pkg_resources import resource_string
ymlfile = resource_string(__name__, 'data.pkl').decode("utf-8")
print(pickle.load(ymlfile))