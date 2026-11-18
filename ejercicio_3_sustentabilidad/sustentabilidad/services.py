def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo energético no puede ser negativo.")
    return round(consumo_kwh * factor_emision, 4)


def obtener_metricas_consumo(registros):
    total_emisiones = 0.0
    consumo_por_planta = {}
    emisiones_por_planta = {}

    for reg in registros:
        planta = reg["planta"]
        consumo = reg["consumo_kwh"]
        emision = calcular_emisiones_carbono(consumo)
        total_emisiones += emision
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0.0) + consumo
        emisiones_por_planta[planta] = round(emisiones_por_planta.get(planta, 0.0) + emision, 2)

    planta_mayor = max(consumo_por_planta, key=consumo_por_planta.get) if consumo_por_planta else "Sin datos"
    consumo_maximo = round(consumo_por_planta.get(planta_mayor, 0.0), 2)

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor,
        "consumo_maximo_kwh": consumo_maximo,
        "desglose_plantas": emisiones_por_planta,
        "historial_detallado": registros
    }
