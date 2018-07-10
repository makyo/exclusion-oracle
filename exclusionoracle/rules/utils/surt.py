# XXX This is a simple implementation of a SURT library and not meant to be authoratitive

class Surt(object):

    def __init__(surt):
        self._surt = surt
        self.protocol, surt = surt.split('://(')
        self.domain, surt = surt.split('/', num=1)
        self.path, surt = surt.split('?')
        self.query, self.hash = surt.split('#')

        self.path_parts = self.path.split('/')
        self.path_parts = [part for part in self.path_parts if part != '']

        self.domain_parts = self.domain.replace(')', '').split(',')
        self.domain_parts = [part for part in self.domain_parts if part != '']

        self.parts = []
        self.parts.append(self.protocol + '://(')
        for domain_part in self.domain_parts:
            self.parts.append(domain_part)
        self.parts[-1] = '{},)'.format(self.parts[-1])
        for path_part in self.path_parts:
            self.parts.append('/{}'.format(path_part))
        self.parts.append(self.query)
        self.parts.append(self.hash)

    def __str__(self):
        return self._surt
