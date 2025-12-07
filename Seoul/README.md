# 🐍 Network Configuration Generator

> **Herramienta de Automatización para HunterNet**
> Este script genera automáticamente las configuraciones de Cisco IOS para la topología Core y de Distribución, ahorrando horas de configuración manual de interfaces y enrutamiento.

## 📋 Descripción

El script `Command_generator.py` automatiza la creación de la infraestructura de red masiva necesaria para el proyecto. Genera ficheros de texto plano con los comandos necesarios para copiar y pegar en los routers de Packet Tracer.

### Funcionalidades principales:
1.  **Cableado Full-Mesh:** Genera las configuraciones de interfaces e IPs para conectar los 9 Routers del Core con los 3 Routers de cada Sede (Tokyo, Jeju, Seoul, Paris, Washington).
2.  **Direccionamiento IP Dinámico:** Calcula automáticamente subredes `/30` (máscara `255.255.255.252`) para todos los enlaces WAN (`10.0.x.y`).
3.  **Configuración HSRP:** Implementa automáticamente la redundancia de puerta de enlace en los routers de las sedes (Prioridades, Preempt, VIP).
4.  **Configuración de VLANs y Trunks:** Configura los puertos hacia los switches de distribución y acceso.

---

## ⚙️ Requisitos Previos

⚠️ **IMPORTANTE:** Antes de ejecutar el script, asegúrate de que la estructura de carpetas existe. El script intenta guardar los archivos en una ruta específica.

1. Debes tener **Python 3** instalado.
2. Crea la siguiente estructura de carpetas en este directorio si no existe:

```text
.
├── Command_generator.py
└── connections/
    └── generated/      <-- ¡Esta carpeta debe existir!