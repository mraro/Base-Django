from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from authors.forms import EditObjectForm
from farmacia import models


# THIS DECORATOR IS UTIL LIKE A FUNC BASE TO VIEW, BUT HERE WE HAVE TO USER @method_decorator and in the end use
# name='dispatch' to refer where @login_required will be affecting (dispatch is in doc of django)
@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class BaseObjectClassedView(View):
    def get_objects_to_view(self, id_obj):
        return models.Remedios.objects.filter(id=id_obj, is_published=False, author=self.request.user).first()

    def render_view(self, form, id):
        if id is not None:
            title_site = 'Editar'
        else:
            title_site = 'Criar'

        return render(self.request, 'pages/edit_obj_view.html', context={
            # 'remedio': remedio[0],
            'form': form,
            'form_button': 'Salvar',
            'edit': 'tru',
            'title': title_site,
        })

    def get(self, request, idobject=None):
        remedio = self.get_objects_to_view(idobject)
        form = EditObjectForm(
            instance=remedio  # fill the fields with sent data
        )
        return self.render_view(form, idobject)

    def post(self, request, idobject=None):
        remedio = self.get_objects_to_view(idobject)
        author = models.User.objects.get(username=request.user)

        form = EditObjectForm(
            data=request.POST or None,  # receive a request data or none
            files=request.FILES or None,
            instance=remedio  # if none receive what will be edited
        )
        if form.is_valid():
            object_data = form.save(commit=False)
            object_data.is_published = False
            object_data.author = author
            object_data.save()

            if idobject is not None:
                messages.success(request, "Remedio Salvo")
            else:
                messages.success(request, "Remedio criado e enviado a analise")

            return redirect(reverse('authors:dashboard'))

        return self.render_view(form, idobject)


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class ObjectClassedViewDelete(BaseObjectClassedView):
    def get(self, *args, **kwargs):
        raise Http404

    def post(self, *args, **kwargs):

        remedio = self.get_objects_to_view(kwargs['idobject'])
        titulo = remedio.title

        if remedio.delete():
            messages.success(self.request, f"{titulo} deletado!")
        else:
            messages.error(self.request, f"{titulo} não foi deletado!")

        return redirect(reverse('authors:dashboard'))
