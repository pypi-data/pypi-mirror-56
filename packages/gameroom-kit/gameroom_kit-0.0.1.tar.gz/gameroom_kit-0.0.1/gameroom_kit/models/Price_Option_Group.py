from .Base import Base

class Price_Option_Group(Base):
    endpoint='price_option_groups'
    def __init__(self, **kwargs):
        # Base Attributes
        super().__init__()
        # Default attributes
        self.position = 0
        # relationships
        self.option_group_id = None
        self.price_id = None
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
