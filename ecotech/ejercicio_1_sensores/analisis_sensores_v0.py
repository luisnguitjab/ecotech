# Se define la función encargada de normalizar un diccionario con lecturas crudas de un sensor.
def limpiar_registro_sensor(registro_raw):
    """
    Recibe un diccionario con datos crudos de un sensor.
    Retorna un nuevo diccionario estandarizado con tipos de datos limpios y seguros.
    """
    # Se obtiene el valor asociado a la clave del identificador, o una cadena vacía por defecto si no existe.
    sensor_id = registro_raw.get("sensor_id", "").strip()
    
    # Se extrae la cadena de texto de la temperatura, asignando cero en texto si la clave no se encuentra.
    temp_raw = registro_raw.get("temperatura", "0")
    
    # Se reemplaza el sufijo de grados centígrados por una cadena vacía para dejar solo los caracteres numéricos.
    temperatura = float(temp_raw.replace("°C", "").strip())
    
    # Se busca la clave de la ubicación en el registro original.
    ubicacion = registro_raw.get("ubicación", "Sin asignar").strip()
    
    # Se construye y devuelve el nuevo diccionario con la información ya normalizada.
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicación": ubicacion
    }


# Se define la función que analiza la colección de sensores limpios frente a un valor límite.
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Toma una lista de registros sanitizados y un valor numérico de umbral térmico.
    Retorna una tupla con la lista de identificadores en alerta y el promedio térmico global.
    """
    # Se inicializa una lista vacía para guardar los identificadores de los dispositivos que superen el límite.
    lista_sensores_alerta = []
    
    # Se declara un acumulador numérico en cero para sumar todas las temperaturas registradas.
    suma_temperatura = 0.0
    
    # Se recorre cada diccionario dentro de la lista de sensores previamente sanitizados.
    for sensor in lista_sensores_limpios:
        # Se extrae el valor numérico de la temperatura del sensor actual.
        temp = sensor["temperatura"]
        
        # Se suma la temperatura actual al acumulador general de la planta.
        suma_temperatura += temp
        
        # Se verifica si la lectura actual es estrictamente mayor al umbral estipulado.
        if temp > umbral_temperatura:
            # Si supera el límite, se agrega el identificador del dispositivo a la lista de alertas.
            lista_sensores_alerta.append(sensor["sensor_id"])
            
    # Se inicializa la variable del promedio en cero por seguridad antes de dividir.
    promedio_temperatura = 0.0
    
    # Se comprueba que la colección tenga al menos un elemento para evitar un error de división por cero.
    if len(lista_sensores_limpios) > 0:
        # Se divide la suma total por la cantidad de sensores y se redondea el resultado a dos decimales.
        promedio_temperatura = round(suma_temperatura / len(lista_sensores_limpios), 2)
        
    # Se retorna la tupla exacta solicitada conteniendo la lista de alertas y el promedio calculado.
    return (lista_sensores_alerta, promedio_temperatura)


# Se establece el bloque de ejecución principal que se corre solo al ejecutar este archivo directamente.
if __name__ == "__main__":
    datos_crudos = [
        {"sensor_id": " Sensor-001 ", "temperatura": "24.5 °C", "ubicación": "Planta Norte"},
        {"sensor_id": "Sensor-002", "temperatura": " 30.2°C "},
        {"sensor_id": " Sensor-003 ", "temperatura": "21.1 °C", "ubicación": "Planta Este"},
        {"sensor_id": "  Sensor-004", "temperatura": "35.5°C", "ubicación": "  Horno Principal  "},
        {"sensor_id": "Sensor-005", "temperatura": " -5.4 °C", "ubicación": "Cámara Frigorífica"},
        {"sensor_id": "Sensor-006  ", "temperatura": " 26.0°C"},
        {"sensor_id": "Sensor-007", "temperatura": " 19.9 °C ", "ubicación": "Planta Sur"}
    ]

    print("=" * 78)
    print("1. Registros crudos de entrada sin procesar".center(78))
    print("=" * 78)
    for i, reg in enumerate(datos_crudos, start=1):
        print(f" [{i}] Id: {repr(reg.get('sensor_id')):<15} | Temp: {repr(reg.get('temperatura')):<12} | Ubicación: {repr(reg.get('ubicación', '<No registrada>'))}")

    sensores_sanitizados = [limpiar_registro_sensor(r) for r in datos_crudos]

    print("\n" + "=" * 78)
    print("2. Registros sanitizados tras aplicar la función de limpieza".center(78))
    print("=" * 78)
    for i, reg in enumerate(sensores_sanitizados, start=1):
        print(f" [{i}] Id: '{reg['sensor_id']}' | Temp (float): {reg['temperatura']:>6.2f} | Ubicación: '{reg['ubicación']}'")

    umbral_estipulado = 25.0
    tupla_resumen = generar_resumen_sensores(sensores_sanitizados, umbral_estipulado)

    print("\n" + "=" * 78)
    print("3. Reporte final y tupla de salida".center(78))
    print("=" * 78)
    print(f" Umbral de temperatura estipulado : {umbral_estipulado} °C")
    print(f" Dispositivos que superan umbral  : {tupla_resumen[0]}")
    print(f" Promedio térmico global          : {tupla_resumen[1]} °C")
    print(f" Tupla final                      : {tupla_resumen}")
    print("=" * 78)
