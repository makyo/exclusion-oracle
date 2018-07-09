from django.db import models


class RuleBase(models.Model):
    POLICY_CHOICES = (
        ('b', 'block'),
        ('a', 'allow'),
        ('r', 'robots'),
    )

    policy = models.CharField(max_length=1, choices=POLICY_CHOICES)
    surt = models.TextField()
    capture_start = models.DateField()
    capture_end = models.DateField()
    retrieval_start = models.CharField(max_length=10)
    retrieval_end = models.CharField(max_length=10)
    seconds_since_capture = models.IntegerField()
    who = models.CharField(max_length=50)
    private_comment = models.TextField(blank=True)
    public_comment = models.TextField(blank=True)
    enabled = models.BooleanField()

    class Meta:
        abstract = True

    def populate(self, values):
        self.surt = values['surt']
        self.capture_start = values['capture_start']
        self.capture_end = values['capture_end']
        self.retrieval_start = values['retrieval_start']
        self.retrieval_end = values['retrieval_end']
        self.seconds_since_capture = values['seconds_since_capture']
        self.who = values['who']
        self.public_comment = values['public_comment']
        self.private_comment = values['private_comment']
        self.enabled = values['enabled']


class Rule(RuleBase):

    def summary(self):
        return {
            'id': self.id,
            'policy': self.get_policy_display(),
            'surt': self.surt,
            'capture_start': self.capture_start,
            'capture_end': self.capture_end,
            'retrieval_start': self.retrieval_start,
            'retrieval_end': self.retrieval_end,
            'seconds_since_capture': self.seconds_since_capture,
            'who': self.who,
            'public_comment': self.public_comment,
            'enabled': self.enabled,
        }

    def full_values(self):
        summary = self.summary()
        summary['private_comment'] = self.private_comment
        return summary


class RuleChange(RuleBase):
    TYPE_CHOICES = (
        ('c', 'created'),
        ('u', 'updated'),
        ('d', 'deleted'),
    )
    rule = models.ForeignKey(
        Rule,
        on_delete=models.CASCADE,
        related_name='rule_change')
    change_date = models.DateField(auto_now=True)
    change_user = models.TextField()
    change_comment = models.TextField()
    change_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def summary(self):
        return {
            'id': self.id,
            'rule_id': self.rule.id,
            'date': self.change_date,
            'user': self.change_user,
            'comment': self.change_comment,
            'type': self.get_change_type_display(),
        }
