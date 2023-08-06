from datetime import datetime
from importlib import import_module

from django.conf import settings
from elasticsearch_dsl import Document as OriginDocument


class Document(OriginDocument):

    @classmethod
    def index_name(cls):
        index_meta = getattr(cls, 'Index')
        index_name = getattr(index_meta, 'name')
        return index_name

    @classmethod
    def get_index(cls):
        indexes = list(cls._index.get_alias().keys())
        return cls._index.clone(name=indexes[0])

    @classmethod
    def generate_index(cls):
        index_name = cls.index_name()
        return cls._index.clone(name='-'.join([index_name, datetime.now().strftime('%Y%m%d%H%M%S%f')]))

    @classmethod
    def migrate(cls, reindex):
        if not cls._index.exists():
            next_index = cls.generate_index()
            next_index.aliases(**{cls.index_name(): {}})
            next_index.save()
        else:
            current_index = cls.get_index()
            if not reindex:
                current_index.save()
            else:
                next_index = cls.generate_index()
                next_index.aliases(**{cls.index_name(): {}})
                next_index.save()
                cls._get_connection().reindex(
                    body={"source": {"index": current_index._name}, "dest": {"index": next_index._name}}
                )
                current_index.delete()


class DocumentRegistry:

    def __init__(cls):
        cls._docs = set()

    def register(cls, document):
        cls._docs.add(document)
        return document

    @staticmethod
    def _migrate_doc(doc, reindex):
        doc.migrate(reindex)

    def migrate(cls, reindex=False):
        for doc in cls._docs:
            cls._migrate_doc(doc, reindex)


registry = DocumentRegistry()
for app_path in settings.DOCUMENT_MIGRATE_APPS:
    import_module('.'.join([app_path, 'docs']))
