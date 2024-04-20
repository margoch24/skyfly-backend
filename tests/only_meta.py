from config import DefaultConfig


class OnlyMeta(type):

    def __new__(cls, name, bases, dct):

        if DefaultConfig.SINGLE_TEST:
            for key, value in dct.items():
                if (
                    key.startswith("test")
                    and callable(value)
                    and not key.endswith("only")
                ):
                    dct[key] = None

        return super().__new__(cls, name, bases, dct)
