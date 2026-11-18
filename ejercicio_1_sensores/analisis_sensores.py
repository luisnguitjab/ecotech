# Se define la función encargada de normalizar un diccionario con lecturas crudas de un sensor.
def limpiar_registro_sensor(registro_raw):
    """
    Recibe un diccionario con datos crudos de un sensor.
    Retorna un nuevo diccionario estandarizado con tipos de datos limpios y seguros.
    """
    # Se obtiene el valor asociado a la clave del identificador, o una cadena vacía por defecto si no existe.
    # Luego se aplica el método de cadenas para eliminar los espacios en blanco al principio y al final.
    sensor_id = registro_raw.get("sensor_id", "").strip()
    
    # Se extrae la cadena de texto de la temperatura, asignando cero en texto si la clave no se encuentra.
    temp_raw = registro_raw.get("temperatura", "0")
    
    # Se reemplaza el sufijo de grados centígrados por una cadena vacía para dejar solo los caracteres numéricos.
    # Después se quitan los espacios sobrantes de los extremos y se convierte el texto resultante a un número decimal.
    temperatura = float(temp_raw.replace("°C", "").strip())
    
    # Se busca la clave de la ubicación en el registro original.
    # Si el dato no fue registrado, se asigna un texto seguro por defecto y se limpian los espacios laterales.
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
    # Se crea una lista de diccionarios que simula las lecturas crudas y heterogéneas de los microcontroladores.
    datos_crudos = [
        {"sensor_id": " Sensor-001 ", "temperatura": "24.5 °C", "ubicación": "Planta Norte"},
        {"sensor_id": "Sensor-002", "temperatura": " 30.2°C "},  # En este registro se omite la clave de ubicación.
        {"sensor_id": " Sensor-003 ", "temperatura": "21.1 °C", "ubicación": "Planta Este"},
        {"sensor_id": "  Sensor-004", "temperatura": "35.5°C", "ubicación": "  Horno Principal  "},
        {"sensor_id": "Sensor-005", "temperatura": " -5.4 °C", "ubicación": "Cámara Frigorífica"},
        {"sensor_id": "Sensor-006  ", "temperatura": " 26.0°C"},  # En este registro también falta la ubicación.
        {"sensor_id": "Sensor-007", "temperatura": " 19.9 °C ", "ubicación": "Planta Sur"}
    ]

    # Se imprime un encabezado visualmente separado para mostrar el estado inicial de los datos.
    print("=" * 78)
    print("A: Normalización de lecturas (limpiar_registro_sensor)".center(78))
    print("-" * 78)
    print("1º: Registros crudos de entrada sin procesar".center(78))
    print("=" * 78)
    
    # Se itera sobre los datos crudos enumerando cada elemento desde el número uno.
    for i, reg in enumerate(datos_crudos, start=1):
        # Se usa la representación oficial en cadena para que las comillas y espacios sobrantes sean visibles.
        id_crudo = repr(reg.get("sensor_id"))
        temp_cruda = repr(reg.get("temperatura"))
        ubic_cruda = repr(reg.get("ubicación", "<No registrada>"))
        
        # Se muestra en consola cada fila alineando las columnas con espacios fijos.
        print(f" [{i}] Id: {id_crudo:<15} | Temp: {temp_cruda:<12} | Ubicación: {ubic_cruda}")

    # Se imprime una sección intermedia para detallar el proceso de limpieza registro por registro.
    print("\n" + "=" * 78)
    print("2º: proceso de limpieza y transformación de cada registro".center(78))
    print("=" * 78)

    # Se crea una lista vacía donde se irán almacenando los registros a medida que se limpian.
    sensores_sanitizados = []

    # Se recorre cada registro crudo para ejecutar la función de limpieza y mostrar los cambios aplicados.
    for i, reg_crudo in enumerate(datos_crudos, start=1):
        # Se invoca la función de normalización sobre el diccionario crudo actual.
        reg_limpio = limpiar_registro_sensor(reg_crudo)
        
        # Se guarda el diccionario ya estandarizado en la colección de sensores sanitizados.
        sensores_sanitizados.append(reg_limpio)
        
        # Se preparan los valores originales con comillas visibles para compararlos con los valores limpios.
        id_orig = repr(reg_crudo.get("sensor_id"))
        temp_orig = repr(reg_crudo.get("temperatura"))
        tiene_ubicacion = "ubicación" in reg_crudo
        ubic_orig = repr(reg_crudo.get("ubicación")) if tiene_ubicacion else "<Faltante>"
        
        # Se explica en consola cómo se transformó cada campo durante la limpieza del registro actual.
        print(f" [Procesando registro {i}]")
        print(f" - Identificador: {id_orig:<15} -> strip()            -> '{reg_limpio['sensor_id']}'")
        print(f" - Temperatura  : {temp_orig:<15} -> sin '°C' y a float -> {reg_limpio['temperatura']} ({type(reg_limpio['temperatura']).__name__})")
        
        # Se detalla si la ubicación solo requirió quitar espacios o si se asignó el valor por defecto seguro.
        accion_ubic = "strip()    " if tiene_ubicacion else "valor por defecto"
        print(f" - Ubicación    : {ubic_orig:<20} -> {accion_ubic} -> '{reg_limpio['ubicación']}'")

    # Se imprime el tercer bloque visual para presentar los registros ya normalizados.
    print("\n" + "=" * 78)
    print("3º. Registros sanitizados tras aplicar la función de limpieza".center(78))
    print("=" * 78)
    
    # Se recorre la nueva lista de diccionarios limpios para mostrar sus valores formateados.
    for i, reg in enumerate(sensores_sanitizados, start=1):
        # Se imprime el identificador sin espacios, la temperatura con dos decimales y la ubicación validada.
        print(
            f" [{i}] Id: '{reg['sensor_id']}' "
            f"| Temp (float): {reg['temperatura']:>6.2f} "
            f"| Ubicación: '{reg['ubicación']}'"
        )

    # Se define el valor límite de temperatura a partir del cual se dispara una alerta.
    umbral_estipulado = 25.0
    
    # Se extraen únicamente los valores numéricos de temperatura en una lista auxiliar para mostrar el desglose matemático.
    temperaturas = [s["temperatura"] for s in sensores_sanitizados]
    
    # Se calcula la suma total y la cantidad de registros para exhibir la operación en pantalla.
    suma_total = sum(temperaturas)
    cantidad_sensores = len(sensores_sanitizados)

    # Se invoca la función de monitoreo estadístico y se guarda la tupla resultante en una única variable.
    tupla_resumen = generar_resumen_sensores(sensores_sanitizados, umbral_estipulado)

    # Se imprime del punto B, la cuarta sección detallando el cálculo del promedio térmico global de la planta.
    print("\n" + "=" * 78)
    print("B: Monitoreo y mapeo estadístico (generar_resumen_sensores)".center(78))
    print("-" * 78)
    print("4º. Cálculo del promedio térmico global de la planta".center(78))
    print("=" * 78)
    print(f" Valores térmicos registrados : {temperaturas}")
    print(f" Suma térmica acumulada       : {suma_total:.2f} °C")
    print(f" Cantidad total de sensores   : {cantidad_sensores}")
    
    # Se muestra la división explícita accediendo al segundo elemento de la tupla retornada.
    print(f" Operación de promedio        : {suma_total:.2f} / {cantidad_sensores} = {tupla_resumen[1]} °C")

    # Se imprime la quinta sección con el reporte consolidado y la estructura exacta de la tupla.
    print("\n" + "=" * 78)
    print("5º. Reporte final y tupla de salida".center(78))
    print("=" * 78)
    print(f" Umbral de temperatura estipulado : {umbral_estipulado} °C")
    
    # Se accede al primer índice de la tupla para mostrar la lista de dispositivos que superaron el umbral.
    print(f" Dispositivos que superan umbral  : {tupla_resumen[0]}")
    
    # Se accede al segundo índice de la tupla para mostrar el promedio térmico global.
    print(f" Promedio térmico global          : {tupla_resumen[1]} °C")
    print("-" * 78)
    
    # Se imprime la variable sin desempaquetar para evidenciar la tupla entre paréntesis y su tipo de dato.
    print(" Tupla final (lista_sensores_alerta, promedio_temperatura):")
    print(f" -> {tupla_resumen}")
    print(f" -> Tipo de dato retornado: {type(tupla_resumen)}")
    print("=" * 78)