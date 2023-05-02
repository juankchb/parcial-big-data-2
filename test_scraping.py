from unittest.mock import MagicMock, patch
import requests

def make_request(url):
    response = requests.get(url)
    return response.text

def test_make_request():
    # Crear un objeto MagicMock para la respuesta HTTP simulada
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = 'Hello, world!'

    mock_get = MagicMock()
    mock_get.return_value = mock_response

    with patch('requests.get', mock_get):
        result = make_request('http://www.example.com')

    assert result == 'Hello, world!'