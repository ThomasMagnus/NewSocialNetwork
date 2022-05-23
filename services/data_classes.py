class FriendsData:
    def __init__(self, name: str, email: str, login: str, status: bool, date: str, request_on_friend: bool):
        self.name = name
        self.email = email
        self.login = login
        self.status = status
        self.date = date
        self.request_on_friend = request_on_friend

    def parse_friends_data(self) -> dict:
        data_object: dict = {
            'name': self.name,
            'email': self.email,
            'login': self.login,
            'status': self.status,
            'date': self.date,
            'request_on_friend': self.request_on_friend
        }

        return data_object

