import json

from django.shortcuts import render
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from .models import (
    Rule,
    RuleChange,
)
from .utils.json import (
    error,
    success,
)
from .utils.surt import Surt
from .utils.tree import tree_for_surt
from .utils.validators import (
    RuleValidationException,
    validate_rule_json,
)


class RulesView(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('surt-exact') is not None:
            rules = Rule.objects.filter(surt=request.GET.get('surt-exact'))
        elif request.GET.get('surt-start') is not None:
            rules = Rule.objects.filter(
                surt__startswith=request.GET.get('surt-start'))
        else:
            rules = Rule.objects.all()
        return success([rule.summary() for rule in rules])

    def put(self, request, *args, **kwargs):
        try:
            new_rule = json.loads(request.body)
        except Exception as e:
            return error('unable to marshal json', str(e))
        try:
            validate_rule_json(new_rule)
        except RuleValidationException as e:
            return error('error validating json', str(e))
        rule = Rule()
        rule.populate(new_rule)
        rule.save()
        return success(rule.summary())


class RuleView(SingleObjectMixin, View):

    model = Rule

    def get(self, request):
        rule = self.get_object()
        return success(rule.summary())

    def post(self, request, *args, **kwargs):
        rule = self.get_object()
        try:
            updates = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return error('unable to marshal json', str(e))
        try:
            validate_rule_json(updates)
        except RuleValidationException as e:
            return error('error validating json', str(e))
        change = RuleChange(
            rule=rule,
            change_user=updates['user'],
            change_comment=updates['comment'])
        change.populate(rule.full_values())
        if rule.enabled and not updates['enabled']:
            change.change_type = 'd'
        else:
            change.change_type = 'u'
        change.save()
        rule.populate(updates)
        rule.save()
        return success({
            'rule': rule.summary(),
            'change': change.summary(),
        })

    def delete(self, request, *args, **kwargs):
        rule = self.get_object()
        rule.delete()
        return success({})


def tree(request, surt_string):
    surt = Surt(surt_string)
    tree = [rule.summary() for rule in tree_for_surt(surt)]
    return success(tree)


def decide(request):
    surt = request.GET.get('surt')
    warc = request.GET.get('warc')
    capture_date = request.GET.get('capture-date')
    if surt is None or warc is None or capture_date is None:
        return error('surt, warc, and capture-date query string params'
                     ' are all required', {})
