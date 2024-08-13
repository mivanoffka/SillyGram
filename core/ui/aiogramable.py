from abc import abstractmethod, ABCMeta


class Aiogramable(metaclass=ABCMeta):

    @abstractmethod
    def aiogramify(self, language_code: str) -> any:
        raise NotImplementedError()
