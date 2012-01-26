from tkp.database.database import DataBase
from tkp.database.dataset import ExtractedSource
from tkp.utility.accessors import DataAccessor
from tkp.utility.accessors import FITSImage
from tkp.utility.accessors import CASAImage
from scipy.stats import chisqprob
from .image import open_image
from tkpweb import settings


def dataset(id=None, extra_info=(), dblogin=None):
    """Get information on one or more datasets form the database

    Kwargs:

        id (int or None): if None, obtain a listing of all
            datasets. Otherwise, obtain the information for a specific
            dataset.

        extra_info (set of strings): if given, some extra
            information (through other tables) is obtained from the
            database. Each string can be one of:

            - ntransients: number of transients for a dataset.

            - nimages: number of images for a dataset.

            - nsources: number of unique sources for a dataset.

            - ntotalsources: total number of sources (found by
              sourcefinder) for this dataset.

            Note that a tuple or list of strings is valid input, but
            will be transformed into a set, to filter out double
            strings.

     Returns:

        (list): A list of dicts; each list item corresponds to a
            single database row, while each dict contains the values
            for the columns (with the column names the keys; some
            column values are available twice, with a different
            key). For a single dataset, the returned value is a
            single-element list.
    """

    extra_info = set(extra_info)
    db = DataBase(**dblogin) if dblogin else DataBase()
    print db.name
    if id is not None:  # id = 0 could be valid for some databases
        db.execute("""SELECT * FROM datasets WHERE dsid = %s""", id)
    else:
        db.execute("""SELECT * FROM datasets""")
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    datasets = []
    for row in db.cursor.fetchall():
        datasets.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into slightly nicer keys
        for key1, key2 in zip(
            ['dsid', 'process_ts'],
            ['id', 'processdate']):
            datasets[-1][key2] = datasets[-1][key1]
        if 'ntransients' in extra_info:
            query = """\
SELECT COUNT(*) FROM transients tr, runningcatalog rc
WHERE tr.xtrsrc_id = rc.xtrsrc_id AND rc.ds_id = %s"""
            datasets[-1]['ntransients'] = db.getone(
                query, datasets[-1]['id'])[0]
        if 'nimages' in extra_info:
            query = """\
SELECT COUNT(*) FROM images WHERE ds_id = %s"""
            datasets[-1]['nimages'] = db.getone(
                query, datasets[-1]['id'])[0]
        if 'nsources' in extra_info:
            query = """\
SELECT COUNT(*) FROM runningcatalog WHERE ds_id = %s"""
            datasets[-1]['nsources'] = db.getone(
                query, datasets[-1]['id'])[0]
        if 'ntotalsources' in extra_info:
            query = """\
SELECT COUNT(*) FROM extractedsources ex, images im
WHERE ex.image_id = im.imageid and im.ds_id = %s"""
            datasets[-1]['ntotalsources'] = db.getone(
                query, datasets[-1]['id'])[0]
    return datasets


def image(id=None, dataset=None, extra_info=(), dblogin=None):
    """Get information on one or more datasets form the database

    Kwargs:

        id (int or None): if None, obtain a listing of all applicable
            images. Otherwise, obtain the information for a specific
            dataset.

        dataset (int or None): limit image(s) to given dataset, if
            any.
        
        extra_info (set of strings): if given, some extra
            information (through other tables) is obtained from the
            database. Each string can be one of:

            - ntotalsources: total number of sources (found by
              sourcefinder) for this image.

            Note that a tuple or list of strings is valid input, but
            will be transformed into a set, to filter out double
            strings.

     Returns:

        (list): A list of dicts; each list item corresponds to a
            single database row, while each dict contains the values
            for the columns (with the column names the keys; some
            column values are available twice, with a different
            key). For a single image, the returned value is a
            single-element list.
    """

    db = DataBase(**dblogin) if dblogin else DataBase()
    extra_info = set(extra_info)
    if id is not None:  # id = 0 could be valid for some databases
        if dataset is not None:
            db.execute(
"""SELECT * FROM images WHERE image_id = %s AND ds_id = %s""", id, dataset)
        else:
            db.execute(
"""SELECT * FROM images WHERE dsid = %s""", id)
    else:
        if dataset is not None:
            db.execute("""SELECT * FROM images WHERE ds_id = %s""", dataset)
        else:
            db.execute("""SELECT * FROM images""")
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    images = []
    for row in db.cursor.fetchall():
        images.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into slightly nicer keys
        for key1, key2 in zip(
            ['imageid', 'taustart_ts', 'tau_time', 'freq_eff', 'freq_bw',
             'ds_id'],
            ['id', 'obsstart', 'inttime', 'frequency', 'bandwidth',
             'dataset']):
            images[-1][key2] = images[-1][key1]
        # Open image to obtain phase center
        img = open_image(images[-1]['url'], dblogin=dblogin)
        header = img.get_header()
        try:
            images[-1]['ra'] = header['phasera']
            images[-1]['dec'] = header['phasedec']
        except KeyError:
            images[-1]['ra'] = None
            images[-1]['Dec'] = None
        if 'ntotalsources' in extra_info:
            query = """\
SELECT COUNT(*) FROM extractedsources WHERE image_id = %s"""
            images[-1]['ntotalsources'] = db.getone(
                query, images[-1]['id'])[0]
    return images


