# Trabajo final de programación con Python - EcoTech Solutions

Repositorio correspondiente a la entrega del trabajo final integrador. El proyecto se encuentra organizado en tres carpetas independientes, abarcando sanitización y análisis estadístico de datos, programación orientada a objetos con manejo de excepciones y persistencia en JSON, y auditoría mediante pruebas unitarias (`unittest`) integrada en una aplicación web con Django bajo el patrón Modelo-Vista-Plantilla (MVT).

---

## Estructura del repositorio

```text
ecotech/
├── README.md                            # Documentación e instrucciones de ejecución
├── requirements.txt                     # Dependencias externas del proyecto (Django)
├── .gitignore                           # Archivos excluidos del control de versiones
│
├── ejercicio_1_sensores/                # Carpeta 1: Sanitización y análisis estadístico
│   └── analisis_sensores.py
│
├── ejercicio_2_inventario/              # Carpeta 2: POO, excepciones y persistencia JSON
│   ├── modelo_catalogo.py
│   └── catalogo_ecotech.json
│
└── ejercicio_3_sustentabilidad/         # Carpeta 3: Proyecto Django completo y tests unitarios
    ├── manage.py
    ├── auditoria_y_metricas.py
    ├── ecotech_project/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── sustentabilidad/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── services.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        └── templates/
            └── sustentabilidad/
                └── panel.html
```

---

## Requisitos previos e instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/ecotech.git
   cd ecotech
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   * En Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * En Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Instrucciones de ejecución por ejercicio

### Ejercicio 1: Sanitización y análisis estadístico de sensores
Normaliza lecturas térmicas crudas mediante `limpiar_registro_sensor(registro_raw)` y genera el reporte estadístico global y de alertas con `generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura)`.

* **Comando de ejecución:**
  ```bash
  python ejercicio_1_sensores/analisis_sensores.py
  ```

### Ejercicio 2: Modelo de productos, excepciones y persistencia
Implementa la clase base `DispositivoEcológico` con encapsulamiento de stock, la excepción personalizada `StockInvalidoError`, la subclase `PanelSolar` con polimorfismo en su ficha técnica y la clase `GestorInventario` para exportar el catálogo válido al archivo `catalogo_ecotech.json`.

* **Comando de ejecución:**
  ```bash
  cd ejercicio_2_inventario
  python modelo_catalogo.py
  cd ..
  ```

### Ejercicio 3: Auditoría con tests unitarios e integración web (Django)
Audita la función `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)` con `TestCalculoEmisiones(unittest.TestCase)`, procesa el historial industrial con `obtener_metricas_consumo(registros)` y renderiza los resultados mediante `vista_panel_sustentabilidad(request)` en la plantilla `sustentabilidad/panel.html`.

Primero, ingresa a la carpeta del tercer ejercicio:
```bash
cd ejercicio_3_sustentabilidad
```

* **Ejecutar demostración en consola:**
  ```bash
  python auditoria_y_metricas.py
  ```
* **Ejecutar suite de pruebas unitarias de Django:**
  ```bash
  python manage.py test
  ```
* **Iniciar servidor web local:**
  ```bash
  python manage.py runserver
  ```
  Luego abre en tu navegador `http://127.0.0.1:8000/`.
