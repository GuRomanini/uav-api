from xml.etree import ElementTree
from falcon import media


class XMLHandler(media.BaseHandler):
    def deserialize(self, stream, content_type, content_length):
        return ElementTree.fromstring(stream.read())

    def serialize(self, media, content_type):
        return media
