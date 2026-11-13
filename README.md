# QRManager - Sistema de Gestión y Generación de Códigos QR

Aplicación web monolítica en capas desarrollada para la materia de Taller de Programación.

## Tecnologías
- Python 3.11+
- NiceGUI
- SQLModel & SQLite
- Docker

## Instalación
```bash
pip install -r requirements.txt
python -m app.main
```

## Docker
```bash
docker build -t qrmanager-app .
docker run -d -p 8080:8080 qrmanager-app
```