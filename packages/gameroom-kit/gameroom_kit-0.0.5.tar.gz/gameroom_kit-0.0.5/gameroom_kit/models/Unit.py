from .Base import Base

class Unit(Base):
    endpoint='products'
    def __init__(self, **kwargs):
        # Base Attributes
        super().__init__()
        # Default attributes
        self.amount = 0
        self.calculated = False
        self.depth = 0
        self.height = 0
        self.identifier = None
        self.index = 0
        self.info = None
        self.locked = False
        self.name = None
        self.offered = False
        self.properties = dict()
        self.quantity = 0
        self.serial_number = None
        self.shopified = False
        self.subname = None
        self.tags = list()
        self.weight = 0
        self.width = 0
        # Relationships
        self.price_id = None
        self.product_id = None
        self.store_id = None
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
