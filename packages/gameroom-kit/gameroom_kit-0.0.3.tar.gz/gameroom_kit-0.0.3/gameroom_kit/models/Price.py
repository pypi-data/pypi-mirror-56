from .Base import Base

class Price(Base):
    endpoint='prices'
    def __init__(self, **kwargs):
        # Base Attributes
        super().__init__()
        # Default attributes
        self.amount = 0
        self.identifier = None
        self.info = None
        self.locked = False
        self.name = None
        self.position = 0
        # Relationships
        self.product_id = None
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
