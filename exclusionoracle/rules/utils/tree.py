from rules.models import Rule


def tree_for_surt(surt):
    surt_parts = surt.parts
    tree_surts = []
    while surt_parts != []:
        tree_parts.append(''.join(surt_parts))
        surt_parts.pop
    tree_rules = []
    for tree_part in tree_parts:
        for rule in Rule.objects.filter(surt=tree_part):
            tree_rules.append(rule)
