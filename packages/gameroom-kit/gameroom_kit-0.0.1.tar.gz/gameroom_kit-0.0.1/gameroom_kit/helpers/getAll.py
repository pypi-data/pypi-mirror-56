from .clearLine import clearLine

def getAll(Model=None, filter=dict(), limit=500, offset=0, sort=list()):
    if Model==None: raise Exception('model not defined')
    # safely get in small batches
    result = []
    more = True
    while more:
      print(f'getting {Model.endpoint}: {len(result)}', end='\r')
      batch = Model.get(filter=filter, limit=limit, offset=offset, sort=sort)
      offset += len(batch)
      result.extend(batch)
      if len(batch) < limit: more = False

    clearLine()
    print(f'got {Model.endpoint}: {len(result)}')
    return result
