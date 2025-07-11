# 🚀 ASIA WOK API REST

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

API REST para Asia Wok, esta API servira como punto central para todo el ecosistema Asia Wok.

## ✨ Características Principales

- Control Completo de Registros
- Autenticación JWT
- Validación de datos con Pydantic
- Documentación automática con Swagger y ReDoc

## 📦 Requisitos Previos

- Python 3.10+
- PostgreSQL 14+

## 🛠️ Instalación

### Entorno Virtual (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/steukchen/Backend-sistema-asia-wok.git

# Crear entorno virtual (Unix/macOS)
python3 -m venv venv
source venv/bin/activate

# Crear entorno virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 🚀 Despliegue

- Crear .env y colocar las variables de entorno.

    ```env
    DATABASE_URL=postgresql://user:password@localhost/db_name
    ALGORITHM = "HS256"
    SECRET_KEY = "SECRET_KEY"
    ```

- Ejecutar

    ```bash
    python -m app.test.create_data
    ```

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
    ```
