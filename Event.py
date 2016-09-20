class Event:
    def __init__(self, date, name, type, time, category):
        self.date = date
        self.name = name
        self.type = type
        self.time = time
        self.category = category

    def has_completed(self):
        return self.time != -1
