# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from django import forms

from PlatApp.models import MDEditorForm


class MDEditorModleForm(forms.ModelForm):

    class Meta:
        model = MDEditorForm
        fields = '__all__'
