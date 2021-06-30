from catalogs.models import Product
from search.documents import ProductDocument, PostDocument
from blog.models import Post
from search.utils import ListSearchMixin, SearchSuggestMixin


class SearchViews(ListSearchMixin):
    model = Product
    search_document = ProductDocument
    additional_dict_model_documents = {'post_list': {
        'model': Post,
        'document': PostDocument,
        'fields': ['name', 'text'],
    }
    }


class SearchSuggestViews(SearchSuggestMixin):
    dict_model_documents = {
        'Объявления': {
            'document': ProductDocument,
            'field': 'name',
            'url': '/product/',
    },
        'Статьи': {
            'document': PostDocument,
            'field': 'name',
            'url': '/blog/post/',
            'slug': True
        }
    }
