from unittest.mock import patch
from django.test import TestCase
from wagtail.models import Page
from wagtail.search.index import SearchField
from wagtail.search.backends import get_search_backend
from wagtail.test.testapp.models import SimplePage


class TestSearchFields(TestCase):
    """
    Testa o comportamento da adição de um campo de forma dinâmica.
    """

    def setUp(self):
        self.search_backend = get_search_backend()
        self.search_backend.reset_index()

    def test_search_field_added_dynamically_is_indexed(self):
        original_search_fields = SimplePage.search_fields

        new_search_fields = original_search_fields + [
            SearchField("content"),
        ]

        with patch.object(SimplePage, 'search_fields', new_search_fields):
            root_page = Page.objects.get(pk=1)
            page = root_page.add_child(
                instance=SimplePage(
                    title="Página Simples para Teste de Busca",
                    slug="pagina-simples-busca",
                    content="um_termo_unico_e_pesquisavel",
                )
            )

            self.search_backend.refresh_index()
            results = Page.objects.search("um_termo_unico_e_pesquisavel")
            self.assertIn(page, [r.specific for r in results])