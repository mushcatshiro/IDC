from celery import shared_task
# from dboperations import *
from time import sleep
import os
import pandas as pd
from .dboperations import initialize_project, update_status


@shared_task
def prepareDataLabelProject(dictObj=None):
    # get all files in the given directory
    # create a DataFrame including index, full dir, filename, category
    # save dataframe to database
    # update datalabel_requestmodel ready column to ready
    # expect to be root dir with files (no extra folders)
    projectRootDir = dictObj.get('projectRootDir')

    fullDirList = []
    for root, folders, files in os.walk(projectRootDir):
        for file in files:
            fullDirList.append(os.path.join(root, file))

    fileNameList = [files for _, _, files in os.walk(projectRootDir)][0]

    categoryList = ['no cat' for x in range(len(fileNameList))]

    assert len(fullDirList) == len(fileNameList)
    assert len(categoryList) == len(fullDirList)

    data = {
        'fullDir': fullDirList,
        'fileName': fileNameList,
        'category': categoryList
    }

    # print(data)
    name = dictObj.get('projectName')
    df = pd.DataFrame(data)
    initialize_project(df, name)
    update_status(name=name)
    return 'success'


@shared_task
def executeFileSorting():
    # ensure project category dont have empty column
    # create all required folders
    # move files to corresponding folders
    # update datalabel_requestmodel ready column to completed
    pass


@shared_task
def sleepy(duration=10):
    sleep(duration)
    os.mkdir('/home/shiro/test')
    return None
