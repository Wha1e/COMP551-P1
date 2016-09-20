class Runner:
    def __init__(self, id, events):
        self.id = id
        self.events = sorted(events, key = lambda x: x.date, reverse=True)

    def get_latest_event(self):
        return self.events[-1]

    def get_latest_category(self):
        return self.get_latest_event().category

    def get_all_events(self):
        splitter =  "----------------------------------------"
        for e in self.events:
            print(splitter)
            print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.type, e.time, e.category))
        print(splitter)

    def get_all_completed_events(self):
        for e in self.events:
            if e.has_completed():
                print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.type, e.time, e.category))
