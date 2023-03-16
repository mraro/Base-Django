import json
import os

from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.views.generic import DetailView

from utility.paginator import make_pagination
from farmacia.views.class_views import ObjectListViewBase, CategoryView, SearchView, TagView
from farmacia.models import Remedios

RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))

""" JSON MADE BY CLASS VIEW, here just return in json mode """


def list_to_dict(list_data):
    """
    Converte uma lista para um dicionario
    """
    if list_data is None:
        return None
    return {i: list_data[i] for i in range(len(list_data))}


class ApiHomeView(ObjectListViewBase):
    template_name = 'pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        objects = self.get_context_data()['remedios']
        objects_list = objects.object_list.values()
        pages = make_pagination(self.request, context.get('remedios'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        # WAS BETTER DO THIS PACKAGE WITH model_to_dict() INSTEAD

        return JsonResponse(
            ({'objects': list(objects_list),
              'pages': {'current-page': str(pages['pagination']),
                        'middle_range': str(pages['middle_range']),
                        'start_range': str(pages['start_range']),
                        'stop_range': str(pages['stop_range']),
                        'last_range': str(pages['last_range']),
                        'first_page_out_of_range': str(pages['first_page_out_of_range']),
                        'last_page_out_of_range': str(pages['last_page_out_of_range']),
                        'current_page': str(pages['current_page']),
                        'medicines_pag': str(pages['medicines_page']),

                        }

              }),
            safe=False,
        )


class ApiCategoryView(CategoryView):
    template_name = 'pages/category-view.html'

    def render_to_response(self, context, **response_kwargs):
        objects = context['object_list'].values()

        # objects_list = objects.values_list()
        objects_list = list_to_dict(objects)
        pages = self.get_context_data()['pages']
        categoryTitle = self.get_context_data()['categoryTitle']

        return JsonResponse({
            'remedios': objects_list,
            'pages': {'current-page': str(pages['pagination']),
                      'middle_range': str(pages['middle_range']),
                      'start_range': str(pages['start_range']),
                      'stop_range': str(pages['stop_range']),
                      'last_range': str(pages['last_range']),
                      'first_page_out_of_range': str(pages['first_page_out_of_range']),
                      'last_page_out_of_range': str(pages['last_page_out_of_range']),
                      'current_page': str(pages['current_page']),
                      'medicines_pag': str(pages['medicines_page']),

                      },
            'categoryTitle': str(categoryTitle),
            'is_detail': False, },
            safe=False,
        )


class ApiSearchView(SearchView):
    def render_to_response(self, context, **response_kwargs):
        objects = context['object_list'].values()

        # objects_list = objects.values_list()
        objects_list = list_to_dict(objects)
        pages = self.get_context_data()['pages']
        var_site = self.get_context_data()['search_done']

        return JsonResponse((
            {
                'remedios': objects_list,
                'pages': {'current-page': str(pages['pagination']),
                          'middle_range': str(pages['middle_range']),
                          'start_range': str(pages['start_range']),
                          'stop_range': str(pages['stop_range']),
                          'last_range': str(pages['last_range']),
                          'first_page_out_of_range': str(pages['first_page_out_of_range']),
                          'last_page_out_of_range': str(pages['last_page_out_of_range']),
                          'current_page': str(pages['current_page']),
                          'medicines_pag': str(pages['medicines_page']),

                          },
                'search_done': var_site,
            }
        ), safe=False)


class ApiTagView(TagView):
    def render_to_response(self, context, **response_kwargs):
        objects = context['object_list'].values()

        objects_list = list_to_dict(objects)
        pages = self.get_context_data()['pages']

        return JsonResponse((
            {
                'remedios': objects_list,
                'pages': {'current-page': str(pages['pagination']),
                          'middle_range': str(pages['middle_range']),
                          'start_range': str(pages['start_range']),
                          'stop_range': str(pages['stop_range']),
                          'last_range': str(pages['last_range']),
                          'first_page_out_of_range': str(pages['first_page_out_of_range']),
                          'last_page_out_of_range': str(pages['last_page_out_of_range']),
                          'current_page': str(pages['current_page']),
                          'medicines_pag': str(pages['medicines_page']),

                          },

            }
        ), safe=False)


class ApiRemedioView(DetailView):
    # DETAIL VIEW WAITS PK
    model = Remedios

    context_object_name = 'remedio'
    template_name = 'pages/remedio-view.html'

    def render_to_response(self, context, **response_kwargs):
        objects = self.get_context_data()['remedio']
        object_dict = model_to_dict(objects)
        if object_dict['cover']:
            object_dict['cover'] = object_dict['cover'].url
        else:
            object_dict['cover'] = ''

        if object_dict['author']:
            if objects.author.first_name:
                object_dict['author'] = objects.author.first_name
            else:
                object_dict['author'] = objects.author.username
        else:
            object_dict['author'] = ''

        if object_dict['tags']:
            object_dict['tags'] = str(list_to_dict(object_dict['tags']))

        del object_dict['preparetion_steps']
        del object_dict['preparetion_steps_is_html']

        return JsonResponse(object_dict,
                            safe=False, )
