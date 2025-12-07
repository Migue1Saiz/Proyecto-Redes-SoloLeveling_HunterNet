# 🛡️ HunterNet: Infraestructura de la Asociación Internacional de Cazadores (IHA)

> **Proyecto de Redes - Solo Leveling**
> Diseño e implementación de una red global interconectada, segura y redundante para la gestión de portales y Dungeons.

## 📖 Descripción del Proyecto

Este repositorio contiene el diseño y la implementación de la infraestructura de red para la **Asociación Internacional de Cazadores (IHA)**. El objetivo principal es solucionar la desorganización actual de la red y garantizar la comunicación crítica entre las sedes mundiales ante amenazas como la Crisis de la Isla Jeju.

La red sigue un **modelo jerárquico (Core, Distribución, Acceso)** y asegura redundancia, seguridad y segmentación de tráfico mediante VLANs.

---

## 👥 Equipo y Asignación de Roles

| Miembro | Rol / Sede Asignada | Responsabilidades Clave |
| :--- | :--- | :--- |
| **Miguel Saiz** | **Seúl (Core Global)** | Centro de Operaciones, Enrutamiento Central, HSRP, Automatización con Python. |
| **Mario** | **Isla Jeju** | Zona de Contención, Túneles de seguridad, Monitorización de Crisis. |
| *Por asignar* | Tokio | Centro de Investigación Mágica. |
| *Por asignar* | Washington D.C. | Centro de Control Norteamericano. |
| *Por asignar* | París | Oficina Regional Europea. |

---

## 🏗️ Estructura del Repositorio

El proyecto está organizado por sedes regionales. A continuación se detalla la estructura actual, destacando el desarrollo del Core en Seúl:

```text
PROYECTO-REDES-SOLO_LEVELING/
│
├── Seoul/                      # Sede Central (Core Layer)
│   ├── Configuration/          # Archivos de comandos de configuración de los switches multicapa
│   ├── Command_generator.py    # Script de automatización para generar comandos de Cisco
│   ├── main.pkt                # Topología principal en Cisco Packet Tracer
│   └── README.md               # Documentación específica de la sede
│
├── Jeju/                       # Sede de Contención (En desarrollo)
│   └── ...
│
└── [Otras Sedes]/              # Washington, Tokio, París (Pendientes)