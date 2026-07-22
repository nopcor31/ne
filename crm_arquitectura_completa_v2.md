# CRM Operativo — Sistema Integral de Gestión de Servicios Médicos NE
## Documento de Arquitectura v2.0

**Rol:** Tech Lead / Arquitecto Senior  
**Fecha:** Junio 2026  
**Alcance:** Arquitectura completa, modelo de datos, wireframes, diagrama de entidades, flujo de estados.  
**Estado:** Diseño — sin código de implementación.

---

## ÍNDICE

1. [Visión del Sistema](#1-visión-del-sistema)
2. [Arquitectura de Capas](#2-arquitectura-de-capas)
3. [Estructura de Carpetas](#3-estructura-de-carpetas)
4. [Inventario de Módulos](#4-inventario-de-módulos)
5. [Modelo de Datos Completo](#5-modelo-de-datos-completo)
6. [Diagrama de Entidades (ER)](#6-diagrama-de-entidades-er)
7. [Flujo de Estados](#7-flujo-de-estados)
8. [Motor de Reglas de Negocio](#8-motor-de-reglas-de-negocio)
9. [Sistema de Alertas](#9-sistema-de-alertas)
10. [Wireframes — Pantallas Principales](#10-wireframes--pantallas-principales)
11. [Design System y Tokens Visuales](#11-design-system-y-tokens-visuales)
12. [Integraciones Externas](#12-integraciones-externas)
13. [Trazabilidad Transversal](#13-trazabilidad-transversal)
14. [Estrategia de Implementación](#14-estrategia-de-implementación)
15. [Decisiones Abiertas](#15-decisiones-abiertas)

---

## 1. Visión del Sistema

### 1.1 Qué es este sistema

Un **CRM operativo de ciclo completo** para una empresa de servicios médicos y ambulatorios. No es un cotizador — es la columna vertebral digital de la operación: gestión de clientes, pipeline comercial, cotizaciones con múltiples eventos, aprobaciones médicas, programación de servicios, control de órdenes de compra, facturación y cierre financiero.

### 1.2 Diferencia crítica respecto a un cotizador simple

| Cotizador básico | CRM Operativo (este sistema) |
|---|---|
| Genera documentos de precio | Gestiona toda la relación con el cliente |
| Hoja de cálculo glorificada | Pipeline comercial con Kanban y estados |
| Sin historial de interacciones | Timeline completa de cada cliente |
| Sin alertas ni tareas | Sistema proactivo de alertas y recordatorios |
| Sin integración de agenda | Programación integrada con Outlook Calendar |
| Estado manual | Máquina de estados automática con trazabilidad |

### 1.3 Usuarios del sistema

| Perfil | Responsabilidades principales en el sistema |
|---|---|
| Ejecutivo Comercial | Clientes, cotizaciones, envío a cliente, seguimiento |
| Coordinador Médico | Aprobación de área médica, programación de servicios |
| Administrativo | OC, facturación, cierre de expedientes |
| Gerencia | Dashboard, KPIs, reportes |

> La versión 1.0 opera con usuario único local. La arquitectura está preparada para multiusuario desde el modelo de datos.

### 1.4 Flujo macro del negocio

```
PROSPECTO → CLIENTE → COTIZACIÓN → APROBACIÓN CLIENTE
         → APROBACIÓN ÁREA MÉDICA → PROGRAMACIÓN DEL SERVICIO
         → ORDEN DE COMPRA → FACTURACIÓN → PAGO → CIERRE
```

---

## 2. Arquitectura de Capas

### 2.1 Patrón general

```
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE PRESENTACIÓN                       │
│          PySide6 Widgets  |  QSS Theming  |  Controllers        │
└──────────────────────────┬──────────────────────────────────────┘
                           │  señales Qt / llamadas directas
┌──────────────────────────▼──────────────────────────────────────┐
│                     CAPA DE ORQUESTACIÓN                        │
│                        Controllers                              │
│         (traducen eventos UI en llamadas a servicios)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │  DTOs (dataclasses)
┌──────────────────────────▼──────────────────────────────────────┐
│                    CAPA DE NEGOCIO (Services)                   │
│                                                                 │
│  CRMService  │  CotizacionService  │  TarifaService             │
│  CalendarioService │ EstadoService │ PDFService                 │
│  AlertaService  │  OutlookEmailSvc │ OutlookCalendarSvc         │
│  FacturacionService │ DashboardService │ HistorialService        │
└──────────────────────────┬──────────────────────────────────────┘
                           │  modelos / criterios de búsqueda
┌──────────────────────────▼──────────────────────────────────────┐
│                  CAPA DE DATOS (Repositories)                   │
│                                                                 │
│  BaseRepository<T>  →  ClienteRepository                        │
│                     →  CotizacionRepository                     │
│                     →  EventoRepository                         │
│                     →  TarifaRepository                         │
│                     →  AlertaRepository                         │
│                     →  HistorialRepository     … etc            │
└──────────────────────────┬──────────────────────────────────────┘
                           │  SQLAlchemy ORM
┌──────────────────────────▼──────────────────────────────────────┐
│                       BASE DE DATOS                             │
│                     SQLite  (SQLAlchemy 2.x + Alembic)          │
└─────────────────────────────────────────────────────────────────┘

Servicios transversales (inyectados en todas las capas):
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │HistorialSvc  │   │  AlertaSvc   │   │ LoggingSvc   │
  └──────────────┘   └──────────────┘   └──────────────┘
```

### 2.2 Principios

| Principio | Aplicación concreta |
|---|---|
| **Separación de responsabilidades** | La UI no conoce SQLAlchemy. Los servicios no conocen Qt. |
| **Reglas de negocio aisladas** | `TarifaService`, `CalendarioService`, `EstadoService` son testeables sin levantar Qt. |
| **Trazabilidad estructural** | El decorador `@registrar_historial` es transversal — no se puede "olvidar". |
| **Alertas como ciudadanos de primera clase** | `AlertaService` corre en hilo de fondo y emite señales Qt cuando hay algo urgente. |
| **Preparado para el futuro** | Repository Pattern permite cambiar SQLite por PostgreSQL sin tocar servicios. Outlook COM puede reemplazarse por Microsoft Graph API sin refactorizar nada de la lógica. |

### 2.3 Patrones de diseño aplicados

| Patrón | Dónde | Por qué |
|---|---|---|
| Repository | `repositories/` | Desacopla persistencia de negocio |
| Service Layer | `services/` | Concentra reglas de negocio, evita lógica dispersa en Controllers |
| Strategy | `TarifaService` | Tarifa general vs. tarifa especial por cliente, intercambiable sin `if` sueltos |
| State Machine | `EstadoService` | Las 14 transiciones de estado están encapsuladas, no dispersas en la UI |
| Observer / Decorator | `@registrar_historial` | Trazabilidad automática sin burocracia manual |
| DTO | `dataclasses` en `services/dto/` | Los modelos ORM no salen de la capa de datos |
| Singleton | `SessionManager`, `ConfigService` | Una sola sesión SQLAlchemy, una sola configuración cargada |
| Background Worker | `QThread` para alertas | El chequeo periódico de alertas no bloquea la UI |

---

## 3. Estructura de Carpetas

```
ne_crm/
│
├── main.py                          # Punto de entrada — QApplication + MainWindow
├── requirements.txt
├── alembic.ini
│
├── config/
│   ├── settings.py                  # Rutas, constantes, timeouts
│   └── logging_config.py            # Rotación diaria, niveles por módulo
│
├── core/
│   ├── database.py                  # Engine, SessionLocal, Base declarativa
│   ├── exceptions.py                # TarifaNoEncontradaError, TransicionInvalidaError, etc.
│   ├── enums.py                     # Todos los enum del dominio (ver §5)
│   └── session_manager.py           # Singleton de sesión SQLAlchemy
│
├── models/                          # Entidades SQLAlchemy — solo estructura, sin lógica
│   ├── usuario.py
│   ├── cliente.py
│   ├── contacto_cliente.py
│   ├── interaccion_crm.py           # Llamadas, reuniones, emails registrados en el CRM
│   ├── tarea.py                     # Tareas y recordatorios vinculados a cliente/cotización
│   ├── ciudad.py
│   ├── servicio.py
│   ├── tarifa.py
│   ├── festivo.py
│   ├── cotizacion.py
│   ├── evento.py
│   ├── extra_evento.py
│   ├── area_medica.py
│   ├── envio_area_medica.py
│   ├── programacion.py
│   ├── orden_compra.py
│   ├── factura.py
│   ├── alerta.py
│   ├── historial_actividad.py
│   └── configuracion.py
│
├── repositories/
│   ├── base_repository.py           # CRUD genérico: get, get_all, create, update, delete
│   ├── cliente_repository.py
│   ├── contacto_repository.py
│   ├── interaccion_repository.py
│   ├── tarea_repository.py
│   ├── tarifa_repository.py
│   ├── cotizacion_repository.py
│   ├── evento_repository.py
│   ├── area_medica_repository.py
│   ├── envio_area_medica_repository.py
│   ├── programacion_repository.py
│   ├── orden_compra_repository.py
│   ├── factura_repository.py
│   ├── alerta_repository.py
│   └── historial_repository.py
│
├── services/
│   ├── dto/                         # Data Transfer Objects (dataclasses)
│   │   ├── cliente_dto.py
│   │   ├── cotizacion_dto.py
│   │   ├── evento_dto.py
│   │   ├── tarifa_dto.py
│   │   └── dashboard_dto.py
│   ├── crm_service.py               # Interacciones, tareas, contactos por cliente
│   ├── cliente_service.py
│   ├── tarifa_service.py            # Motor de tarifas (Strategy + fallback)
│   ├── calendario_service.py        # Horas diurnas/nocturnas, tipo de día, festivos
│   ├── cotizacion_service.py        # CRUD + totales + duplicado de evento
│   ├── evento_service.py            # Cálculo automático al guardar evento
│   ├── estado_service.py            # CotizacionStateMachine — transiciones válidas
│   ├── pdf_service.py               # ReportLab — generación de PDF de cotización
│   ├── outlook_email_service.py     # Envío de correo vía Outlook COM
│   ├── outlook_calendar_service.py  # Creación de eventos en Outlook Calendar
│   ├── area_medica_service.py
│   ├── programacion_service.py
│   ├── orden_compra_service.py
│   ├── facturacion_service.py
│   ├── alerta_service.py            # Genera, evalúa y emite alertas (QThread)
│   ├── dashboard_service.py         # Agrega KPIs y métricas
│   └── historial_service.py         # Registro transversal de actividad
│
├── controllers/
│   ├── dashboard_controller.py
│   ├── crm_controller.py
│   ├── cliente_controller.py
│   ├── tarifa_controller.py
│   ├── cotizacion_controller.py
│   ├── evento_controller.py
│   ├── programacion_controller.py
│   ├── area_medica_controller.py
│   ├── oc_controller.py
│   ├── facturacion_controller.py
│   ├── alerta_controller.py
│   ├── historial_controller.py
│   └── configuracion_controller.py
│
├── views/
│   ├── main_window.py               # Shell: sidebar + topbar + stacked widget
│   │
│   ├── components/                  # Design system — widgets reutilizables
│   │   ├── sidebar.py               # Nav lateral colapsable
│   │   ├── topbar.py                # Búsqueda global + campanita de alertas + usuario
│   │   ├── kpi_card.py              # Tarjeta KPI con ícono, valor y delta
│   │   ├── modern_table.py          # QTableView + sorting + paginación + densidad
│   │   ├── kanban_board.py          # Columnas drag-and-drop por estado
│   │   ├── kanban_card.py           # Tarjeta individual del Kanban
│   │   ├── timeline_widget.py       # Feed de actividad (Dashboard + Historial + Cliente)
│   │   ├── state_badge.py           # Pill de color según estado
│   │   ├── filter_bar.py            # Chips de filtro activos + buscador inline
│   │   ├── drawer_panel.py          # Panel lateral deslizante (detalle sin abrir modal)
│   │   ├── alert_bell.py            # Ícono con contador de alertas + dropdown
│   │   ├── empty_state.py           # Ilustración + CTA cuando no hay datos
│   │   ├── confirm_dialog.py        # Modal de confirmación reutilizable
│   │   └── progress_steps.py        # Indicador visual del estado del pipeline
│   │
│   ├── dashboard/
│   │   └── dashboard_view.py
│   ├── clientes/
│   │   ├── clientes_view.py         # Tabla/lista de clientes
│   │   ├── cliente_detail_view.py   # Detalle CRM: info + contactos + interacciones + tareas
│   │   └── cliente_form.py
│   ├── tarifas/
│   │   ├── tarifas_view.py
│   │   └── tarifa_form.py
│   ├── cotizaciones/
│   │   ├── cotizaciones_view.py     # Lista + Kanban
│   │   ├── cotizacion_detail_view.py
│   │   └── evento_form.py
│   ├── programacion/
│   │   └── programacion_view.py     # Vista calendario mensual/semanal
│   ├── areas_medicas/
│   │   └── areas_medicas_view.py
│   ├── ordenes_compra/
│   │   └── oc_view.py
│   ├── facturacion/
│   │   └── facturacion_view.py
│   ├── alertas/
│   │   └── alertas_view.py
│   ├── historial/
│   │   └── historial_view.py
│   └── configuracion/
│       └── configuracion_view.py
│
├── workers/
│   └── alerta_worker.py             # QThread — evalúa alertas en background cada N min
│
├── resources/
│   ├── styles/
│   │   ├── tokens.qss               # Variables del design system
│   │   └── main.qss                 # Hoja de estilo global
│   ├── icons/                       # SVG — set completo de iconografía
│   ├── fonts/                       # Inter / Segoe UI Variable
│   └── pdf_templates/
│       └── cotizacion_layout.py     # Clase ReportLab para PDF de cotización
│
├── utils/
│   ├── formatters.py                # COP, fechas, duraciones, plurales
│   ├── validators.py
│   ├── numero_generador.py          # COT-AAAA-NNNN
│   └── decorators.py                # @registrar_historial, @requiere_estado
│
├── migrations/                      # Alembic
│   └── versions/
│
├── data/
│   └── ne_crm.db
│
├── logs/
│   └── crm.log
│
└── tests/
    ├── unit/
    │   ├── test_calendario_service.py
    │   ├── test_tarifa_service.py
    │   ├── test_estado_service.py
    │   └── test_alerta_service.py
    └── integration/
        └── test_cotizacion_workflow.py
```

---

## 4. Inventario de Módulos

| # | Módulo | Propósito | Componentes clave |
|---|---|---|---|
| 1 | **Dashboard** | Centro de mando — KPIs y actividad reciente | KPI cards, mini-Kanban, timeline, alertas activas |
| 2 | **Clientes (CRM)** | Gestión de la relación completa con el cliente | Ficha cliente, múltiples contactos, interacciones, tareas, historial, cotizaciones relacionadas |
| 3 | **Tarifas** | Catálogo de precios general y por cliente especial | Tabla de tarifas con versionado, carga masiva por CSV |
| 4 | **Cotizaciones** | Pipeline comercial — Lista y Kanban | Eventos múltiples, cálculo automático, PDF, envío por Outlook |
| 5 | **Programación** | Agenda operativa de servicios aprobados | Vista calendario, integración Outlook Calendar |
| 6 | **Áreas Médicas** | Flujo de aprobación interna | Catálogo de áreas, registro de envíos y respuestas |
| 7 | **Órdenes de Compra** | Control de OC del cliente | Seguimiento de solicitud y recepción |
| 8 | **Facturación** | Cierre financiero | Control de emisión y pago de facturas |
| 9 | **Alertas** | Sistema proactivo de avisos | Alerta por vencimiento, sin respuesta, OC demorada |
| 10 | **Historial** | Bitácora global de toda acción | Timeline filtrable por entidad, usuario, fecha |
| 11 | **Configuración** | Parámetros del sistema | Catálogos, datos empresa, cuenta Outlook, festivos |

---

## 5. Modelo de Datos Completo

### 5.1 Enums del dominio

```python
# core/enums.py

class TipoCliente(enum):
    NORMAL    = "NORMAL"
    ESPECIAL  = "ESPECIAL"

class TipoDia(enum):
    ORDINARIO = "ORDINARIO"   # Lunes a Sábado no festivo
    FESTIVO   = "FESTIVO"     # Domingos y festivos legales

class TipoHorario(enum):
    DIURNO   = "DIURNO"      # 07:00 – 18:59
    NOCTURNO = "NOCTURNO"    # 19:00 – 06:59

class TipoServicio(enum):
    AMBULANCIA_TAB     = "AMBULANCIA_TAB"
    AMBULANCIA_TAM     = "AMBULANCIA_TAM"
    AUXILIAR_ENFERMERIA = "AUXILIAR_ENFERMERIA"
    PARAMEDICO         = "PARAMEDICO"
    CONDUCTOR_TAB      = "CONDUCTOR_TAB"
    CONDUCTOR_TAM      = "CONDUCTOR_TAM"
    MEDICO_GENERAL     = "MEDICO_GENERAL"

class TipoExtra(enum):
    PEAJE        = "PEAJE"
    ALIMENTACION = "ALIMENTACION"
    TRANSPORTE   = "TRANSPORTE"
    OTROS        = "OTROS"

class EstadoCotizacion(enum):
    BORRADOR              = "BORRADOR"
    COTIZADA              = "COTIZADA"
    ENVIADA_CLIENTE       = "ENVIADA_CLIENTE"
    ACEPTADA_CLIENTE      = "ACEPTADA_CLIENTE"
    RECHAZADA_CLIENTE     = "RECHAZADA_CLIENTE"
    PENDIENTE_AREA_MEDICA = "PENDIENTE_AREA_MEDICA"
    APROBADA_AREA_MEDICA  = "APROBADA_AREA_MEDICA"
    PROGRAMADA            = "PROGRAMADA"
    OC_SOLICITADA         = "OC_SOLICITADA"
    OC_RECIBIDA           = "OC_RECIBIDA"
    PENDIENTE_FACTURACION = "PENDIENTE_FACTURACION"
    FACTURADA             = "FACTURADA"
    PAGADA                = "PAGADA"
    CERRADA               = "CERRADA"

class TipoInteraccionCRM(enum):
    LLAMADA   = "LLAMADA"
    REUNION   = "REUNION"
    EMAIL     = "EMAIL"
    NOTA      = "NOTA"
    VISITA    = "VISITA"

class TipoAlerta(enum):
    COTIZACION_SIN_RESPUESTA   = "COTIZACION_SIN_RESPUESTA"
    OC_DEMORADA                = "OC_DEMORADA"
    PAGO_PENDIENTE             = "PAGO_PENDIENTE"
    TAREA_VENCIDA              = "TAREA_VENCIDA"
    AREA_MEDICA_SIN_RESPUESTA  = "TAREA_VENCIDA"
    SERVICIO_HOY               = "SERVICIO_HOY"

class PrioridadTarea(enum):
    BAJA   = "BAJA"
    MEDIA  = "MEDIA"
    ALTA   = "ALTA"
    CRITICA = "CRITICA"

class OrigenFestivo(enum):
    LIBRERIA = "LIBRERIA"
    MANUAL   = "MANUAL"
```

### 5.2 Entidades — definición completa

---

#### `usuario`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| nombre | string(100) | |
| email | string(150), único | |
| activo | bool, default=True | |
| fecha_creacion | datetime | |

---

#### `cliente`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| empresa | string(200) | |
| nit | string(20), único | |
| correo_principal | string(150) | |
| telefono_principal | string(20) | |
| tipo_cliente | enum TipoCliente | Determina si busca tarifa propia |
| sector | string(100), nullable | Sector económico / industria |
| ciudad_id | FK → ciudad | Ciudad principal del cliente |
| direccion | string(300), nullable | |
| sitio_web | string(200), nullable | |
| observaciones | text, nullable | |
| activo | bool, default=True | |
| fecha_creacion | datetime | |
| usuario_creador_id | FK → usuario | |

---

#### `contacto_cliente`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cliente_id | FK → cliente | |
| nombre | string(150) | |
| cargo | string(100), nullable | |
| correo | string(150), nullable | |
| telefono | string(20), nullable | |
| es_principal | bool, default=False | Solo uno puede ser principal por cliente |
| activo | bool, default=True | |

Restricción: un solo `es_principal = True` por `cliente_id`.

---

#### `interaccion_crm`
Registro de cada punto de contacto con el cliente (llamada, reunión, email, visita, nota interna).

| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cliente_id | FK → cliente | |
| cotizacion_id | FK → cotizacion, nullable | Interacción puede o no estar ligada a una cotización |
| tipo | enum TipoInteraccionCRM | |
| fecha_hora | datetime | |
| asunto | string(300) | |
| descripcion | text, nullable | |
| usuario_id | FK → usuario | Quién registró la interacción |

---

#### `tarea`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cliente_id | FK → cliente, nullable | |
| cotizacion_id | FK → cotizacion, nullable | Al menos uno de los dos debe estar presente |
| titulo | string(300) | |
| descripcion | text, nullable | |
| prioridad | enum PrioridadTarea | |
| fecha_vencimiento | datetime | |
| completada | bool, default=False | |
| fecha_completada | datetime, nullable | |
| usuario_asignado_id | FK → usuario | |
| usuario_creador_id | FK → usuario | |

---

#### `ciudad`
| Campo | Tipo |
|---|---|
| id | PK |
| nombre | string(150), único |
| departamento | string(100) |
| activo | bool |

---

#### `servicio`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| codigo | string(30), único | |
| nombre | string(200) | |
| tipo | enum TipoServicio | |
| activo | bool | |

---

#### `tarifa`
La pieza central del motor de precios — **nada se hardcodea**.

| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| ciudad_id | FK → ciudad | |
| servicio_id | FK → servicio | |
| tipo_dia | enum TipoDia | ORDINARIO / FESTIVO |
| tipo_horario | enum TipoHorario | DIURNO / NOCTURNO |
| cliente_id | FK → cliente, **nullable** | NULL = tarifa general; con valor = tarifa exclusiva del cliente |
| valor_hora | decimal(14,2) | |
| vigente_desde | date | Permite versionar cambios de tarifa en el tiempo |
| vigente_hasta | date, nullable | NULL = vigente indefinidamente |
| activo | bool | |

**Restricción UNIQUE:** `(ciudad_id, servicio_id, tipo_dia, tipo_horario, cliente_id, vigente_desde)` — evita tarifas duplicadas activas para la misma combinación.

---

#### `festivo`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| fecha | date, único | |
| nombre | string(200) | |
| origen | enum OrigenFestivo | LIBRERIA (auto) o MANUAL (editado por usuario) |

---

#### `cotizacion`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| numero_cotizacion | string(20), único | Formato: `COT-AAAA-NNNN` |
| cliente_id | FK → cliente | |
| contacto_id | FK → contacto_cliente, nullable | Contacto específico destinatario |
| estado | enum EstadoCotizacion | Gestionado por EstadoService |
| usuario_creador_id | FK → usuario | |
| usuario_asignado_id | FK → usuario, nullable | Para asignación futura |
| fecha_creacion | datetime | |
| fecha_enviada_cliente | datetime, nullable | |
| fecha_respuesta_cliente | datetime, nullable | |
| fecha_enviada_area | datetime, nullable | |
| fecha_aprobacion_area | datetime, nullable | |
| fecha_programacion | datetime, nullable | |
| fecha_oc_solicitada | datetime, nullable | |
| fecha_oc_recibida | datetime, nullable | |
| fecha_facturacion | datetime, nullable | |
| fecha_pago | datetime, nullable | |
| valor_subtotal | decimal(14,2) | Suma de eventos sin extras |
| valor_extras | decimal(14,2) | Suma de todos los extras |
| valor_total | decimal(14,2) | subtotal + extras |
| observaciones | text, nullable | |
| condiciones_comerciales | text, nullable | Se incluye en PDF |
| pdf_path | string(500), nullable | Ruta al último PDF generado |

---

#### `evento`
Cada servicio individual dentro de una cotización.

| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cotizacion_id | FK → cotizacion | |
| servicio_id | FK → servicio | |
| fecha | date | |
| hora_inicio | time | |
| hora_fin | time | |
| ciudad_id | FK → ciudad | |
| direccion | string(400) | |
| contacto | string(150) | |
| telefono | string(20) | |
| observaciones | text, nullable | |
| tipo_dia | enum TipoDia | **Calculado automáticamente** al guardar |
| horas_diurnas | decimal(6,2) | **Calculado automáticamente** |
| horas_nocturnas | decimal(6,2) | **Calculado automáticamente** |
| valor_horas_diurnas | decimal(14,2) | **Calculado** |
| valor_horas_nocturnas | decimal(14,2) | **Calculado** |
| valor_extras | decimal(14,2) | Suma de ExtraEvento |
| valor_evento | decimal(14,2) | Total del evento |
| orden | int | Orden de despliegue en la cotización |

---

#### `extra_evento`
| Campo | Tipo |
|---|---|
| id | PK |
| evento_id | FK → evento |
| tipo | enum TipoExtra |
| descripcion | string(300) |
| valor | decimal(14,2) |

---

#### `area_medica`
| Campo | Tipo |
|---|---|
| id | PK |
| nombre | string(200) |
| correo_contacto | string(150) |
| telefono | string(20), nullable |
| responsable | string(150), nullable |
| activo | bool |

---

#### `envio_area_medica`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cotizacion_id | FK → cotizacion | |
| area_medica_id | FK → area_medica | |
| fecha_envio | datetime | |
| usuario_envio_id | FK → usuario | |
| fecha_respuesta | datetime, nullable | |
| aprobado | bool, nullable | NULL = sin respuesta aún |
| observaciones_respuesta | text, nullable | |

---

#### `programacion`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cotizacion_id | FK → cotizacion | |
| evento_id | FK → evento | |
| fecha_programada | date | |
| hora_inicio | time | |
| hora_fin | time | |
| recurso_asignado | string(200), nullable | Nombre del personal/ambulancia asignado |
| notas | text, nullable | |
| outlook_event_id | string(500), nullable | EntryID del evento de Outlook Calendar |
| estado | enum(PENDIENTE, CONFIRMADA, REALIZADA, CANCELADA) | |

---

#### `orden_compra`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cotizacion_id | FK → cotizacion | |
| numero_oc | string(100), nullable | El número que da el cliente |
| fecha_solicitud | datetime | Cuándo se solicitó al cliente |
| fecha_recibido | datetime, nullable | |
| archivo_path | string(500), nullable | Ruta al PDF de la OC recibida |
| observaciones | text, nullable | |
| estado | enum(SOLICITADA, RECIBIDA) | |

---

#### `factura`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| cotizacion_id | FK → cotizacion | |
| numero_factura | string(100) | |
| fecha_facturacion | date | |
| fecha_vencimiento | date | |
| fecha_pago | date, nullable | |
| valor_facturado | decimal(14,2) | |
| observaciones | text, nullable | |
| estado | enum(PENDIENTE, FACTURADA, PAGADA) | |

---

#### `alerta`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| tipo | enum TipoAlerta | |
| titulo | string(300) | |
| mensaje | text | |
| entidad_tipo | string(50) | "cotizacion", "tarea", "factura" |
| entidad_id | int | ID de la entidad afectada |
| prioridad | enum(INFO, ADVERTENCIA, CRITICA) | |
| fecha_creacion | datetime | |
| fecha_visto | datetime, nullable | NULL = no leída |
| usuario_id | FK → usuario | A quién va dirigida |
| activa | bool, default=True | False = descartada |

---

#### `historial_actividad`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| fecha_hora | datetime | |
| usuario_id | FK → usuario | |
| entidad_tipo | string(50) | "cotizacion", "cliente", "factura", etc. |
| entidad_id | int | |
| accion | string(300) | Texto legible: "Cotización enviada al cliente" |
| detalle | text, nullable | Contexto adicional (ej. correo destinatario) |
| es_automatico | bool | True si lo generó el sistema, False si fue acción del usuario |

---

#### `configuracion`
Clave-valor flexible para parámetros del sistema.

| Campo | Tipo |
|---|---|
| id | PK |
| clave | string(100), único |
| valor | text |
| descripcion | string(300) |

Claves esperadas: `empresa.nombre`, `empresa.nit`, `empresa.direccion`, `empresa.logo_path`, `outlook.cuenta_email`, `pdf.condiciones_generales`, `alertas.dias_sin_respuesta`, `alertas.dias_oc_demorada`.

---

## 6. Diagrama de Entidades (ER)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DIAGRAMA ENTIDAD-RELACIÓN                              │
│                    CRM Operativo — Servicios Médicos NE                      │
└─────────────────────────────────────────────────────────────────────────────┘

USUARIO ──────────────────┬──────────────────────────────────────────────────┐
 id, nombre, email        │ (crea, asigna, registra)                         │
                          │                                                   │
CLIENTE ◄─────────────────┘                  ┌──── TARIFA                    │
 id, empresa, nit         ├──── CONTACTO     │      id                       │
 tipo_cliente             │     CLIENTE      │      ciudad_id ──┐             │
 ciudad_id                │      (1:N)       │      servicio_id  │             │
                          │                  │      tipo_dia     │             │
                          ├──── INTERACCION  │      tipo_horario │             │
                          │     CRM (1:N)    │      cliente_id ──┘ (nullable) │
                          │                  │      valor_hora                │
                          ├──── TAREA (1:N)  │      vigente_desde             │
                          │                  └──── SERVICIO                   │
                          │                         id, nombre               │
                          │                         tipo (enum)              │
                          │                                                   │
                          └──── COTIZACION ──────────────────────────────────┘
                                  id
                                  numero_cotizacion
                                  cliente_id ──────────────────► CLIENTE
                                  contacto_id ─────────────────► CONTACTO_CLIENTE
                                  estado (14 estados)
                                  valor_total
                                  │
                                  ├──── EVENTO (1:N)
                                  │       id
                                  │       servicio_id ──────────► SERVICIO
                                  │       ciudad_id ────────────► CIUDAD
                                  │       fecha, hora_inicio/fin
                                  │       tipo_dia (calculado)
                                  │       horas_diurnas/nocturnas (calculados)
                                  │       valor_evento (calculado)
                                  │       │
                                  │       └──── EXTRA_EVENTO (1:N)
                                  │               tipo, descripcion, valor
                                  │
                                  ├──── ENVIO_AREA_MEDICA (1:N)
                                  │       area_medica_id ────────► AREA_MEDICA
                                  │       fecha_envio, aprobado
                                  │
                                  ├──── PROGRAMACION (1:N)
                                  │       evento_id ───────────► EVENTO
                                  │       recurso_asignado
                                  │       outlook_event_id
                                  │
                                  ├──── ORDEN_COMPRA (1:N)
                                  │       numero_oc, fecha
                                  │       archivo_path
                                  │
                                  ├──── FACTURA (1:N)
                                  │       numero_factura
                                  │       fecha_pago
                                  │       valor_facturado
                                  │
                                  └──── HISTORIAL_ACTIVIDAD (1:N)
                                          accion, detalle
                                          usuario_id ──────────► USUARIO


FESTIVO                    CIUDAD
 id, fecha, nombre          id, nombre, departamento
 origen (LIB/MANUAL)        │
 ▲                          ▼
 └─ usado por CALENDARIO_SERVICE para calcular TipoDia
    y EVENTO al guardar

ALERTA
 tipo, titulo, mensaje
 entidad_tipo, entidad_id ──► (cotizacion | tarea | factura)
 prioridad, activa
 usuario_id ────────────────► USUARIO
```

---

## 7. Flujo de Estados

### 7.1 Diagrama de la máquina de estados

```
                    ┌─────────────────────────────────────────────────────┐
                    │           MÁQUINA DE ESTADOS — COTIZACIÓN           │
                    └─────────────────────────────────────────────────────┘

                              ┌──────────┐
                              │ BORRADOR │◄── Estado inicial al crear
                              └────┬─────┘
                                   │ [Usuario completa cotización]
                                   ▼
                              ┌──────────┐
                              │ COTIZADA │◄── Cálculos validados
                              └────┬─────┘
                                   │ [Botón: Enviar a Cliente → genera PDF + envía email]
                                   ▼
                        ┌──────────────────┐
                        │ ENVIADA_CLIENTE  │◄── Email enviado, fecha registrada
                        └────────┬─────────┘
                  ┌──────────────┤
                  │              │
                  ▼              ▼
         ┌────────────┐   ┌────────────────────┐
         │  RECHAZADA │   │  ACEPTADA_CLIENTE  │
         │  _CLIENTE  │   └─────────┬──────────┘
         └─────┬──────┘             │ [Botón: Enviar a Área Médica]
               │                    ▼
               │        ┌──────────────────────────┐
               │        │ PENDIENTE_ÁREA_MÉDICA    │◄── Email enviado al área
               │        └──────────┬───────────────┘
               │                   │
               │       ┌───────────┤
               │       │           │
               │       ▼           ▼
               │  [Rechazada] [Aprobada]
               │   ◄──────    ┌──────────────────────┐
               │              │  APROBADA_ÁREA_MÉDICA │
               │              └──────────┬────────────┘
               │                         │ [Botón: Programar servicio]
               │                         ▼
               │              ┌─────────────────┐
               │              │   PROGRAMADA    │◄── Evento creado en Outlook
               │              └────────┬────────┘
               │                       │ [Botón: Solicitar OC al cliente]
               │                       ▼
               │              ┌──────────────────┐
               │              │  OC_SOLICITADA   │◄── Email enviado al cliente
               │              └────────┬─────────┘
               │                       │ [Acción: OC recibida + adjuntar archivo]
               │                       ▼
               │              ┌──────────────────┐
               │              │   OC_RECIBIDA    │
               │              └────────┬─────────┘
               │                       │ [Acción: Marcar como pendiente facturación]
               │                       ▼
               │              ┌──────────────────────────┐
               │              │  PENDIENTE_FACTURACIÓN   │
               │              └────────┬─────────────────┘
               │                       │ [Acción: Registrar factura emitida]
               │                       ▼
               │              ┌────────────────┐
               │              │   FACTURADA    │
               │              └────────┬───────┘
               │                       │ [Acción: Registrar pago recibido]
               │                       ▼
               │              ┌────────────────┐
               │              │    PAGADA      │
               │              └────────┬───────┘
               │                       │ [Acción: Cerrar expediente]
               │                       ▼
               └──────────────► ┌─────────────┐
                                │   CERRADA   │ ← Estado terminal
                                └─────────────┘
```

### 7.2 Tabla de transiciones válidas

| Estado actual | Evento / Acción | Estado siguiente | Efectos automáticos |
|---|---|---|---|
| BORRADOR | Validar cotización | COTIZADA | Recalcula totales |
| COTIZADA | Enviar a cliente | ENVIADA_CLIENTE | Genera PDF + Envía email Outlook + registra fecha |
| ENVIADA_CLIENTE | Registrar aceptación | ACEPTADA_CLIENTE | Registra fecha respuesta |
| ENVIADA_CLIENTE | Registrar rechazo | RECHAZADA_CLIENTE | Registra fecha + motivo |
| ACEPTADA_CLIENTE | Enviar a área médica | PENDIENTE_ÁREA_MÉDICA | Envía email al área + registra fecha |
| PENDIENTE_ÁREA_MÉDICA | Registrar aprobación área | APROBADA_ÁREA_MÉDICA | Registra fecha + responsable |
| PENDIENTE_ÁREA_MÉDICA | Registrar rechazo área | RECHAZADA_CLIENTE | Notifica al comercial |
| APROBADA_ÁREA_MÉDICA | Programar servicio | PROGRAMADA | Crea evento en Outlook Calendar |
| PROGRAMADA | Solicitar OC | OC_SOLICITADA | Envía email al cliente + registra fecha |
| OC_SOLICITADA | Registrar OC recibida | OC_RECIBIDA | Adjunta archivo + registra fecha |
| OC_RECIBIDA | Pasar a facturación | PENDIENTE_FACTURACIÓN | Crea registro en módulo Facturación |
| PENDIENTE_FACTURACIÓN | Registrar factura emitida | FACTURADA | Registra número y fecha factura |
| FACTURADA | Registrar pago | PAGADA | Registra fecha de pago |
| PAGADA | Cerrar expediente | CERRADA | Cierre definitivo |

> **Regla de oro:** ningún Controller puede mutar el estado directamente — toda transición pasa por `EstadoService.transicionar(cotizacion_id, nuevo_estado, usuario_id)`. Si la transición no está en la tabla, se lanza `TransicionInvalidaError`.

### 7.3 Acciones permitidas por estado (visible en la UI)

```
BORRADOR             → [Editar] [Completar cotización]
COTIZADA             → [Editar] [Ver PDF] [Enviar a Cliente]
ENVIADA_CLIENTE      → [Ver PDF] [Reenviar] [Registrar Respuesta] [Crear Alerta de Seguimiento]
ACEPTADA_CLIENTE     → [Enviar a Área Médica]
RECHAZADA_CLIENTE    → [Ver] [Duplicar como nuevo borrador]
PENDIENTE_ÁREA       → [Registrar Respuesta Área]
APROBADA_ÁREA        → [Programar Servicio]
PROGRAMADA           → [Ver Programación] [Solicitar OC]
OC_SOLICITADA        → [Registrar OC Recibida]
OC_RECIBIDA          → [Ver OC] [Pasar a Facturación]
PENDIENTE_FACTURACIÓN→ [Registrar Factura]
FACTURADA            → [Registrar Pago]
PAGADA               → [Cerrar Expediente]
CERRADA              → [Solo lectura]
```

---

## 8. Motor de Reglas de Negocio

### 8.1 Cálculo de horas diurnas / nocturnas

**Regla:** DIURNO = 07:00–18:59 | NOCTURNO = 19:00–06:59

```
ALGORITMO calcular_horas(fecha, hora_inicio, hora_fin):

  inicio_dt = datetime(fecha, hora_inicio)
  fin_dt    = datetime(fecha, hora_fin)

  si fin_dt <= inicio_dt:
      fin_dt += timedelta(days=1)   ← el evento cruza medianoche

  horas_diurnas   = Decimal("0.00")
  horas_nocturnas = Decimal("0.00")
  cursor = inicio_dt
  FRONTERA_DIURNA   = time(7, 0)
  FRONTERA_NOCTURNA = time(19, 0)

  mientras cursor < fin_dt:
      siguiente_frontera = calcular_siguiente_frontera(cursor, FRONTERA_DIURNA, FRONTERA_NOCTURNA)
      tramo_fin = min(fin_dt, siguiente_frontera)
      duracion_horas = (tramo_fin - cursor).total_seconds() / 3600

      si es_franja_diurna(cursor):
          horas_diurnas += duracion_horas
      sino:
          horas_nocturnas += duracion_horas

      cursor = tramo_fin

  retornar horas_diurnas, horas_nocturnas

FUNCIÓN es_franja_diurna(dt):
  retornar FRONTERA_DIURNA <= dt.time() < FRONTERA_NOCTURNA
```

**Validación contra ejemplo del requerimiento:**
- Entrada: 14:00 → 20:00
- Tramo 14:00–19:00 → diurno → 5.00 h
- Tramo 19:00–20:00 → nocturno → 1.00 h
- **Resultado: 5h diurnas / 1h nocturna ✓**

### 8.2 Determinación de tipo de día

```
FUNCIÓN tipo_dia(fecha):
  si fecha.weekday() == 6 (DOMINGO):
      retornar FESTIVO
  si FestivoRepository.existe(fecha):
      retornar FESTIVO
  retornar ORDINARIO
```

### 8.3 Motor de tarifas (Strategy Pattern)

```
FUNCIÓN obtener_tarifa(cliente, ciudad_id, servicio_id, tipo_dia, tipo_horario, fecha):

  si cliente.tipo_cliente == ESPECIAL:
      tarifa = TarifaRepository.buscar(
          cliente_id  = cliente.id,
          ciudad_id   = ciudad_id,
          servicio_id = servicio_id,
          tipo_dia    = tipo_dia,
          tipo_horario = tipo_horario,
          vigente_en  = fecha
      )
      si tarifa existe: retornar tarifa

  # Fallback a tarifa general (también aplica a clientes NORMALES)
  tarifa = TarifaRepository.buscar(
      cliente_id  = NULL,
      ciudad_id   = ciudad_id,
      servicio_id = servicio_id,
      tipo_dia    = tipo_dia,
      tipo_horario = tipo_horario,
      vigente_en  = fecha
  )

  si tarifa no existe:
      lanzar TarifaNoEncontradaError(ciudad, servicio, tipo_dia, tipo_horario)

  retornar tarifa
```

### 8.4 Cálculo completo de un evento

```
valor_diurno   = horas_diurnas   × tarifa_diurna.valor_hora
valor_nocturno = horas_nocturnas × tarifa_nocturna.valor_hora
suma_extras    = Σ extra.valor para extra in evento.extras
valor_evento   = valor_diurno + valor_nocturno + suma_extras
```

---

## 9. Sistema de Alertas

Las alertas son **ciudadanas de primera clase** en este CRM — no un módulo de segunda fase.

### 9.1 Tipos de alerta y reglas de disparo

| Tipo | Regla de disparo | Prioridad |
|---|---|---|
| COTIZACION_SIN_RESPUESTA | Cotización en ENVIADA_CLIENTE sin respuesta desde hace N días (configurable) | ADVERTENCIA |
| AREA_MEDICA_SIN_RESPUESTA | En PENDIENTE_ÁREA_MÉDICA sin respuesta hace N días | ADVERTENCIA |
| OC_DEMORADA | En OC_SOLICITADA sin recibir hace N días (configurable) | ADVERTENCIA |
| PAGO_PENDIENTE | Factura emitida con fecha_vencimiento < hoy | CRITICA |
| TAREA_VENCIDA | Tarea con fecha_vencimiento < ahora y no completada | ALTA |
| SERVICIO_HOY | Evento programado para hoy (aviso matutino) | INFO |

### 9.2 Arquitectura del sistema de alertas

Un `AlertaWorker` (subclase de `QThread`) se ejecuta en background y evalúa las reglas periódicamente (cada 5 minutos por defecto). Cuando encuentra una condición:

1. Verifica si ya existe una alerta activa del mismo tipo para la misma entidad (evita duplicados).
2. Si no existe, crea el registro en la tabla `alerta`.
3. Emite una señal Qt al hilo principal → `AlertaBell` actualiza el contador.
4. El usuario ve el badge rojo con el número de alertas no leídas.

```
QApplication (hilo principal)
      │
      ├── MainWindow
      │       └── TopBar
      │               └── AlertaBell (contador visual)
      │                       ▲
      │               señal Qt: alerta_nueva
      │
      └── AlertaWorker (QThread)
              │
              cada 5 min: evalúa reglas
              │
              ├── cotizaciones sin respuesta (ENVIADA_CLIENTE)
              ├── áreas sin respuesta (PENDIENTE_ÁREA_MÉDICA)
              ├── OC demoradas (OC_SOLICITADA)
              ├── facturas vencidas (FACTURADA)
              └── tareas vencidas
```

---

## 10. Wireframes — Pantallas Principales

### 10.1 Layout global de la aplicación

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │  NE Logo    🔍 Buscar clientes, cotizaciones...        🔔3  👤 Admin   │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║  ┌─────────┐  ┌──────────────────────────────────────────────────────────┐  ║
║  │ ⬛      │  │                   CONTENIDO DEL MÓDULO                   │  ║
║  │Dashboard│  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 👥      │  │                                                          │  ║
║  │Clientes │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 💲      │  │                                                          │  ║
║  │Tarifas  │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 📋      │  │                                                          │  ║
║  │Cotizac. │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 📅      │  │                                                          │  ║
║  │Program. │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 🏥      │  │                                                          │  ║
║  │ÁreasMéd │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 📦      │  │                                                          │  ║
║  │   OC    │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 🧾      │  │                                                          │  ║
║  │Facturac.│  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 🔔      │  │                                                          │  ║
║  │Alertas  │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ 📖      │  │                                                          │  ║
║  │Historial│  │                                                          │  ║
║  │         │  │                                                          │  ║
║  │ ⚙       │  │                                                          │  ║
║  │Config.  │  │                                                          │  ║
║  │         │  │                                                          │  ║
║  └─────────┘  └──────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
Nota: sidebar colapsable (solo iconos ↔ iconos + texto)
```

---

### 10.2 Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Dashboard                                    📅 Junio 2026   [Este mes ▼]  │
├─────────────────────────────────────────────────────────────────────────────┤
│                          — KPI CARDS —                                       │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│ │📋  18    │ │⏳  5     │ │🏥  3     │ │📅  7     │ │🧾  4     │           │
│ │Abiertas  │ │Pend.     │ │Pend.     │ │Programad.│ │Pend.Fact.│           │
│ │          │ │Cliente   │ │ÁreaMéd.  │ │          │ │          │           │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│ ┌──────────────────────┐ ┌──────────────────────────┐                       │
│ │ 💰 $142.350.000      │ │ 💵 $89.200.000            │                       │
│ │ Total Cotizado       │ │ Total Facturado           │                       │
│ └──────────────────────┘ └──────────────────────────┘                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────┐  ┌──────────────────────────────────┐  │
│  │     ALERTAS ACTIVAS            │  │     ACTIVIDAD RECIENTE           │  │
│  │ ────────────────────────────── │  │ ──────────────────────────────── │  │
│  │ 🔴 Factura vencida — COT-0047  │  │ 14:22 · PDF generado COT-0051    │  │
│  │     Vencida hace 3 días        │  │ 13:45 · Área Médica aprobó COT-  │  │
│  │ 🟡 OC demorada — COT-0043      │  │        0048                      │  │
│  │     8 días sin recibir         │  │ 11:30 · Cotización enviada a     │  │
│  │ 🟡 Sin respuesta — COT-0039    │  │        Hospital El Tunal         │  │
│  │     5 días sin respuesta       │  │ 09:15 · Nueva cotización creada  │  │
│  │ 🔵 Servicio mañana — COT-0050  │  │        COT-0052                  │  │
│  │     Hospital Nacional 09:00    │  │ Ayer · OC recibida COT-0040      │  │
│  └────────────────────────────────┘  └──────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                  COTIZACIONES POR ESTADO (mini Kanban)               │  │
│  │  BORRADOR  │ ENVIADA  │ ACEPTADA  │  ÁREA MÉD  │ PROGRAMADAS │ FACT  │  │
│  │   ████     │  ████    │  ███      │    ███      │    ███      │  ██   │  │
│  │    4       │   5      │   3       │     3       │     7       │   4   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 10.3 Módulo Clientes — Vista principal + detalle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Clientes                              [🔍 Buscar...]  [+ Nuevo cliente]    │
├──────────────────────────────────────────────────────────────────────────┬──┤
│  [Todos ▼]  [Normal] [Especial]  [Ciudad ▼]                              │  │
│                                                                          │  │
│  ┌──────────────────────────────────────────────────────────────────┐   │  │
│  │ Empresa              NIT          Tipo      Ciudad    Cotizac.   │   │  │
│  ├──────────────────────────────────────────────────────────────────┤   │  │
│  │ ● Hospital El Bosque  890.123.456  ESPECIAL  Bogotá   12 abiert  │   │  │
│  │ ● Clínica Palermo     900.234.567  NORMAL    Bogotá    3 abiert  │   │  │
│  │ ● SOS Médico S.A.     800.345.678  ESPECIAL  Medellín  7 abiert  │   │  │
│  │ ● Cruz Roja Seccional 860.456.789  NORMAL    Bogotá    1 abiert  │   │  │
│  │   ...                                                            │   │  │
│  └──────────────────────────────────────────────────────────────────┘   │  │
└──────────────────────────────────────────────────────────────────────────┘  │
                                                                               │
  Al hacer click en un cliente → se abre panel de detalle (drawer o full-page):
                                                                               │
╔══════════════════════════════════════════════════════════════════════════════╗
║  ← Volver    Hospital El Bosque                           ESPECIAL  ✎ Editar║
╠══════════════════════════════════════════════════════════════════════════════╣
║  NIT: 890.123.456   Bogotá, D.C.   📧 compras@bosque.com   📞 601-234-5678 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [Información] [Contactos] [Tarifas Especiales] [Cotizaciones] [Historial] ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PESTAÑA: Contactos                                     [+ Agregar contacto]║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ ★ Carlos Mendoza — Jefe de Compras   📧 cmendoza@bosque.com   301-xxx  │ ║
║  │   Laura Gómez    — Coordinadora Med  📧 lgomez@bosque.com     302-xxx  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  INTERACCIONES RECIENTES                         [+ Registrar interacción]  ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ 📞 15 Jun · Llamada — Seguimiento cotización COT-0048                  │ ║
║  │    "Confirmaron que la OC está en proceso de aprobación interna"       │ ║
║  │ 📧 10 Jun · Email — Envío cotización COT-0048                         │ ║
║  │ 🤝  5 Jun · Reunión — Presentación de tarifas 2026                    │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  TAREAS PENDIENTES                                       [+ Nueva tarea]    ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ 🔴 [ALTA]  Seguimiento OC — vence mañana                ○ Pendiente   │ ║
║  │ 🟡 [MEDIA] Enviar tarifas 2027 antes del 30 Jun          ○ Pendiente  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

### 10.4 Cotizaciones — Vista Lista / Kanban

**Vista Lista:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Cotizaciones            [Lista] [Kanban]     [🔍 Buscar]  [+ Nueva cot.]   │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Estado ▼] [Cliente ▼] [Fecha ▼] [Asignado ▼]                Ordenar ▼   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ #       Cliente            Estado              Total       Fecha     │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ COT-0052  Hospital Bosque  ● BORRADOR          $0           22 Jun  │  │
│  │ COT-0051  Clínica Palermo  ● COTIZADA       $4.800.000      20 Jun  │  │
│  │ COT-0050  SOS Médico       ● PROGRAMADA     $9.200.000      15 Jun  │  │
│  │ COT-0049  Cruz Roja        ● ENVIADA_CLIENTE $3.100.000     12 Jun  │  │
│  │ COT-0048  Hospital Bosque  ● OC_SOLICITADA  $11.400.000      5 Jun  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Vista Kanban:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│  BORRADOR(2)  COTIZADA(3)  ENVIADA(4)  ACEPTADA(2)  PEND.ÁREA(3) PROGRAMADA │
│  ──────────  ──────────── ─────────── ────────────  ──────────── ──────────  │
│  ┌────────┐  ┌──────────┐ ┌─────────┐ ┌──────────┐  ┌─────────┐ ┌────────┐  │
│  │COT-0052│  │COT-0051  │ │COT-0049 │ │COT-0046  │  │COT-0044 │ │COT-0050│  │
│  │Hosp.   │  │Clínica   │ │Cruz Roja│ │SOS Méd.  │  │Clínica  │ │SOS Méd.│  │
│  │Bosque  │  │Palermo   │ │         │ │          │  │Palermo  │ │        │  │
│  │        │  │$4.800.000│ │$3.1M    │ │$6.5M     │  │$2.3M    │ │$9.2M   │  │
│  │─────── │  │20 Jun    │ │12 Jun ⚠ │ │08 Jun    │  │01 Jun ⚠ │ │15 Jun  │  │
│  │0 event.│  │2 eventos │ │1 evento │ │3 eventos │  │2 eventos│ │4 event.│  │
│  └────────┘  └──────────┘ └─────────┘ └──────────┘  └─────────┘ └────────┘  │
│              ┌──────────┐ ...                                                 │
│              │COT-0047  │                                                    │
│              │...       │                                                    │
│              └──────────┘                                                    │
│  [+ Nuevo]                                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 10.5 Cotización — Vista de detalle

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← Cotizaciones   COT-0051                    [● COTIZADA]   [Historial]      │
├──────────────────────────────────────────────────────────────────────────────┤
│  Hospital El Bosque · Carlos Mendoza                                         │
│  Creada: 20 Jun 2026                                 Total: $4.800.000       │
│                                                                              │
│  ╔══════════════════════════════════════════════════════════════════════════╗│
│  ║  ① BORRADOR  →  ② COTIZADA  →  ③ ENVIADA  →  ④ ACEPTADA  → ...       ║│
│  ╚══════════════════════════════════════════════════════════════════════════╝│
├──────────────────────────────────────────────────────────────────────────────┤
│  ACCIONES DISPONIBLES:  [🖨 Ver PDF]  [📧 Enviar a Cliente]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  EVENTOS                                  [+ Agregar evento] [Duplicar sel.] │
│  ──────────────────────────────────────────────────────────────────────────  │
│  ┌───┬──────────────────┬─────────────┬──────────────┬─────────────────────┐│
│  │ # │ Servicio         │ Fecha       │ Ciudad       │ Total Evento        ││
│  ├───┼──────────────────┼─────────────┼──────────────┼─────────────────────┤│
│  │ 1 │ Ambulancia TAB   │ 25 Jun 2026 │ Bogotá       │ $1.920.000         ││
│  │   │  ↳ 14:00–20:00  Ordinario│ 5h diurnas + 1h nocturna │ +$50.000 peaje││
│  ├───┼──────────────────┼─────────────┼──────────────┼─────────────────────┤│
│  │ 2 │ Paramédico       │ 25 Jun 2026 │ Bogotá       │ $2.880.000         ││
│  │   │  ↳ 08:00–18:00  Ordinario│ 10h diurnas          │                  ││
│  ├───┴──────────────────┴─────────────┴──────────────┴─────────────────────┤│
│  │                              Subtotal eventos: $4.750.000               ││
│  │                              Extras:              $50.000               ││
│  │                              TOTAL:             $4.800.000              ││
│  └─────────────────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────────────────┤
│  HISTORIAL DE ESTA COTIZACIÓN                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  20 Jun 14:30 · Sistema · Cotización creada                                  │
│  20 Jun 15:45 · Admin · 2 eventos agregados                                  │
│  20 Jun 16:00 · Sistema · Totales recalculados                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 10.6 Formulario de Evento (modal / inline)

```
╔══════════════════════════════════════════════════════╗
║  Agregar Evento                               [✕]   ║
╠══════════════════════════════════════════════════════╣
║  Servicio        [Ambulancia TAB          ▼]         ║
║  Fecha           [25/06/2026 🗓]                    ║
║  Hora inicio     [14:00 🕐]  Hora fin  [20:00 🕐]  ║
║                                                      ║
║  ─ Calculado automáticamente: ─                     ║
║  Tipo de día:    ● Ordinario  (Lunes)               ║
║  Horas diurnas:  5.00 h  (14:00 – 19:00)            ║
║  Horas nocturnas:1.00 h  (19:00 – 20:00)            ║
║                                                      ║
║  Ciudad          [Bogotá, D.C.             ▼]        ║
║  Dirección       [Cra. 7 #40-62                   ]  ║
║  Contacto        [Dr. Juan López                  ]  ║
║  Teléfono        [300-123-4567                    ]  ║
║  Observaciones   [                               ]   ║
║                                                      ║
║  EXTRAS                          [+ Agregar extra]  ║
║  ─────────────────────────────────────────────────  ║
║  Peaje · Autopista Norte · $50.000           [✕]   ║
║                                                      ║
║  ─ Resumen de costos: ─                            ║
║  5h diurnas  × $320.000 =  $1.600.000              ║
║  1h nocturna × $270.000 =    $270.000              ║
║  Extras                  =    $50.000              ║
║  ─────────────────────────────────────             ║
║  TOTAL EVENTO             $1.920.000              ║
║                                                      ║
║              [Cancelar]  [Guardar evento]           ║
╚══════════════════════════════════════════════════════╝
```

---

### 10.7 Programación — Vista Calendario

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Programación               [◄ Jun 2026 ►]  [Mes] [Semana]  [🔄 Sync Out.] │
├─────────────────────────────────────────────────────────────────────────────┤
│  Lun    Mar    Mié    Jue    Vie    Sáb    Dom                              │
│                                                                              │
│  ──22── ──23── ──24── ──25── ──26── ──27── ──28──                          │
│         ┌────┐        ┌────┐ ┌────┐                                        │
│         │🚑  │        │👨‍⚕️  │ │🚑  │                                        │
│         │TAB │        │MED │ │TAM │                                        │
│         │Hosp│        │SOS │ │CRuz│                                        │
│         │9am │        │14h │ │8am │                                        │
│         └────┘        └────┘ └────┘                                        │
│                                                                              │
│  ──29── ──30──                                                              │
│  ┌────┐                                                                     │
│  │🚑  │                                                                     │
│  │TAB │                                                                     │
│  │Pal.│                                                                     │
│  │11h │                                                                     │
│  └────┘                                                                     │
│                                                                              │
│  Al hacer click en un evento → drawer con detalle + COT asociada             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 10.8 Historial / Timeline global

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Historial de Actividad                                                      │
│  [Entidad ▼] [Usuario ▼] [Desde: ____] [Hasta: ____]   [🔍 Buscar texto]   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ● HOY                                                                       │
│  │                                                                           │
│  ├─ 16:00  👤 Admin · Cotización · COT-0052                                  │
│  │         Borrador creado para Hospital El Bosque                           │
│  │                                                                           │
│  ├─ 15:22  🤖 Sistema · Factura                                              │
│  │         Alerta generada: Factura FACT-0031 vencida                        │
│  │                                                                           │
│  ├─ 14:30  👤 Admin · Cotización · COT-0048                                  │
│  │         Estado cambiado: OC_RECIBIDA → PENDIENTE_FACTURACIÓN              │
│  │                                                                           │
│  ├─ 11:15  👤 Admin · Cliente · Hospital El Bosque                           │
│  │         Interacción registrada: Llamada con Carlos Mendoza                │
│  │                                                                           │
│  ● AYER                                                                      │
│  │                                                                           │
│  ├─ 17:45  👤 Admin · Cotización · COT-0051                                  │
│  │         PDF generado · cotizacion_COT0051_20jun2026.pdf                   │
│  │                                                                           │
│  ├─ 16:00  🤖 Sistema · Cotización · COT-0049                                │
│  │         Correo enviado a cmendoza@bosque.com                              │
│  │                                                                           │
│  └─ ...                                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Design System y Tokens Visuales

### 11.1 Paleta de colores

| Token | Hex | Uso |
|---|---|---|
| `--color-primary` | `#1B6FD8` | Botones primarios, sidebar activo, links |
| `--color-primary-light` | `#E8F0FD` | Fondo de item activo en sidebar, hover en tabla |
| `--color-surface` | `#FFFFFF` | Tarjetas, tablas, formularios |
| `--color-bg` | `#F4F6FA` | Fondo general de la app |
| `--color-border` | `#E2E6EC` | Bordes de tarjetas e inputs |
| `--color-text-primary` | `#111827` | Texto principal |
| `--color-text-secondary` | `#6B7280` | Texto secundario, labels |
| `--color-text-placeholder` | `#9CA3AF` | Placeholders de inputs |
| `--estado-borrador` | `#9CA3AF` | Gris neutro |
| `--estado-cotizada` | `#3B82F6` | Azul |
| `--estado-enviada` | `#8B5CF6` | Violeta |
| `--estado-aceptada` | `#10B981` | Verde |
| `--estado-rechazada` | `#EF4444` | Rojo |
| `--estado-area-med` | `#F59E0B` | Amarillo |
| `--estado-programada` | `#06B6D4` | Cyan |
| `--estado-oc` | `#6366F1` | Índigo |
| `--estado-facturada` | `#84CC16` | Lima |
| `--estado-pagada` | `#16A34A` | Verde intenso |
| `--estado-cerrada` | `#374151` | Gris oscuro |
| `--alerta-info` | `#3B82F6` | Azul |
| `--alerta-advertencia` | `#F59E0B` | Ámbar |
| `--alerta-critica` | `#EF4444` | Rojo |

### 11.2 Tipografía

| Rol | Fuente | Peso | Tamaño |
|---|---|---|---|
| Título de módulo | Inter / Segoe UI Variable | 600 | 22px |
| Subtítulos | Inter | 600 | 16px |
| Cuerpo | Inter | 400 | 14px |
| Labels | Inter | 500 | 12px |
| KPI valor | Inter | 700 | 28px |
| Monospace (PDF paths, IDs) | JetBrains Mono (fallback: Consolas) | 400 | 12px |

### 11.3 Bordes y sombras

| Token | Valor |
|---|---|
| `--radius-sm` | 6px (inputs, badges) |
| `--radius-md` | 10px (tarjetas, panels) |
| `--radius-lg` | 14px (modales, drawers) |
| `--shadow-card` | `0 1px 4px rgba(0,0,0,0.07)` |
| `--shadow-modal` | `0 8px 32px rgba(0,0,0,0.14)` |
| `--shadow-dropdown` | `0 4px 12px rgba(0,0,0,0.10)` |

---

## 12. Integraciones Externas

### 12.1 Outlook — Correo (win32com)

`OutlookEmailService` encapsula completamente la comunicación con Outlook local vía COM. El resto del sistema solo llama a `enviar_cotizacion(cotizacion_id)` o `enviar_a_area_medica(cotizacion_id, area_id)`.

Flujo interno de `enviar_cotizacion`:
1. `PDFService.generar_pdf(cotizacion_id)` → retorna `pdf_path`
2. `OutlookEmailService.crear_correo(destinatario, asunto, cuerpo, adjuntos=[pdf_path])`
3. Correo se envía (o se abre en pantalla para revisión antes de enviar — configurable)
4. Se registra `fecha_enviada_cliente` en la cotización
5. `EstadoService.transicionar(cotizacion_id, ENVIADA_CLIENTE, usuario_id)`
6. `HistorialService` registra automáticamente la acción

### 12.2 Outlook — Calendario (win32com)

`OutlookCalendarService` gestiona eventos del calendario local:

- `crear_evento(programacion_id)` → crea `AppointmentItem`, guarda `EntryID` en `programacion.outlook_event_id`
- `actualizar_evento(programacion_id)` → busca el evento por EntryID y actualiza campos
- `eliminar_evento(programacion_id)` → cancela el evento en el calendario

### 12.3 PDF — ReportLab

`PDFService` usa un `CotizacionPDFBuilder` que acepta el DTO de la cotización y produce:

1. **Encabezado**: logo + datos de empresa (de `Configuracion`) + número y fecha de cotización
2. **Destinatario**: datos del cliente y contacto
3. **Tabla de eventos**: por cada evento, una sección con desglose:
   - Servicio, fecha, horario, ciudad
   - Horas diurnas × tarifa = subtotal diurno
   - Horas nocturnas × tarifa = subtotal nocturno
   - Extras desglosados
   - Total del evento
4. **Resumen financiero**: subtotal, extras totales, gran total
5. **Condiciones comerciales**: texto de `cotizacion.condiciones_comerciales`
6. **Pie de página**: datos legales de la empresa

---

## 13. Trazabilidad Transversal

Todos los métodos que producen cambios de estado, envíos o generación de documentos están decorados con `@registrar_historial`. El decorador captura:

- `fecha_hora`: timestamp del momento de la acción
- `usuario_id`: tomado de la sesión activa
- `entidad_tipo` + `entidad_id`: de los parámetros del método decorado
- `accion`: etiqueta descriptiva definida en el decorador
- `detalle`: argumento opcional que el método puede retornar para enriquecer el registro

Este mecanismo es **estructural** — no depende de que cada desarrollador recuerde llamar a `HistorialService`. Si el método se ejecuta exitosamente, el registro existe.

---

## 14. Estrategia de Implementación

| Fase | Módulos/Componentes | Entregable funcional al terminar la fase |
|---|---|---|
| **0 — Fundaciones** | Project scaffold, DB + Alembic, SessionManager, enums, exceptions, `@registrar_historial`, QSS base, MainWindow + Sidebar | App arranca, sidebar navega entre módulos vacíos |
| **1 — CRM Base** | Clientes (CRUD completo), Contactos, Ciudades, Servicios, Configuración | Se pueden crear y gestionar clientes con múltiples contactos |
| **2 — Motor de Tarifas** | Tarifas general + por cliente, `TarifaService`, `CalendarioService`, `FestivoService` | Se pueden cargar y consultar tarifas; los cálculos de horas pasan los tests unitarios |
| **3 — Cotizaciones (núcleo)** | Cotización CRUD, Eventos (agregar/eliminar/duplicar), cálculo automático, extras, totales | Se puede crear una cotización completa con múltiples eventos y ver el desglose |
| **4 — Kanban y Pipeline** | Vista Kanban de cotizaciones, EstadoService, transiciones de estado | El pipeline es visible y navegable; los estados transicionan correctamente |
| **5 — PDF y Correo** | PDFService (ReportLab), OutlookEmailService, botón "Enviar cotización" | Una cotización puede convertirse en PDF y enviarse por Outlook |
| **6 — Área Médica** | CRUD ÁreasMédicas, EnvioAreaMedica, aprobaciones | Flujo completo de aprobación médica |
| **7 — Programación + Calendario** | Vista calendario, ProgramacionService, OutlookCalendarService | Los servicios aprobados quedan en la agenda y en Outlook |
| **8 — OC y Facturación** | MódulosOC y Facturación, transiciones de estado relacionadas | Flujo financiero completo desde OC hasta pago |
| **9 — CRM Avanzado** | Interacciones, Tareas, timeline del cliente, drawer de detalle | La ficha de cliente refleja toda la relación |
| **10 — Alertas** | AlertaWorker (QThread), AlertaBell, AlertasView | El sistema avisa proactivamente de situaciones críticas |
| **11 — Dashboard** | DashboardService, KPIs, mini-Kanban, timeline reciente | Visión gerencial operativa en tiempo real |
| **12 — QA y Pulido** | Tests unitarios (calendar, tarifa, estado), tests de integración, refinamiento visual, manual de usuario | Versión 1.0 entregable |

> **Regla de implementación**: las Fases 0–4 son el núcleo irreemplazable. Las Fases 5–11 pueden ejecutarse en paralelo una vez el núcleo está sólido. Nunca se saltea la Fase 0.

---

## 15. Decisiones Abiertas

Antes de comenzar la Fase 0, conviene confirmar:

| # | Pregunta | Opciones | Impacto |
|---|---|---|---|
| 1 | **Tipo de día con eventos que cruzan medianoche** | (A) Usar fecha de inicio del evento | Afecta `CalendarioService` |
| 2 | **Cliente ESPECIAL sin tarifa cargada** | (A) Fallback automático a tarifa general / (B) Bloquear hasta cargar tarifa | Afecta `TarifaService` y UX del formulario |
| 3 | **Formato de numeración de cotizaciones** | COT-AAAA-NNNN (propuesto) / formato institucional existente | Afecta `NumeroGenerador` |
| 4 | **IVA en facturación** | (A) El valor cotizado ya es neto / (B) Se aplica IVA en factura | Afecta modelo `Factura` y PDFService |
| 5 | **Outlook — modo de envío** | (A) Envía directo / (B) Abre Outlook para revisión antes de enviar | Afecta `OutlookEmailService` |
| 6 | **Multiusuario** | Single-user en v1 con modelo preparado / habilitar en v2 | No afecta arquitectura, sí el plan de QA |

---

**Próximo paso:** con las decisiones del §15 confirmadas, se procede a generar el código de la **Fase 0** (scaffold completo del proyecto, modelos SQLAlchemy, migraciones iniciales, MainWindow con sidebar funcional).
