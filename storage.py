import json

class Storage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, chromosomes):
        file = open(self.filename, 'w')
        json.dump({"chromosomes": chromosomes}, file)

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return data["chromosomes"]
        except Exception:
            return []