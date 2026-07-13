# ForensicKit

Herramienta de análisis forense digital para evidencia autorizada — recolección, análisis, timeline y reportes.

> **ADVERTENCIA**: Esta herramienta es **únicamente para análisis forense autorizado**. El análisis de evidencia digital sin autorización es ilegal.

## Características

- **Imágenes forenses** con verificación MD5/SHA256/SHA512
- **Extracción de metadata** de archivos (JPEG, PDF, ELF, ZIP, etc.)
- **Timeline forense** a partir de timestamps de archivos
- **Recolección de logs** del sistema
- **Recolección de estado de red** (interfaces, conexiones, ARP)
- **Detección de esteganografía** (LSB, entropía alta, datos trailing)
- **Recuperación de archivos** eliminados por magic bytes
- **Cadena de custodia** completa con registro de manipulación
- **Verificación de integridad** con múltiples algoritmos hash
- **Reportes JSON y HTML** con visualizaciones
- **CLI Click** con comandos intuitivos

## Aviso Legal

Esta herramienta se proporciona únicamente con fines educativos y para análisis forense autorizado. El usuario asume toda la responsabilidad de garantizar que cuenta con la autorización adecuada.

**Al usar este software, aceptas que:**
- Solo lo usarás con fines de aprendizaje o en investigaciones forenses autorizadas
- No manipularás evidencia sin la cadena de custodia adecuada
- Los autores no asumen responsabilidad por uso indebido

Leyes aplicables (incluyendo pero no limitándose a):
- **Panamá**: Ley 51 de 2012 — Delitos Informáticos
- **USA**: Computer Fraud and Abuse Act (CFAA)
- **UE**: Directive on Attacks against Information Systems (2013/40/EU)

## Requisitos

- Python 3.11+

```bash
git clone https://github.com/Shadow-King-Cyber/ForensicKit.git
cd ForensicKit
pip install -r requirements.txt
```

## Inicio Rápido

```bash
# Crear imagen forense con verificación hash
forensic-kit image --source /dev/sda1 --output evidence.dd

# Extraer metadata de un archivo
forensic-kit metadata --path archivo.jpg

# Calcular hashes de un archivo
forensic-kit hashes --path archivo.bin

# Construir timeline forense
forensic-kit timeline --path /var/log --depth 2

# Detectar esteganografía
forensic-kit stego --path imagen.png

# Buscar archivos eliminados en imagen de disco
forensic-kit recover --file imagen.disco

# Generar reporte forense
forensic-kit report --format html --output reporte
```

## Comandos del CLI

```bash
# Crear imagen forense
forensic-kit image --source /dev/sda1 --output evidence.dd

# Extraer metadata
forensic-kit metadata --path archivo.jpg

# Calcular hashes
forensic-kit hashes --path archivo.bin

# Construir timeline
forensic-kit timeline --path /var/log --depth 3

# Detectar esteganografía
forensic-kit stego --path imagen.png

# Recuperar archivos eliminados
forensic-kit recover --file imagen.disco

# Generar reporte
forensic-kit report --format both --output reporte
```

## Estructura del Proyecto

```
ForensicKit/
├── forensic_kit/
│   ├── core/           # ScopeManager, AuditLogger, EvidenceChain
│   ├── collection/     # DiskImager, LogCollector, NetworkCollector
│   ├── analysis/       # MetadataExtractor, TimelineBuilder, StegoDetector, FileRecovery
│   ├── reporting/      # Reportes JSON/HTML
│   └── ui/             # CLI Click
├── tests/              # Suite de tests con pytest
├── requirements.txt    # Dependencias de Python
├── pyproject.toml      # Configuración del proyecto
└── LICENSE             # Licencia MIT
```

## Ejecutar Tests

```bash
pytest -v
```

## Licencia

MIT License — ver [LICENSE](LICENSE)
