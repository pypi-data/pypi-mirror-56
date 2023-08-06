from pkg_resources import resource_string
ymlfile = resource_string(__name__, 'data_EELS.txt')
print(ymlfile)