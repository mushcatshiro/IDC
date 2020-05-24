from django.shortcuts import render, redirect
from .forms import requestForm
from .models import RequestModel
from .tasks import prepareDataLabelProject
from .dboperations import get_top_empty_row
from django.contrib import messages
# from django.http import HttpResponse

# Create your views here.


def index(request):
    # index should show all projects
    # pagination
    # sleepy.delay()
    return render(request, 'datalabel/index.html',
                  {'projects': RequestModel.objects.all()})


def projectRequestForm(request):
    # form for user to fill in
    if request.method == 'POST':
        form = requestForm(request.POST)
        if form.is_valid():
            form.save()
            prepareDataLabelProject.delay(dictObj=form.cleaned_data)
            return redirect('datalabel-index')
    else:
        form = requestForm()
    return render(request, 'datalabel/projectrequestform.html', {'form': form})


def projectDetail(request, id):
    detail = RequestModel.objects.get(id=id)
    context = {
        'detail': detail
    }
    return render(request, 'datalabel/projectdetail.html', context)


# generate dynamic selection
def getNextItem(request):
    # get image
    # labaled = False
    # if get_top_empty_row is None:
    #     messages.add_message(request, messages.INFO,
    #                          'all data has been labeled')
    #     labaled = True
    # # add indicator variable to get labeled category
    # context = {
    #     'imageFullDir': 'some dir query'
    # }

    # if labeled:
    #     context['label'] = 'some queried label'

    return render(request, 'datalabel/labelitem.html', context)


def addToProcessQueue():
    pass