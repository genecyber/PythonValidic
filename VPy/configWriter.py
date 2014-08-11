import ConfigParser

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('Application')
config.add_section('Credentials')
config.add_section('API')
config.set('Application', 'Mode', 'Test')
config.set('Credentials', 'TestOrgId', '51aca5a06dedda916400002b')
config.set('Credentials', 'TestAccessToken', 'ENTERPRISE_KEY')
config.set('Credentials', 'TestUserId', '52ff6899f1f70e2d65000002')
config.set('Credentials', 'OrgId', '53be5b33cad90cc9be000011')
config.set('Credentials', 'AccessToken', 'd054f958a9abf0319f09abd34a3f59d32ef6af5241200e3f148ada027a93d6b3')
config.set('Credentials', 'UserId', '53e289ce84626b8e59000008')

config.set('API', 'TestBaseUrl', 'https://api.validic.com/v1/')
config.set('API', 'BaseUrl', 'https://api.validic.com/v1/')


# Writing our configuration file to 'example.cfg'
with open('settings.cfg', 'wb') as configfile:
    config.write(configfile)