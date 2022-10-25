
class instaPerson():

    def __init__(self, name, instaId):
        self.INSTA_ID = instaId
        self.NAME = name

    def tostring(self):
        return f"user name:{self.NAME}  user instagramID = {self.INSTA_ID}"
