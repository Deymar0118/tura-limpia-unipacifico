# 🚛 Tura Limpia

### Sistema de Gestión y Optimización para la Recolección y Transporte de Residuos Sólidos

- **Universidad del Pacífico Omar Barona Murillo (Sede Campus Universitario)**  
- **Programa:** Ingeniería de Sistemas (8.º Semestre)  
- **Asignatura:** Seminario de Actualización  
- **Periodo Academico:** 2026-2
- **Distrito:** Buenaventura, Valle del Cauca, Colombia

--- 

# Descripción del Proyecto

En el Distrito de Buenaventura se han presentado problemáticas recurrentes asociadas a la acumulación de residuos sólidos en las calles y a periodos prolongados sin el paso de los vehículos recolectores. La operación del servicio a cargo de la empresa Pazífico Limpio S.A.S. E.S.P. se enfrenta a diversos retos operacionales, tales como el estado deficiente de las vías, calles estrechas, congestión vehicular, obras civiles, bloqueos y situaciones de orden público.

Este proyecto busca analizar la gestión actual del proceso de recolección y transporte de residuos sólidos para identificar los principales factores críticos que afectan la continuidad y eficiencia del servicio. Asimismo, plantea el desarrollo de una herramienta de software centralizada que permita optimizar el control operativo y el registro de incidencias.

---

# Requisitos funcionales

### Usuarios y autenticación

| ID | Descripción |
| --- | --- |
| RF-01 | Gestionar los roles: Cliente/Ciudadano, Trabajador, Gerente y Administrador. |
| RF-02 | El sistema debe permitir al ciudadano registrar una cuenta opcional (Rol: Cliente/Ciudadano) para acceder a funciones de valor agregado. |
| RF-03 | El sistema debe garantizar la visualización abierta del dashboard de rutas, frecuencias y horarios de recolección para usuarios invitados (no autenticados). |
| RF-04 | Permitir que el Administrador registre usuarios con rol de Gerente. |
| RF-05 | Permitir que un Gerente registre usuarios con rol de Trabajador. |
| RF-06 | Inicio de sesión seguro con credenciales (correo/usuario y contraseña), asignando permisos según el rol. |

### Rutas y seguimiento de camiones

| ID | Descripción |
| --- | --- |
| RF-07 | Consultar en tiempo real la ubicación geográfica exacta de un camión recolector específico (Clientes, Trabajadores y Administradores). |
| RF-08 | Mostrar una tabla ordenada con las rutas asignadas a cada vehículo compactador: sectores/barrios, días de operación y horario estimado de llegada. |
| RF-09 | Permitir al Administrador y al Gerente crear, modificar o suspender rutas, definir el trazado de los recorridos y actualizar horarios. |

### Cuadrillas de barrido

| ID | Descripción |
| --- | --- |
| RF-10 | Permitir al Administrador y al Gerente gestionar trabajadores de barrido: **asignar** a un grupo o sector, **cambiar** de grupo o sector, y **eliminar** (remover o dar de baja en la programación). |
| RF-11 | Consultar la composición de cada grupo de barrido y la lista de trabajadores por barrio. |

### Flota e incidencias

| ID | Descripción |
| --- | --- |
| RF-12 | Registrar y consultar el estado operativo de la flota: disponible, en servicio, en mantenimiento o fuera de servicio. |
| RF-13 | Permitir a trabajadores, gerentes y administradores registrar novedades o imprevistos en ruta (bloqueos de vías, fallas mecánicas, inundaciones, congestión o calles estrechas). |

---

# Arquitectura

El sistema se implementará bajo una Arquitectura RESTful, dividiendo la solución en dos entidades completamente independientes: Cliente (Frontend) y Servidor (Backend). Esta separación garantiza que cada módulo pueda evolucionar, mantenerse y escalar de forma autónoma según las exigencias del entorno.

### Principios Clave de la Arquitectura:
- Especialización del Cliente (Frontend): Permite construir interfaces de usuario avanzadas, reactivas y amigables, enfocadas en ofrecer la mejor experiencia posible para todos los usuarios.

- Especialización del Servidor (Backend): Concentra la lógica de negocio orientada a la gestión de flotas y rutas, la validación de esquemas operativos y la persistencia de datos, exponiendo sus capacidades mediante una API REST para ser consumida por el cliente (frontend)

- Escalabilidad Independiente: Al estar desacoplados, es posible escalar el servidor sin afectar el cliente o viceversa.

---

# Backend

### Estructura de Carpetas

```text
backend/
├── .env.example                      # Plantilla de variables de entorno
├── requirements.txt                  # Dependencias del proyecto
├── Procfile                          # Configuración de despliegue
├── seed_admin.py                     # Script para inicializar usuario administrador
└── src/
    ├── main.py                       # Punto de entrada de FastAPI y middlewares
    ├── assets/                       # Diagramas y recursos estáticos propios del backend
    ├── core/                         # Configuración central, BD, excepciones y prompts
    ├── models/                       # Modelos ORM
    ├── repository/                   # Acceso a datos (Patrón Repository)
    ├── routers/                      # Endpoints REST (FastAPI Routers)
    ├── schemas/                      # DTOs y validaciones con Pydantic
    ├── security/                     # Seguridad, JWT, hashing y control de acceso
    └── services/                     # Lógica de negocio

```

--- 

# Frontend

### Estructura de Carpetas

```text
frontend/
├── index.html
├── package.json
├── vite.config.js
├── .oxlintrc.json
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── index.css
    ├── app/                          # Capa transversal (guards, layouts, navegación, sesión)
    │   ├── icons.jsx
    │   ├── navigation.jsx
    │   ├── session.js
    │   ├── guards/
    │   └── layouts/
    ├── modules/                      # Módulos por dominio (Screaming Architecture)
    │   ├── <modulo>/                 # Estructura interna: components/, pages/, services/, types/
    └── shared/                       # Recursos compartidos reutilizables (ui, api, assets)
        ├── api/
        ├── assets/
        └── ui/
```

