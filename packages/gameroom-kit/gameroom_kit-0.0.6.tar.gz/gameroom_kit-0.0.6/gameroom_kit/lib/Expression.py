from .Comparison import Comparison

def Expression(**kwargs):
    return {
        'key': kwargs.get('key') if 'key' in kwargs else None,
        'comparison': Comparison(kwargs.get('comparison')) if 'comparison' in kwargs else Comparison('='),
        'value': kwargs.get('value') if 'value' in kwargs else None
    }
