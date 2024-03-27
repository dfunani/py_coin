class base:
    a = 1
    @classmethod
    def run(cls):
        return base.a
    

class profile(base):
    def __init__(self) -> None:
        super().__init__()
        self.a = 1
        base.a += 1

class p(base):
    def __init__(self) -> None:
        super().__init__()
        base.a += 1

print(profile().run(), p().run(), profile().run())