import unittest
from unittest.mock import patch
import application

class TestApplication(unittest.TestCase):

    @patch("application.f.load_file")
    def setUp(self, mock_load_file):
        """ Configura el cliente de prueba y los datos simulados """
        self.app = application.application.test_client()
        self.app.testing = True

        # Datos simulados
        mock_data = {
            "1": {"name": "Superman", "power": "Flight"},
            "2": {"name": "Batman", "power": "Intelligence"}
        }
        mock_load_file.return_value = mock_data

        # Recargar datos con el mock
        application.data = mock_data

    def test_index(self):
        """ Verifica que la ruta raíz devuelve todos los héroes """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "1": {"name": "Superman", "power": "Flight"},
            "2": {"name": "Batman", "power": "Intelligence"}
        })

    def test_heroe_found(self):
        """ Verifica que se obtiene un héroe por ID """
        response = self.app.get("/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"name": "Superman", "power": "Flight"})

    def test_heroe_not_found(self):
        """ Verifica que se maneja un ID inexistente correctamente """
        response = self.app.get("/99")  # ID inexistente
        self.assertEqual(response.status_code, 500)  # Flask lanzará un error interno

if __name__ == "__main__":
    unittest.main()
