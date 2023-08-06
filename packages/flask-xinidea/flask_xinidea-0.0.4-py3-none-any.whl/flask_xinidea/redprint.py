#


class Redprint(object):
    '''
    A Flask Blueprint extension
    '''

    def __init__(self, bp, url_prefix=None):
        self.bp = bp
        self.url_prefix = url_prefix

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            if self.url_prefix:
                new_rule = self.url_prefix + rule
            else:
                new_rule = rule
            self.bp.add_url_rule(new_rule, endpoint, f, **options)
            return f
        return decorator
