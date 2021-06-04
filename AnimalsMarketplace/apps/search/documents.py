from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from catalogs.models import Product
from elasticsearch_dsl import analyzer, tokenizer

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

ngram = analyzer('custom_ngram',
                 tokenizer=tokenizer('custom_ngram_tokenizer', 'ngram', min_gram=1, max_gram=4),
                 filter=["lowercase", "stop", "snowball"],
                 char_filter=["html_strip"])

ngram_text = analyzer('custom_ngram',
                      tokenizer=tokenizer('custom_ngram_tokenizer', 'ngram', min_gram=4, max_gram=10),
                      filter=["lowercase", "stop", "snowball"],
                      char_filter=["html_strip"])


@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(
        analyzer=ngram,
        fields={'raw': fields.KeywordField()}
    )
    text = fields.TextField(
        analyzer=ngram_text,
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_ngram_diff': 10
        }

    class Django:
        model = Product
        fields = ('id', 'sex',)
