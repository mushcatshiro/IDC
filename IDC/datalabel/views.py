from django.shortcuts import render, redirect
from .forms import requestForm
from .models import RequestModel
from .tasks import prepareDataLabelProject, executeFileSorting
from .dboperations import get_table
from django.contrib import messages
from django.core.paginator import Paginator
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


def labelingProject(request, projectName):
    qTable, categoryList = get_table(tableName=projectName)
    # pagination = Paginator(qTable, 50)

    # not sure how it handles if page is not given
    # pageNumber = request.GET.get('page') or 1
    # pageObj = pagination.get_page(pageNumber)
    # pageObj = pageObj.to_json

    context = {
        'qTable': qTable,
        'projectName': projectName
    }

    return render(request, 'datalabel/labelingProject.html', context)


def labelItem(request, pname, fname):
    return render(request, 'done')

"""
# generate dynamic selection
def labelNextItem(request):
    if get_top_empty_row:

        return render(request, 'datalabel/labelitem.html', context)
    else:
        # all labeled for reviewing purpose
        return render(request, 'datalabel/viewitem.html', context)


    return render(request, 'datalabel/labelitem.html', context)


def labelCorrection(request, ):
    return
"""


def addToProcessQueue(request, tableName):
    tableName = tableName
    executeFileSorting.delay(tableName=tableName)
