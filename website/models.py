import datetime


class Note:

    def __init__(self, id, data, user_id):
        self.id = id
        self.data = data
        self.user_id = user_id
        self.date = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")


class User:

    def __init__(self, id, email, password, first_name, notes):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.notes = notes