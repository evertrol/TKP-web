from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .tools import dbase
from tkp.database.database import DataBase
import tkp.database.dataset as dbset
import tkp.database.utils as tkpdbutils
from tkp.classification.manual.transient import Transient
from tkp.classification.manual.utils import Position
from scipy.stats import chisqprob
import datetime


class DatasetsView(TemplateResponseMixin, View):
    template_name = "dataset/datasets.html"

    def get(self, request):
        """List all available datasets, together with a bit of
        extra information"""

        datasets = dbase.dataset(extra_info=["ntransients"])
        return self.render_to_response(
            {'datasets': datasets}
            )


class DatasetView(TemplateResponseMixin, View):
    template_name = "dataset/dataset.html"

    def get(self, request, id):
        """List details for single dataset"""

        dataset = dbase.dataset(id=id, extra_info=[
            "ntransients", "nimages", "nsources", "ntotalsources"])
        if not dataset:
            raise Http404
        else:
            dataset = dataset[0]
        return self.render_to_response(
            {'dataset': dataset}
            )
    
    
class ImagesView(TemplateResponseMixin, View):
    template_name = "dataset/images.html"

    def get(self, request, dataset):
        images = dbase.image(dataset=dataset, extra_info=['ntotalsources'])
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'images': images,
             'dataset': dataset}
            )


class ImageView(TemplateResponseMixin, View):
    template_name = "dataset/image.html"

    def get(self, request, dataset, id):
        image = dbase.image(dataset=dataset, extra_info=['ntotalsources'])
        if not image:
            raise Http404
        else:
            image = image[0]
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'image': image,
             'dataset': dataset}
            )



class TransientsView(TemplateResponseMixin, View):
    template_name = "dataset/transients.html"

    def get(self, request, dataset):
        transients = dbase.transient(dataset=dataset)
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'transients': transients,
             'dataset': dataset}
            )


class TransientView(TemplateResponseMixin, View):
    template_name = "dataset/transient.html"

    def get(self, request, dataset, id):
        transient = dbase.transient(id=id, dataset=dataset)
        if not transient:
            raise Http404
        else:
            transient = transient[0]
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'transient': transient,
             'dataset': dataset}
            )


class SourcesView(TemplateResponseMixin, View):
    template_name = "dataset/sources.html"

    def get(self, request, dataset):
        sources = dbase.source(dataset=dataset)
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'sources': sources,
             'dataset': dataset}
            )


class SourceView(TemplateResponseMixin, View):
    template_name = "dataset/source.html"

    def get(self, request, dataset, id):
        source = dbase.source(id=id, dataset=dataset)
        if not source:
            raise Http404
        else:
            source = source[0]
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'source': source,
             'dataset': dataset}
            )


class ExtractedSourcesView(TemplateResponseMixin, View):
    template_name = "dataset/extractedsources.html"

    def get(self, request, dataset):
#        self.db = DataBase()
#        self.db.execute("""\
#SELECT * FROM extractedsources ex, images im
#WHERE ex.image_id = im.imageid AND im.ds_id = %s""", (dataset,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        extractedsources = []
#	for row in self.db.cursor.fetchall():
#            extractedsources.append(
#                dict([(key, row[column])
#                      for key, column in description.iteritems()]))
#            # Format into slightly nicer keys
#            for key1, key2 in zip(['xtrsrcid',], ['id',]):
#                extractedsources[-1][key2] = extractedsources[-1][key1]
#            extractedsources[-1]['fluxes'] = {'peak': [], 'int': []}
#            for key in "iquv":
#                extractedsources[-1]['fluxes']['peak'].append(
#                    {'flux': extractedsources[-1][key+"_peak"],
#                     'fluxerror': extractedsources[-1][key+"_peak_err"]}
#                    )
#                extractedsources[-1]['fluxes']['int'].append(
#                    {'flux': extractedsources[-1][key+"_int"],
#                     'fluxerror': extractedsources[-1][key+"_int_err"]}
#                     )
#        self.db.execute("""SELECT * FROM datasets WHERE dsid = %s""", (dataset,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.cursor.fetchone()
#        dataset = dict([(key, row[column]) for key, column in
#                        description.iteritems()])
#        dataset['id'] = dataset['dsid']
        extractedsources = dbase.extractedsource(dataset=dataset)
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'extractedsources': extractedsources,
             'dataset': dataset}
            )


class ExtractedSourceView(TemplateResponseMixin, View):
    template_name = "dataset/extractedsource.html"

    def get(self, request, dataset, id):
#        self.db = DataBase()
#        result = self.db.execute("""\
#SELECT * FROM extractedsources ex, images im
#WHERE ex.xtrsrcid = %s AND ex.image_id = im.imageid AND im.ds_id = %s""",
#                                 (id, dataset))
#        if not result:
#            raise Http404
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.cursor.fetchone()
#        extractedsource = dict([(key, row[column]) for key, column in
#                      description.iteritems()])
#        # Format into slightly nicer keys
#        for key1, key2 in zip(['xtrsrcid'], ['id',]):
#            extractedsource[key2] = extractedsource[key1]
#        extractedsource['flux'] = {'peak': [], 'int': []}
#        for stokes in "iquv":
#            for flux in ('peak', 'int'):
#                extractedsource['flux'][flux].append(
#                    {'stokes': stokes.upper(),
#                     'value': extractedsource[stokes+"_"+flux],
#                     'error': extractedsource[stokes+"_"+flux+"_err"]}
#                    )
#                
#            
#        self.db.execute("""SELECT * FROM datasets WHERE dsid = %s""", (dataset,))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.cursor.fetchone()
#        dataset = dict([(key, row[column]) for key, column in
#                        description.iteritems()])
#        dataset['id'] = dataset['dsid']
#
#        self.db.execute("""SELECT * FROM images WHERE ds_id = %s""", (dataset['id'],))
#        description = dict(
#            [(d[0], i) for i, d in enumerate(self.db.cursor.description)])
#        row = self.db.cursor.fetchone()
#        image = dict([(key, row[column]) for key, column in
#                        description.iteritems()])
#        image['id'] = image['imageid']
        extractedsource = dbase.extractedsource(id=id, dataset=dataset)
        if not extractedsource:
            raise Http404
        else:
            extractedsource = extractedsource[0]
        dataset = dbase.dataset(id=dataset)[0]
        return self.render_to_response(
            {'extractedsource': extractedsource,
             'dataset': dataset}
            )
