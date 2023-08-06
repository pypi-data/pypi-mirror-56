import pickle
from pkg_resources import resource_string
ymlfile = resource_string(__name__, 'data.pkl')
print(pickle.load(ymlfile))