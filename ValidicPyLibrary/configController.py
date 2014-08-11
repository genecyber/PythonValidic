import ConfigParser
class configClient(object):
    def __init__(self, mode):
        self.mode = mode
        self.config = ConfigParser.RawConfigParser()
        self.config.read('settings.cfg')

    def getMode(this):
        return this.config.get('Application', 'mode')

    def getOrgId(this):
        return this.config.get('Credentials', this.mode+'orgid')

    def getAccessToken(this):
        return this.config.get('Credentials', this.mode+'accesstoken')

    def getBaseUrl(this):
        return this.config.get('API',this.mode+baseurl)


