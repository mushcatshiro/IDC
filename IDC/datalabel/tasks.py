from celery import shared_task
# from dboperations import *
from time import sleep
import os
import pandas as pd
from shutil import copy2
from .dboperations import initialize_project, update_status_ready,\
                          check_table_labeling_complete,\
                          get_table_category, update_status_exported


PROJECT_DUMPS = '/home/shiro/dumps'

@shared_task
def prepareDataLabelProject(dictObj=None):
    # get all files in the given directory
    # create a DataFrame including index, full dir, filename, category
    # save dataframe to database
    # update datalabel_requestmodel ready column to ready
    # expect to be root dir with files (no extra folders)
    projectRootDir = dictObj.get('projectRootDir')
    categories = dictObj.get('categories')

    fullDirList = []
    for root, folders, files in os.walk(projectRootDir):
        for file in files:
            fullDirList.append(os.path.join(root, file))

    fileNameList = [files for _, _, files in os.walk(projectRootDir)][0]

    categoryList = ['no cat' for x in range(len(fileNameList))]

    locked = ['' for x in range(len(fileNameList))]

    assert len(fullDirList) == len(fileNameList)
    assert len(categoryList) == len(fullDirList)

    data = {
        'fullDir': fullDirList,
        'fileName': fileNameList,
        'category': categoryList,
        'locked': locked
    }

    # print(data)
    name = dictObj.get('projectName')
    df = pd.DataFrame(data)
    initialize_project(df, name)
    update_status_ready(name=name)
    return 'success'


@shared_task
def executeFileSorting(tableName):
    # ensure project category dont have empty column
    # create all required folders
    # move files to corresponding folders
    # update datalabel_requestmodel ready column to completed
    returnTable = check_table_labeling_complete(tableName=tableName)
    if returnTable:
        categories = get_table_category(projectName=tableName)

        # pre create a new tree of folders
        os.mkdir(os.path.join(PROJECT_DUMPS, projectName))
        for category in categories:
            os.mkdir(os.path.join(PROJECT_DUMPS, projectName, category))

        errorCtr = 0

        for row in range(len(returnTable)):
            # get returnTable[i, 'fullDir'], returnTable[i, 'category']
            # to move or to copy?
            try:
                copy2(returnTable[i, 'fullDir'],
                      os.path.join(PROJECT_DUMPS,
                                   projectName,
                                   returnTable[i, 'category']))
            except Exception as e:
                errorCtr += 1

        if errorCtr > 0:
            # write a report
            with open(os.path.join(PROJECT_DUMPS,
                                   projectName,
                                   'report.txt'), 'w') as wf:
                wf.write(f'there exists a total of {errorCtr} file failed to be copied')
        
        update_status_exported(tableName=tableName)
        return 'success'


@shared_task
def sleepy(duration=10):
    sleep(duration)
    os.mkdir('/home/shiro/test')
    return None
