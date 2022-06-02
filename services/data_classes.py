class FriendsDataDict:
    def __init__(self, firstname: str, lastname: str, login: str):
        self.firstname = firstname
        self.lastname = lastname
        self.login = login

    def parse_friends_data(self) -> dict:
        data_object: dict = {
            'name': f'{self.firstname} {self.lastname}',
            'login': self.login,
        }

        return data_object

