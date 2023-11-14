import unittest
from unittest.mock import MagicMock, patch
from scraper import Immobiliare
from requests.exceptions import HTTPError


class TestImmobiliare(unittest.TestCase):
    @patch("scraper.requests.get")
    def test_check_url(self, mock_requests_get):
        print("_check_url Tests:")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.test.it")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&mapCenter=45.469642%2C9.167833&zoom=13")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.immobiliare.it/search-list/?idContratto=2&idCategoria=1&idTipologia%5B0%5D=4&idTipologia%5B1%5D=5&criterio=rilevanza&__lang=it&fkRegione=lom&idProvincia=MI&idComune=8042&idNazione=IT&pag=1")
        with self.assertRaises(HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = HTTPError
            mock_requests_get.return_value = mock_response
            immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza")


if __name__ == '__main__':
    unittest.main()