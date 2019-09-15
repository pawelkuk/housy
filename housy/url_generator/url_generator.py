import abc


class AbsUrlGenerator(metaclass=abc.ABCMeta):
    """Defines an interface for creating urls for different target sites"""
    def __init__(self, requirements):
        self.requirements = requirements

    @abc.abstractmethod
    def generate_url(self):
        pass


class OtodomUrlGenerator(AbsUrlGenerator):
    def generate_url(self):
        pass
