from .Base import Base

class Option_Group(Base):
    endpoint='option_groups'
    def __init__(self, **kwargs):
        # Base Attributes
        super().__init__()
        # Default attributes
        self.info = None
        self.multitudinal = False
        self.name = None
        self.tags = list()
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
