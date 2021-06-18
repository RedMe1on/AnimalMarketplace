from catalogs.models import Product
from search.documents import ProductDocument, PostDocument
from blog.models import Post
from search.utils import ListSearchMixin, SearchSuggestMixin


class SearchViews(ListSearchMixin):
    model = Product
    search_document = ProductDocument
    additional_dict_model_documents = {'posts': {
        'model': Post,
        'document': PostDocument,
        'fields': ['name', 'text']
    }
    }


class SearchSuggestViews(SearchSuggestMixin):
    dict_model_documents = {'products': {
        'document': ProductDocument,
        'field': 'name'
    },
        'blog': {
            'document': PostDocument,
            'field': 'name'
        }
    }
