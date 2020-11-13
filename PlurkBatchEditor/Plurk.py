class Plurk:
    def __init__(self, plurkID, qualifier, isUnread, content, plurkType, userID, ownerID):
        self.plurkID = plurkID
        self.qualifier = qualifier
        self.isUnread = isUnread
        self.content = content
        self.plurkType = plurkType
        self.userID = userID
        self.ownerID = ownerID

    @staticmethod
    def parseFromJSON(jsonResult):
        plurk_id = jsonResult['plurk_id']
        qualifier = jsonResult['qualifier']
        qualifier_translated = jsonResult['qualifier_translated']
        is_unread = jsonResult['is_unread']
        plurk_type = jsonResult['plurk_type']
        user_id = jsonResult['user_id']
        owner_id = jsonResult['owner_id']
        posted = jsonResult['posted']
        no_comments = jsonResult['no_comments']
        content = jsonResult['content']
        content_raw = jsonResult['content_raw']
        response_count = jsonResult['response_count']
        responses_seen = jsonResult['responses_seen']
        limited_to = jsonResult['limited_to']
        favorite = jsonResult['favorite']
        favorite_count = jsonResult['favorite_count']
        favorers = jsonResult['favorers']
        replurkable = jsonResult['replurkable']
        replurked = jsonResult['replurked']
        replurker_id = jsonResult['replurker_id']
        replurkers_count = jsonResult['replurkers_count']
        replurkers = jsonResult['replurkers']

        plurk = Plurk(plurk_id, qualifier, is_unread, content, plurk_type, user_id, owner_id)

        return plurk
    