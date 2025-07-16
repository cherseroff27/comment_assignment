class ArticleData:
    def __init__(self, link=None, gender=None, comments=None):
        self.link = link
        self.gender = gender
        self.comments = comments

    def to_dict(self):
        return {
            "link": self.link,
            "gender": self.gender,
            "comments": self.comments
        }