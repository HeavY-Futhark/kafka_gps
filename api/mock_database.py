class MockDatabase:
    data = {
    }

    def readAll(self):
        return self.data.values()

    def readOne(self, id):
        return self.data[id]
