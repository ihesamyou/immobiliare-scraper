import unittest
from unittest.mock import MagicMock, patch
from scraper import Immobiliare
from requests.exceptions import HTTPError


class TestImmobiliare(unittest.TestCase):

    def setUp(self):
        # Set up any necessary resources before each test
        pass

    def tearDown(self):
        # Clean up any resources after each test
        pass

    @patch("scraper.requests.get")
    def test_init(self, mock_requests_get):
        print("_check_url Tests:")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.test.it")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&mapCenter=45.469642%2C9.167833&zoom=13")
        with self.assertRaises(ValueError):
            immo = Immobiliare(url="https://www.immobiliare.it/search-list/?idContratto=2&idCategoria=1&idTipologia%5B0%5D=4&idTipologia%5B1%5D=5&criterio=rilevanza&__lang=it&fkRegione=lom&idProvincia=MI&idComune=8042&idNazione=IT&pag=1")
        with self.assertRaises(HTTPError):
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = HTTPError
            mock_requests_get.return_value = mock_response
            immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza")

        # print("gather_real_estate_data Tests:")
        # with self.assertRaises(KeyError):
        #     immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza")
        # url = "https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza"
        # immo = Immobiliare(url=url, get_data_of_following_pages=True)
        # self.assertIsInstance(immo.response, MagicMock)

    
    # def test_gather_real_estate_data(self, mock_requests_get):
    #     url = "https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&pag=75"
    #     immo = Immobiliare(url=url, get_data_of_following_pages=True)

    #     mock_response = MagicMock()
    #     mock_requests_get.return_value = mock_response
    #     mock_response.status_code = 200
    #     mock_response.text = "Mock response text"

    #     immo.gather_real_estate_data()

    #     self.assertEqual(immo.last_response, mock_response)


if __name__ == '__main__':
    unittest.main()