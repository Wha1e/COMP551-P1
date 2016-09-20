class Event:
    def __init__(self, date, name, etype, time, category):
        self.date = date
        self.name = name
        self.etype = etype
        self.time = time
        self.category = category

    def has_completed(self):
        return self.time != -1
