# Se importa el módulo nativo para trabajar con archivos en formato de texto estructurado.
import json


# Se define la excepción personalizada heredando de la clase base de excepciones del lenguaje.
class StockInvalidoError(Exception):
    """
    Excepción que se lanza cuando se intenta asignar una cantidad negativa al inventario.
    """
    def __init__(self, stock_intentado, id_producto="desconocido"):
        self.stock_intentado = stock_intentado
        self.mensaje = (
            f"El producto '{id_producto}' no admite un stock negativo ({stock_intentado} unidades)."
        )
        super().__init__(self.mensaje)


# Se diseña la clase base que representa cualquier producto sustentable del catálogo.
class DispositivoEcológico:
    """
    Clase base que encapsula el estado del inventario y los datos generales del dispositivo.
    """
    def __init__(self, id_producto, nombre, marca, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.marca = marca
        self.stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, nuevo_valor):
        if nuevo_valor < 0:
            raise StockInvalidoError(nuevo_valor, self.id_producto)
        self._stock = nuevo_valor

    def emitir_ficha_tecnica(self):
        return (
            f"Ficha comercial -> Código: {self.id_producto} | "
            f"Dispositivo: {self.nombre} ({self.marca}) | "
            f"Unidades en stock: {self.stock}"
        )

    def a_diccionario(self):
        return {
            "tipo_dispositivo": "DispositivoEcológico",
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "marca": self.marca,
            "stock": self.stock,
            "ficha_tecnica": self.emitir_ficha_tecnica()
        }


# Se desarrolla la clase especializada que hereda el comportamiento de la clase base.
class PanelSolar(DispositivoEcológico):
    """
    Subclase que representa un panel fotovoltaico con atributos técnicos específicos.
    """
    def __init__(self, id_producto, nombre, marca, stock, potencia_watts, eficiencia_porcentaje):
        super().__init__(id_producto, nombre, marca, stock)
        self.potencia_watts = potencia_watts
        self.eficiencia_porcentaje = eficiencia_porcentaje

    def emitir_ficha_tecnica(self):
        return (
            f"Ficha comercial solar -> Código: {self.id_producto} | "
            f"Panel: {self.nombre} ({self.marca}) | "
            f"Potencia: {self.potencia_watts} w | "
            f"Eficiencia: {self.eficiencia_porcentaje}% | "
            f"Unidades en stock: {self.stock}"
        )

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "tipo_dispositivo": "PanelSolar",
            "potencia_watts": self.potencia_watts,
            "eficiencia_porcentaje": self.eficiencia_porcentaje,
            "ficha_tecnica": self.emitir_ficha_tecnica()
        })
        return datos


# Se implementa la clase responsable de la persistencia y gestión del catálogo en disco.
class GestorInventario:
    """
    Componente encargado de serializar y almacenar los dispositivos válidos en un archivo.
    """
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        catalogo_serializable = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo_json:
            json.dump(catalogo_serializable, archivo_json, indent=4, ensure_ascii=False)
        return catalogo_serializable


if __name__ == "__main__":
    dispositivos_validos = [
        DispositivoEcológico("Disp-01", "Batería de litio recargable", "EcoPower", 12),
        PanelSolar("Sol-101", "Monocristalino hogar", "SunTech", 25, 450, 21.5),
        PanelSolar("Sol-202", "Bifacial alta carga", "SunTech", 8, 650, 23.8)
    ]

    for disp in dispositivos_validos:
        print(disp.emitir_ficha_tecnica())

    try:
        PanelSolar("Sol-999", "Panel experimental", "EcoFail", -5, 300, 18.0)
    except StockInvalidoError as error:
        print(f"Excepción capturada: {error}")

    GestorInventario.guardar_catalogo_json(dispositivos_validos, "catalogo_ecotech.json")
    print("Catálogo exportado correctamente a catalogo_ecotech.json")
