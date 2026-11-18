# Se importa el marco de pruebas unitarias integrado en la biblioteca estándar del lenguaje.
import unittest


# Se define la función encargada de calcular las emisiones de carbono según el consumo eléctrico.
def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo energético no puede ser un valor negativo.")
    return round(consumo_kwh * factor_emision, 4)


# Se desarrolla la función que procesa el historial de consumos de las plantas industriales.
def obtener_metricas_consumo(registros):
    total_emisiones = 0.0
    consumo_por_planta = {}
    emisiones_por_planta = {}

    for reg in registros:
        nombre_planta = reg["planta"]
        consumo = reg["consumo_kwh"]
        emision_calculada = calcular_emisiones_carbono(consumo)
        total_emisiones += emision_calculada
        consumo_por_planta[nombre_planta] = consumo_por_planta.get(nombre_planta, 0.0) + consumo
        emisiones_por_planta[nombre_planta] = round(
            emisiones_por_planta.get(nombre_planta, 0.0) + emision_calculada, 2
        )

    planta_mayor_consumo = "Sin registros"
    consumo_maximo = 0.0
    if consumo_por_planta:
        planta_mayor_consumo = max(consumo_por_planta, key=consumo_por_planta.get)
        consumo_maximo = round(consumo_por_planta[planta_mayor_consumo], 2)

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_maximo_kwh": consumo_maximo,
        "desglose_plantas": emisiones_por_planta,
        "cantidad_registros": len(registros)
    }


class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_valores_nominales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)
        self.assertAlmostEqual(calcular_emisiones_carbono(250.5), 100.2)

    def test_calculo_consumo_cero_y_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(0), 0.0)
        self.assertAlmostEqual(calcular_emisiones_carbono(100, factor_emision=0.55), 55.0)

    def test_excepcion_consumo_negativo(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)


def render_simulado(request, template_name, context):
    return {"plantilla_objetivo": template_name, "contexto_enviado": context}


def vista_panel_sustentabilidad(request):
    historial_consumos = [
        {"planta": "Planta Norte", "consumo_kwh": 1200.0},
        {"planta": "Planta Sur", "consumo_kwh": 950.0},
        {"planta": "Planta Este", "consumo_kwh": 600.0},
        {"planta": "Planta Norte", "consumo_kwh": 450.0},
        {"planta": "Planta Sur", "consumo_kwh": 800.0}
    ]
    contexto = obtener_metricas_consumo(historial_consumos)
    return render_simulado(request, "sustentabilidad/panel.html", contexto)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculoEmisiones)
    unittest.TextTestRunner(verbosity=2).run(suite)
    print(vista_panel_sustentabilidad(request="PETICION_HTTP_GET"))
