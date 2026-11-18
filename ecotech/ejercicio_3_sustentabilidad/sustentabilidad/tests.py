import unittest
from .services import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_exactitud_nominal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)
        self.assertAlmostEqual(calcular_emisiones_carbono(500), 200.0)

    def test_calculo_consumo_cero(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(0), 0.0)

    def test_elevacion_excepcion_consumo_negativo(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-25)
