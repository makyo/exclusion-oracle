from django.shortcuts import render
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from models import (
    Rule,
    RuleChange,
)
from utils.json import (
    error,
    success,
)
from utils.validators import (
    RuleValidationException,
    validate_rule_json,
)


class RulesView(View):

    def get(self, request, *args, **kwargs):
        rules = [rule.summary() for rule in Rule.objects.all()]
        return success(rules)

    def put(self, request, *args, **kwargs):
        try:
            new_rule = json.loads(request.body)
        except:
            return error('unable to marshal json')
        try:
            validate_rule_json(new_rule)
        except RuleValidationException as e:
            return error('error validating json: {}'.format(e))
        # Create rule
        # Save


class RuleView(SingleObjectMixin, View):

    def get(self, request):
        rule = self.get_object()
        return HttpResponse(success(rule.summary()))

    def post(self, request, *args, **kwargs):
        rule = self.get_object()
        try:
            updates = json.loads(request.body)
        except:
            return error('unable to marshal json')
        try:
            validate_rule_json(updates)
        except RuleValidationException as e:
            return error('error validating json: {}'.format(e))
        # Copy rule fields to new rulechange and save
        # Update rule
        # Save

    def delete(self, request, *args, **kwargs):
        rule = self.get_object()
        rule.delete()
        return success({})
