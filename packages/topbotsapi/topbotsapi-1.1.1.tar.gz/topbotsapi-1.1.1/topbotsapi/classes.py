class Bot:
    def __init__(self, botID, botName, botDiscriminator, botPrefix, botLib, botDesc, botGithub, botWebsite, botTags,
                 botDC, botAvatar, botVerif, botCert, botVote, botOwner):
        self.botOwner = botOwner
        self.botAvatar = botAvatar
        self.botVote = botVote
        self.botCert = botCert
        self.botDC = botDC
        self.botTags = botTags
        self.botWebsite = botWebsite
        self.botGithub = botGithub
        self.botDesc = botDesc
        self.botLib = botLib
        self.botPrefix = botPrefix
        self.botDiscriminator = botDiscriminator
        self.botName = botName
        self.botID = botID
        self.botVerif = botVerif


class User:
    def __init__(self, userID, userName, userDiscriminator, userAvatar):
        self.userAvatar = userAvatar
        self.userDiscriminator = userDiscriminator
        self.userName = userName
        self.userID = userID
