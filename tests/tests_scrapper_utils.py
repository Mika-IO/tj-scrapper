from app.scrapper.utils import validate_process_number
from app.scrapper.utils import is_valid_uuid
from app.scrapper.utils import first_level_url
from app.scrapper.utils import second_level_url
from app.scrapper.utils import has_second_level
from app.scrapper.utils import get_soup
from app.scrapper.utils import get_text
from app.scrapper.utils import get_parts
from app.scrapper.utils import get_moves

from bs4 import BeautifulSoup

from unittest.mock import patch
import unittest


class TestIsValidUUID(unittest.TestCase):
    def test_valid_uuid(self):
        # Testando com UUIDs válidos
        self.assertTrue(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479"))
        self.assertTrue(is_valid_uuid("6ba7b810-9dad-11d1-80b4-00c04fd430c8"))
        self.assertTrue(is_valid_uuid("123e4567-e89b-12d3-a456-426655440000"))

    def test_invalid_uuid(self):
        # Testando com entradas inválidas
        self.assertFalse(is_valid_uuid("invalid-uuid"))
        self.assertFalse(
            is_valid_uuid("123e4567-e89b-12d3-a456-42665544000")
        )  # Tamanho inválido
        self.assertFalse(
            is_valid_uuid("123e4567-e89b-12d3-a456-42665544000g")
        )  # Caractere inválido


class TestProcessNumberValidation(unittest.TestCase):
    def test_valid_process_number(self):
        valid_process_number = "0710802-55.2018.8.02.0001"
        self.assertTrue(validate_process_number(valid_process_number))

    def test_invalid_process_number(self):
        invalid_process_number = "1234567-89.2021.0.00.0000"
        self.assertFalse(validate_process_number(invalid_process_number))

    def test_invalid_process_number(self):
        invalid_process_number = "Roberto Carlos"
        self.assertFalse(validate_process_number(invalid_process_number))


class TestFirstLevelUrl(unittest.TestCase):
    def test_valid_base_url_and_process_number(self):
        base_url = "http://example.com/api"
        process_number = "12345"
        expected_url = "http://example.com/api?processo.numero=12345"
        result = first_level_url(base_url, process_number)
        self.assertEqual(result, expected_url)


class TestSecondLevelUrl(unittest.TestCase):
    def test_valid_base_url_and_process_number(self):
        base_url = "http://example.com/api"
        process_number = "12345"
        expected_url = "http://example.com/api?processo.codigo=12345"
        result = second_level_url(base_url, process_number)
        self.assertEqual(result, expected_url)


class TestHasSecondLevel(unittest.TestCase):
    @patch("app.scrapper.utils.get_soup")
    def test_has_second_level_with_process_code(self, mock_get_soup):
        mock_get_soup.return_value.find.return_value.get.return_value = "12345"

        base_url = "example.com"
        process_number = "202300000001234567890"

        has, process_code = has_second_level(base_url, process_number)

        self.assertTrue(has)
        self.assertEqual(process_code, "12345")

    @patch("app.scrapper.utils.get_soup")
    def test_has_second_level_without_process_code(self, mock_get_soup):
        mock_get_soup.return_value.find.return_value = None

        base_url = "example.com"
        process_number = "202300000001234567890"

        has, process_code = has_second_level(base_url, process_number)

        self.assertFalse(has)
        self.assertEqual(process_code, "")


class TestGetSoup(unittest.TestCase):
    def setUp(self):
        self.url = "http://example.com"  # URL fictícia para testes
        self.content = b"<html><body><p>Hello, world!</p></body></html>"  # Conteúdo fictício da página

    @patch("app.scrapper.utils.requests.get")
    def test_get_soup(self, mock_get):
        mock_get.return_value = unittest.mock.Mock()
        mock_get.return_value.content = self.content

        soup = get_soup(self.url)

        self.assertIsInstance(soup, BeautifulSoup)

        self.assertEqual(soup.p.get_text(), "Hello, world!")

        mock_get.assert_called_once_with(self.url, verify=False)


class TestGetTextFunction(unittest.TestCase):
    def setUp(self):
        self.html_page = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <div id="tag1">This is some text</div>
                <div id="tag2">  Another   text   with  extra    spaces  </div>
            </body>
        </html>
        """
        self.soup = BeautifulSoup(self.html_page, "html.parser")

    def test_valid_tag_id(self):
        expected_result = "This is some text"
        result = get_text("http://example.com", self.soup, "tag1")
        self.assertEqual(result, expected_result)

    def test_invalid_tag_id(self):
        expected_result = ""
        result = get_text("http://example.com", self.soup, "non_existent_tag")
        self.assertEqual(result, expected_result)

    def test_empty_html_page(self):
        empty_soup = BeautifulSoup("", "html.parser")
        expected_result = ""
        result = get_text("http://example.com", empty_soup, "tag1")
        self.assertEqual(result, expected_result)

    def test_extra_spaces_in_empty_tag(self):
        empty_soup_with_spaces = BeautifulSoup(
            "<div id='empty_tag'>   </div>", "html.parser"
        )
        expected_result = ""
        result = get_text("http://example.com", empty_soup_with_spaces, "empty_tag")
        self.assertEqual(result, expected_result)

class TestGetMoves(unittest.TestCase):

    def setUp(self):
        # Sample HTML content to be used for testing
        self.sample_html = """
            <html>
                <body>
                    <div>
                        <table id="sample_table">
                            <tr class="fundoClaro">
                                <td> 2023-08-01 </td>
                                <td> Some other data </td>
                                <td> Description 1 </td>
                            </tr>
                            <tr class="fundoClaro">
                                <td> 2023-08-02 </td>
                                <td> Some other data </td>
                                <td> Description 2 </td>
                            </tr>
                            <tr class="fundoClaro">
                                <td> 2023-08-03 </td>
                                <td> Some other data </td>
                                <td> Description 3 </td>
                            </tr>
                        </table>
                    </div>
                </body>
            </html>
        """

    def test_get_moves(self):
        # Create a BeautifulSoup object from the sample HTML content
        soup = BeautifulSoup(self.sample_html, 'html.parser')

        # Test case 1: Check if function returns correct moves
        expected_moves = [
            {"date": "2023-08-01", "description": "Description 1"},
            {"date": "2023-08-02", "description": "Description 2"},
            {"date": "2023-08-03", "description": "Description 3"}
        ]
        moves = get_moves(soup, tag_id="sample_table")
        self.assertEqual(moves, expected_moves)