def transient(id=None, dataset=None, dblogin=None):
    """Get information on one or more datasets form the database

    Kwargs:

        id (int or None): if None, obtain a listing of all applicable
            images. Otherwise, obtain the information for a specific
            dataset.

        dataset (int or None): limit image(s) to given dataset, if
            any.
        
     Returns:

        (list): A list of dicts; each list item corresponds to a
            single database row, while each dict contains the values
            for the columns (with the column names the keys; some
            column values are available twice, with a different
            key). For a single image, the returned value is a
            single-element list.
    """

    db = DataBase(**dblogin) if dblogin else DataBase()
    if id is not None:  # id = 0 could be valid for some databases
        if dataset is not None:
            db.execute("""\
SELECT * FROM transients tr, runningcatalog rc
WHERE tr.transientid = %s AND tr.xtrsrc_id = rc.xtrsrc_id AND rc.ds_id = %s""",
                       id, dataset)
        else:
            db.execute("""\
SELECT * FROM transients WHERE transientsid = %s""", id)
    else:
        if dataset is not None:
            db.execute("""\
SELECT * FROM transients tr, runningcatalog rc
WHERE tr.xtrsrc_id = rc.xtrsrc_id AND ds_id = %s""", dataset)
        else:
            db.execute("""SELECT * FROM transients""")
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    transients = []
    for row in db.cursor.fetchall():
        transients.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into somewhat nicer keys
        for key1, key2 in zip(
            ['transientid', 't_start'],
            ['id', 'startdate']):
            transients[-1][key2] = transients[-1][key1]
        n = transients[-1]['datapoints']
        transients[-1]['siglevel'] = chisqprob(
            transients[-1]['siglevel'] * n, n)
    return transients


def source(id=None, dataset=None, dblogin=None):
    """Get information on one or sources from the database

    The sources obtained are those in the runningcatalog; these are the
    unique (= with associations) sources.
    
    Kwargs:

        id (int or None): if None, obtain a listing of all applicable
            sources. Otherwise, obtain the information for a specific
            dataset.

        dataset (int or None): limit image(s) to given dataset, if
            any.
        
     Returns:

        (list): A list of dicts; each list item corresponds to a
            single database row, while each dict contains the values
            for the columns (with the column names the keys; some
            column values are available twice, with a different
            key). For a single image, the returned value is a
            single-element list.
    """

    db = DataBase(**dblogin) if dblogin else DataBase()
    if id is not None:  # id = 0 could be valid for some databases
        if dataset is not None:
            db.execute("""
SELECT * FROM runningcatalog
WHERE xtrsrc_id = %s AND ds_id = %s""", id, dataset)
        else:
            db.execute("""\
SELECT * FROM runningcatalog WHERE xtrsrc_id = %s""", id)
    else:
        if dataset is not None:
            db.execute("""\
SELECT * FROM runningcatalog WHERE ds_id = %s""", dataset)
        else:
            db.execute("""SELECT * FROM runningcatalog""")
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    sources = []
    for row in db.cursor.fetchall():
        sources.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into somewhat nicer keys
        for key1, key2 in zip(
            ['xtrsrc_id', 'ds_id'],
            ['id', 'dataset']):
            sources[-1][key2] = sources[-1][key1]
    return sources


