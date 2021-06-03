from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from catalogs.models import Product
from elasticsearch_dsl import analyzer

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class ProductDocument(Document):
    text = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Product
        fields = ('id', 'name', 'sex',)