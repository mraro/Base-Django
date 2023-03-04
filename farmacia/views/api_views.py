import os

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.views.generic import DetailView

from utility.paginator import make_pagination
from .class_views import ObjectListViewBase
from farmacia.models import Remedios

RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


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


class ApiCategoryView(ObjectListViewBase):
    template_name = 'pages/category-view.html'

    # TODO

    # def render_to_response(self, context, **response_kwargs):
    #     return JsonResponse()


class ApiSearchView(ObjectListViewBase):
    ...  # TODO


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

        del object_dict['preparetion_steps']
        del object_dict['preparetion_steps_is_html']

        return JsonResponse(object_dict,
                            safe=False, )
