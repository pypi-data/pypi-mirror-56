from .Base import Base

class Product(Base):
    endpoint='products'
    def __init__(self, **kwargs):
        # Base Attributes
        super().__init__()
        # Default attributes
        self.depth = 0
        self.height = 0
        self.identifier = None
        self.info = None
        self.name = None
        self.properties = dict()
        self.subname = None
        self.tags = list()
        self.rank = 0
        self.weight = 0
        self.width = 0
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
