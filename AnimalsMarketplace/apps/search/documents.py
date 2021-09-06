from django.utils.safestring import mark_safe
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from catalogs.models import Product
from elasticsearch_dsl import analyzer, tokenizer

from blog.models import Post

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

custom_ngram = analyzer('custom_ngram',
                        tokenizer=tokenizer('custom_ngram_tokenizer', 'ngram', min_gram=1, max_gram=5),
                        filter=["lowercase"], char_filter=["html_strip"])

custom_ngram_text = analyzer('custom_ngram_text',
                             tokenizer=tokenizer('custom_ngram_tokenizer_text', 'edge_ngram', min_gram=4, max_gram=10),
                             filter=["lowercase"], char_filter=["html_strip"])


@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(
        attr='name',
        analyzer=custom_ngram,
        fields={'raw': fields.KeywordField(),
                'suggest': fields.CompletionField()}
    )
    text = fields.TextField(
        analyzer=custom_ngram_text,
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
        fields = ('id',)
        # auto_refresh = False
        # ignore_signals = True


@registry.register_document
class PostDocument(Document):
    name = fields.TextField(
        attr='name',
        analyzer=custom_ngram,
        fields={'raw': fields.KeywordField(),
                'suggest': fields.CompletionField()}
    )
    text = fields.TextField(
        analyzer=custom_ngram_text,
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'blogs'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_ngram_diff': 10
        }

    class Django:
        model = Post
        fields = ('id', 'slug')
        # auto_refresh = False
        # ignore_signals = True
