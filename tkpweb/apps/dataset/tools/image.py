import os
from tkp.database.database import DataBase
from tkp.utility.accessors import DataAccessor
from tkp.utility.accessors import FITSImage
from tkp.utility.accessors import CASAImage


def open_image(url, dblogin=None):
    image = None
    if isinstance(url, DataAccessor):
        pass
    elif isinstance(url, basestring):
        name, ext = os.path.splitext(url)
        if ext.lower() == '.fits':
            image = FITSImage(url)
        elif ext.lower() == '.img':
            image = AIPSppImage(url)
    elif isinstance(url, (int, long)):
        db = DataBase(**dblogin) if dblogin else DataBase()
        url = Image(id=url, database=database).url
        name, ext = os.path.splitext(url)
        if ext.lower() == '.fits':
            image = FITSImage(url)
        elif ext.lower() == '.img':
            image = CASAImage(url)
        db.close()
    else:
        raise ValueError("unknown image type")
    return image