def extractedsource(id=None, dataset=None, image=None, dblogin=None):
    """Get information on one or more extractedsources from the
    database

    Kwargs:

        id (int or None): if None, obtain a listing of all applicable
            sources. Otherwise, obtain the information for a specific
            dataset.

        dataset (int or None): limit image(s) to given dataset, if
            any.

        image (int or None): limit sources to given image. If the
            image is not in the dataset, an empty list will be
            returned.
        
     Returns:

        (list): A list of dicts; each list item corresponds to a
            single database row, while each dict contains the values
            for the columns (with the column names the keys; some
            column values are available twice, with a different
            key). For a single image, the returned value is a
            single-element list.
    """

    db = DataBase(**dblogin) if dblogin else DataBase()
    if id is not None:  # id = 0 could be valid for some databases
        if dataset is not None:
            if image is not None:
                db.execute("""
SELECT * FROM extractedsources ex, images im
WHERE ex.xtrsrcid = %s AND ex.image_id = im.imageid AND
im.ds_id = %s and ex.image_id = %s""", id, dataset, image)
            else:
                db.execute("""
SELECT * FROM extractedsources ex, images im
WHERE ex.xtrsrcid = %s AND ex.image_id = im.imageid AND
im.ds_id = %s""", id, dataset)
        else:
            if image is not None:
                db.execute("""\
SELECT * FROM extractedsources WHERE xtrsrcid = %s
AND image_id = %s""", id, image)
            else:
                db.execute("""\
SELECT * FROM extractedsources WHERE xtrsrcid = %s""", id)
    else:
        if dataset is not None:
            if image is not None:
                db.execute("""\
SELECT * FROM extractedsources ex, images im
WHERE ex.image_id = im.imageid AND im.ds_id = %s
AND ex.image_id = %s""", dataset, image)
            else:
                db.execute("""\
SELECT * FROM extractedsources ex, images im
WHERE ex.image_id = im.imageid AND im.ds_id = %s""", dataset)
        else:
            if image is not None:
                db.execute("""\
SELECT * FROM extractedsources WHERE image_id = %s""", image)
            else:
                db.execute("""SELECT * FROM extractedsources""")
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    sources = []
    for row in db.cursor.fetchall():
        sources.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into somewhat nicer keys
        for key1, key2 in zip(
            ['xtrsrcid', 'image_id'],
            ['id', 'image']):
            sources[-1][key2] = sources[-1][key1]
        sources[-1]['flux'] = {'peak': [], 'int': []}
        for stokes in "iquv":
            for fluxtype in ('peak', 'int'):
                sources[-1]['flux'][fluxtype].append(
                    {'stokes': stokes, 
                     'value': sources[-1][stokes+"_"+fluxtype],
                     'error': sources[-1][stokes+"_"+fluxtype+"_err"]}
                    )
    return sources


def monitoringlist(dataset=dataset, dblogin=None):

    db = DataBase(**dblogin) if dblogin else DataBase()
    # Get all user defined entries
    query = """\
SELECT * FROM monitoringlist WHERE userentry = TRUE"""
    db.execute(query)
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    sources = []
    for row in db.cursor.fetchall():
        sources.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into somewhat nicer keys;
        for key1, key2 in zip(
            ['monitorid', 'image_id'],
            ['id', 'image']):
            sources[-1][key2] = sources[-1][key1]
    # Get all non-user entries belonging to this dataset
    query = """\
SELECT * FROM monitoringlist ml, runningcatalog rc
WHERE ml.userentry = FALSE AND ml.xtrsrc_id = rc.xtrsrc_id AND rc.ds_id = %s"""
    db.execute(query, dataset)
    description = dict(
        [(d[0], i) for i, d in enumerate(db.cursor.description)])
    for row in db.cursor.fetchall():
        sources.append(
            dict([(key, row[column])
                  for key, column in description.iteritems()]))
        # Format into somewhat nicer keys;
        # replace ra, dec by values from runningcatalog
        for key1, key2 in zip(
            ['monitorid', 'image_id', 'wm_ra', 'wm_decl'],
            ['id', 'image', 'ra', 'decl']):
            sources[-1][key2] = sources[-1][key1]
    db.close()
    return sources


