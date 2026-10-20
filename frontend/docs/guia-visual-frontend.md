# Guía visual breve — Tura Limpia

Esta guía es la propuesta inicial para que las pantallas del prototipo mantengan una apariencia común. Se basa en las variables y el logo que ya existen en `src/index.css` y en el diseño de la landing actual. Hay que contrastarla con el archivo de Figma antes de declararla definitiva.

## Identidad y tono

- Comunicar una herramienta académica de apoyo a la gestión de recolección en Buenaventura.
- Usar un tono claro, cercano y responsable. No presentar datos simulados como programación oficial ni afirmar que una función está conectada si todavía es un prototipo.
- Dar prioridad a lectura sencilla, navegación visible y acciones fáciles de reconocer.

## Tipografía

| Uso | Familia | Recomendación |
|---|---|---|
| Títulos y nombres de sección | Manrope (`--font-display`) | 600–800; títulos compactos, con interlineado de 1.1–1.25. |
| Párrafos, etiquetas y controles | Plus Jakarta Sans (`--font-sans`) | 400–700; interlineado cercano a 1.5. |
| Texto auxiliar | Plus Jakarta Sans | No bajar de 0.8rem salvo iconos decorativos. |

Las fuentes deben cargarse desde un recurso acordado por el equipo; mientras no se configure, se usa el fallback sans-serif.

## Colores

| Token | Valor actual | Uso recomendado |
|---|---|---|
| `--color-tl-green-primary` | `#10B981` | Acción principal y detalles de identidad. |
| `--color-tl-green-dark` | `#046D4F` | Hover, énfasis y estados que necesitan contraste. |
| `--color-tl-blue-primary` | `#0077B6` | Enlaces, iconos informativos y foco. |
| `--color-tl-blue-sky` | `#71BBD1` | Acentos suaves y contornos de foco. |
| `--color-tl-sun` | `#F59E0B` | Acento puntual, no para texto pequeño sobre blanco. |
| `--color-tl-bg` | `#F7FBFC` | Fondo general. |
| `--color-text-main` | `#0B2545` | Títulos y texto principal. |
| `--color-text-body` | `#086A83` | Texto secundario; verificar contraste antes de usar en cuerpo pequeño. |
| `--color-border` | `#D7E5E9` | Bordes de campos y tarjetas. |
| `--color-error` / `--color-error-bg` | `#B42318` / `#FEF3F2` | Errores de formulario, siempre acompañados de texto. |
| `--color-success` / `--color-success-bg` | `#067647` / `#ECFDF3` | Confirmaciones, siempre acompañadas de texto. |

Evitar depender solo del color para transmitir significado. Comprobar contraste del texto sobre cada fondo antes de cerrar el diseño.

## Espaciado, superficies y controles

- Usar la escala compartida: `--space-1` (4 px), `--space-2` (8 px), `--space-3` (12 px), `--space-4` (16 px), `--space-6` (24 px), `--space-8` (32 px), `--space-12` (48 px).
- Campos y botones: altura mínima de 44 px, borde de 1 px, radio `--radius-control` y texto visible que identifique cada campo.
- Tarjetas y paneles: fondo blanco, borde `--color-border`, radio `--radius-card`; usar sombra suave con moderación.
- Mantener espacios consistentes entre etiqueta, control, ayuda y mensaje de error. En móvil, apilar campos y acciones.

## Botones y enlaces

- **Primario:** fondo verde principal, texto blanco; una acción primaria por bloque cuando sea posible.
- **Hover:** verde oscuro; foco de teclado visible mediante `:focus-visible` y contorno separado del botón.
- **Secundario:** fondo blanco o transparente con borde y texto oscuro; reservar el verde sólido para la acción principal.
- **Deshabilitado:** contraste suficiente para reconocerlo y atributo `disabled`; explicar por qué no está disponible cuando no sea evidente.
- Los enlaces deben tener texto descriptivo; evitar depender solo de iconos.

## Formularios y estados

- Cada control tiene una etiqueta persistente; el placeholder solo ofrece un ejemplo.
- Marcar campos obligatorios de forma explícita y validar sin borrar los datos ya escritos.
- **Error:** mensaje junto al campo, explicación concreta y `aria-describedby`; no indicar el error solo con rojo.
- **Carga:** mostrar estado comprensible y evitar que se envíe el mismo formulario repetidas veces.
- **Éxito:** confirmación breve y perceptible por tecnologías de asistencia (`role="status"`).
- **Sin resultados:** indicar que la consulta se procesó, explicar que no se encontró horario y ofrecer una acción para cambiar la búsqueda.
- **Datos de prueba:** mostrar una nota persistente cerca de los resultados y no usar lenguaje que sugiera información oficial o en tiempo real.

## Estructura propuesta de la landing

1. Encabezado con marca, navegación y acceso de usuario.
2. Hero con el propósito del proyecto y acciones para conocer más o consultar horarios.
3. Sección breve sobre el contexto del servicio en Buenaventura.
4. Sección de la solución y capacidades del prototipo.
5. Buscador público de horarios.
6. Aviso visible cuando la información sea simulada.
7. Pie con naturaleza académica del proyecto y enlaces acordados.

La landing existente ya ofrece el encabezado y el hero. Los enlaces a secciones que aún no existen deben agregarse cuando su contenido se acuerde.

## Buscador público: propuesta para acordar con célula 3

**Entradas mínimas:** barrio, día de recolección y franja horaria. Confirmar con célula 3 si día y franja son filtros opcionales o requeridos, el formato/nombre de barrio, la zona horaria si aplica y cómo se representará la última actualización.

**Resultado sugerido:** barrio consultado, días, franja, fecha de actualización y una etiqueta de datos de prueba hasta que exista información validada. No se fijan horas exactas en este boceto porque aún deben salir del acuerdo con la célula 3.

**Sin horario disponible:** conservar los filtros; mostrar “Sin horarios disponibles para esta búsqueda”; permitir cambiar barrio, día o franja. Diferenciar este estado de un error técnico, que debe explicar que no fue posible consultar y ofrecer reintentar.

El componente `PublicRouteSearch` es un ejemplo visual local: el formulario muestra el estado vacío al enviarse y no consulta una API ni representa horarios reales.
