from errors import NotFoundResource


class SinkResource:
    def __call__(self, *args):
        raise NotFoundResource()