def update_monitoringlist(ra, dec, dblogin=None):
    db = DataBase(**dblogin) if dblogin else DataBase()
    query = """\
INSERT INTO monitoringlist
(xtrsrc_id, ra, decl, userentry)
VALUES (-1, %s, %s, TRUE)"""
    db.execute(query, ra, dec)
    db.commit()
    db.close()


def lightcurve(srcid, dblogin=None):
    db = DataBase(**dblogin) if dblogin else DataBase()
    lc = ExtractedSource(id=srcid, database=db).lightcurve()
    db.close()
    return lc




# # # #  Old stuff, for backup

#class AllView(TemplateResponseMixin, View):
#    template_name = "dataset/index.html"
#
#    def _listing(self):
#        """List all available datasets, together with a bit of
#        extra information"""
#        
#        datasets = []
#        self.db.execute("""SELECT * FROM datasets""")
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#	for row in self.db.cursor.fetchall():
#            datasets.append(
#                dict([(key, row[column])
#                      for key, column in description.iteritems()]))
#            query = """\
#            SELECT COUNT(*) FROM transients tr, extractedsources ex
#            WHERE tr.xtrsrc_id = ex.xtrsrcid
#            AND ex.image_id in (SELECT imageid from images im, datasets ds WHERE im.ds_id = ds.dsid AND ds.dsid = %s)
#            """
#            datasets[-1]['ntransients'] = self.db.getone(query, (datasets[-1]['dsid'],))[0]
#        return {'datasets': datasets}
#
#    def _dataset(self, dsid):
#        """List details for single dataset"""
#
#        self.db.execute("""SELECT * FROM datasets WHERE dsid = %s""", (dsid,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.cursor.fetchone()
#        dataset = dict([(key, row[column]) for key, column in
#                        description.iteritems()])
#        return {'dataset': dataset}
#    
#    def _table(self, dsid, table):
#        """List details for requested table"""
#
#        tables = {
#            'image': {'query': ("images", 'ds_id = %s'), 'id': 'imageid'},
#            'source': {'query': ("runningcatalog", 'ds_id = %s'), 'id': 'xtrsrc_id'},
#            'extractedsource': {'query': ("extractedsources ex, images im",
#                                          "ex.image_id = rc.image_id and ex.ds_id = %s"),
#                                'id': 'xtrsrc_id'},
#            'transient': {'query': ("transients tr, runningcatalog rc",
#                                    "tr.xtrsrc_id = rc.xtrsrc_id and rc.ds_id = %s"),
#                          'id': 'transientid'},
#                  }
#        listing = []
#        query = """SELECT * FROM %s WHERE %s""" % tables[table]['query']
#        self.db.execute(query, (dsid,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        for row in self.db.cursor.fetchall():
#            listing.append(
#                dict([(key, row[column])
#                      for key, column in description.iteritems()]))
#            listing[-1]['id'] = listing[-1][tables[table]['id']]
#        d = {'listing': listing}
#        d.update(self._dataset(dsid))
#        return d
#    
#    def _row(self, dsid, table, row):
#        """List single item for requested table"""
#
#        tables = {
#            'image': ("images", 'imageid = %s'),
#            'source': ("runningcatalog", "xtrsrc_id = %s"),
#            'extractedsource': ("extractedsources", "ex.xtrsrc_id = %s"),
#            'transient': ("transients", "transientid = %s"),
#                  }
#        query = """SELECT * FROM %s WHERE %s""" % tables[table]
#        self.db.execute(query, (row,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.fetchone()
#        data = dict([(key, row[column]) for key, column in
#                        description.iteritems()])
#        d = {'data': data}
#        d.update(self._dataset(dsid))
#        return d
#    
#    def get(self, request, dataset=None, table=None, row=None):
#        #name = request.session['database']
#        #self.db = DataBase(host='heastro1', name=name, user=name, password=name)
#        self.db = DataBase()
#
#        if not dataset:
#            self.template_name = 'dataset/listing.html'
#            return self.render_to_response(self._listing())
#        elif not table:
#            self.template_name = 'dataset/single.html'
#            return self.render_to_response(self._dataset(dataset))
#        elif not row:
#            self.template_name = 'dataset/table.html'
#            d = {'name': table}
#            d.update(self._table(dataset, table))
#            return self.render_to_response(d)
#        else:
#            self.template_name = 'dataset/row.html'
#            d = {'name': table}
#            d.update(self._row(dataset, table, row))
#            return self.render_to_response(d)
#
