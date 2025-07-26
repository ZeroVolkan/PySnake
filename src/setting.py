import toml

class Setting():
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load()

    def load(self):
        with open(self.file_path, 'r') as file:
            return toml.load(file)

    def save(self):
        with open(self.file_path, 'w') as file:
            toml.dump(self.data, file)

    def scan(self, object, path: list[str]):
        select = self.data
        for i in path:
            select = select[i]

        params = []
        if "__annotations__" in object.__dict__:
            for name, t in object.__annotations__.items():
                params.append(t(select[name]))
        else:
            raise TypeError("Class don't have __annotation__")

        return params

    def __str__(self):
        return f"Setting({self.file_path})"
