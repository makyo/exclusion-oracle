from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from models import (
    Rule,
    RuleChange,
)
from utils.json import (
    error,
    success,
)


class RulesView(View):

    def get(self, request, *args, **kwargs):
        rules = [rule.summary() for rule in Rule.objects.all()]
        return HttpResponse(success(rules))
