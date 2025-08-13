# Mi Primera API FastAPI - Bootcamp

**👤 Desarrollador**: David Esteban Bernal Rodriguez
**📧 Email**: esteban.b.200805@gmail.com
**� Privacidad**: Email configurado según mejores prácticas de GitHub
**�📅 Fecha de creación**: 2025-08-02 16:24:13
**📂 Ruta del proyecto**: /c/Users/Aprendiz/fastapi_david_bernal
**💻 Equipo de trabajo**: BOGDFPCGMP5677

## 🔧 Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: `venv-personal/`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## 🚀 Instalación y Ejecución

```bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

## 📝 Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## 🛠️ Troubleshooting Personal

- Si el entorno virtual no se activa: `rm -rf venv-personal && python3 -m venv venv-personal`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar `git config user.name` y `git config user.email`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails

## aprendizajes adquiridos 

- Aprendí sobre el uso de los typehints para la declaracion del tipo de datos de la variable 
- Aprendí sobre como hacer un readme desde la interfaz de gitbash
- Aprendí sobre como hacer documentacion automatica con fastapi y uvicorn 

## aprendizajes adquiridos 2
- Esta semana aprendí a usar Pydantic para que la API valide los datos automáticamente, y eso hace que todo sea más seguro y menos propenso a errores. También puse type hints en las funciones, lo que me ayudó a entender mejor el código, y hice endpoints con parámetros que permiten buscar y filtrar información.

- Me di cuenta de que usar Pydantic y type hints hace que el código sea más ordenado y fácil de cambiar después. Además, agregar parámetros en las rutas y en las consultas hace que la API sea más flexible y profesional, algo que no sabía antes.

- mLo que más me gustó fue aprender a validar datos con Pydantic, porque así evito que la API reciba cosas raras o mal escritas. También hice endpoints que dejan buscar productos con filtros, lo que hace que la API sea más práctica y fácil de usar.
