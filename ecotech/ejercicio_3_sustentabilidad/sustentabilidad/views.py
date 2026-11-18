from django.shortcuts import render
from .services import obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    registros_planta = [
        {"planta": "Planta Norte", "consumo_kwh": 1200.0},
        {"planta": "Planta Sur", "consumo_kwh": 950.0},
        {"planta": "Planta Este", "consumo_kwh": 600.0},
        {"planta": "Planta Norte", "consumo_kwh": 450.0},
        {"planta": "Planta Sur", "consumo_kwh": 800.0}
    ]
    contexto = obtener_metricas_consumo(registros_planta)
    return render(request, "sustentabilidad/panel.html", contexto)
