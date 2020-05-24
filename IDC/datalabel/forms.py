from django.forms import ModelForm
from django import forms
from .models import RequestModel
import os
import re


class requestForm(ModelForm):

    class Meta:

        model = RequestModel
        fields = ['projectName', 'projectDesc', 'projectRootDir',
                  'categories', 'author']

    def clean(self):
        cleaned_data = super().clean()
        projectRootDir = cleaned_data.get("projectRootDir")
        categories = cleaned_data.get("categories")
        pattern = re.compile(r'(.+)+(,.+)+')

        if not os.path.exists(str(projectRootDir)):
            raise forms.ValidationError("project root directory \
                                         does not exist")

        if not re.search(pattern, categories):
            raise forms.ValidationError("categories \
                                         does not match pattern")
