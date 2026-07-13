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
- **Reportes JSON y HTML** con Chart.js
- **CLI Click** con comandos intuitivos

## Aviso Legal

Esta herramienta se proporciona únicamente con fines educativos y para análisis forense autorizado. El usuario asume toda la responsabilidad de garantizar que cuenta con la autorización adecuada.

## Requisitos

- Python 3.11+

```bash
git clone https://github.com/Shadow-King-Cyber/ForensicKit.git
cd ForensicKit
pip install -r requirements.txt
```

## Inicio Rápido

```bash
# Crear imagen forense
forensic-kit image --source /dev/sda1 --output evidence.dd

# Extraer metadata
forensic-kit metadata --path archivo.jpg

# Calcular hashes
forensic-kit hashes --path archivo.bin

# Construir timeline
forensic-kit timeline --path /var/log --depth 2

# Detectar esteganografía
forensic-kit stego --path imagen.png

# Buscar archivos eliminados
forensic-kit recover --file imagen.disco

# Generar reporte
forensic-kit report --format html
```

## Estructura

```
ForensicKit/
├── forensic_kit/
│   ├── core/           # ScopeManager, AuditLogger, EvidenceChain
│   ├── collection/     # DiskImager, LogCollector, NetworkCollector
│   ├── analysis/       # MetadataExtractor, TimelineBuilder, StegoDetector, etc.
│   ├── reporting/      # Reportes JSON/HTML
│   └── ui/             # CLI Click
└── tests/              # Tests en español (~30+)
```

## Licencia

MIT License — Shadow-King-Cyber
