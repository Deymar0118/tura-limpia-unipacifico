# Guía Visual y Sistema de Diseño · Tura Limpia

**Seminario de Actualización — Universidad del Pacífico (Buenaventura, Colombia)**  
*Documento de Especificación de Interfaz y Estilos Oficiales para el Frontend*  
*Versión: 2.0 — Actualizada conforme al código fuente del proyecto*

---

## 1. Introducción y Propósito

Esta guía establece las directrices visuales, tokens de diseño y patrones de componentes aplicados en el frontend de **Tura Limpia**. Su objetivo es garantizar una experiencia de usuario moderna, consistente y accesible para la comunidad del Distrito de Buenaventura, los operarios y el personal administrativo de **Pacífico Limpio S.A.S. E.S.P.**

La identidad visual combina la estética ecológica y marítima de Buenaventura con una interfaz limpia, legible y optimizada para dispositivos móviles y de escritorio.

---

## 2. Identidad Visual y Filosofía de Marca

El sistema gráfico toma como base los símbolos del territorio y la misión del proyecto:

1. **El Isotipo (Logo):**  
   * **Pin de localización:** Simboliza la georreferenciación y el seguimiento en tiempo real de rutas y compactadores.
   * **Sol naciente (Dorado/Ámbar):** Representa el amanecer en el Pacífico y la energía activa.
   * **Olas marinas (Azul):** Alusión directa a la bahía y al entorno costero de Buenaventura.
   * **Trazado punteado (Verde):** Rutas dinámicas y optimización del recorrido.
   * **Hoja ecológica (Verde vibrante):** Compromiso con la sostenibilidad ambiental y la limpieza urbana.
2. **Atmósfera Visual:**  
   * Fondos claros y aireados (`#F7FBFC`) acompañados de resplandores o gradientes radiales orgánicos en tonos celestes y verdes (`--color-tl-glow-blue`, `--color-tl-glow-green`).
   * Superficies pulidas con desenfoque de fondo (*glassmorphism* suave) en cabeceras fijas.

---

## 3. Paleta Cromática y Tokens de Diseño

Los colores oficiales están definidos como variables CSS globales en `:root` dentro de `src/index.css`.

### 3.1 Colores Principales de Marca

| Token CSS | Valor Hex | Muestra | Uso y Aplicación |
| :--- | :--- | :---: | :--- |
| `--color-tl-green-primary` | `#10B981` | 🟩 | Color de identidad principal, botones de acción primaria, pines de mapa y detalles de éxito. |
| `--color-tl-green-dark` | `#046D4F` | 🌲 | Énfasis, hover de enlaces y contraste con fondos claros. |
| `--color-btn-hover` | `#047857` / `#0F4E61` | 🌿 | Estado hover y activo de botones principales. |
| `--color-tl-blue-primary` | `#0077B6` | 🟦 | Azul mar institucional, enlaces informativos y bordes de acento. |
| `--color-tl-blue-sky` | `#71BBD1` | 🌊 | Acentos suaves, halos de foco en accesibilidad (`focus-visible`) y sombras difusas de elevación. |
| `--color-tl-sun` | `#F59E0B` | ☀️ | Amarillo sol/atardecer. Señalización, alertas preventivas e insignia de datos de prueba. |

### 3.2 Fondos y Superficies

| Token CSS / Elemento | Valor | Propósito |
| :--- | :--- | :--- |
| `--color-tl-bg` | `#F7FBFC` | Fondo general de la aplicación (sustituye al blanco plano para evitar fatiga visual). |
| Superficie de Tarjetas (Cards) | `#FFFFFF` | Contenedores de contenido, modales y formularios. |
| Superficie Alterna | `#F1F8F6` / `#F4F7F6` | Fondos de secciones alternas en landing (e.g., Solución, Cuadrículas). |
| `--color-tl-glow-blue` | `rgba(113, 187, 209, 0.22)` | Resplandor radial ambiental azul. |
| `--color-tl-glow-green` | `rgba(16, 185, 129, 0.18)` | Resplandor radial ambiental verde. |

### 3.3 Jerarquía de Textos

| Token CSS | Valor Hex | Aplicación |
| :--- | :--- | :--- |
| `--color-text-main` | `#0B2545` | Azul marino profundo. Títulos principales (H1, H2) y encabezados de alta jerarquía. |
| `--color-text-body` | `#086A83` | Carbón azulado legible para párrafos, explicaciones y texto descriptivo. |
| `--color-text-muted` | `#0E52B1` | Gris azulado suave para fechas, detalles secundarios e indicadores neutros. |
| `--color-text-highlight-green` | `#15803D` | Verde hoja para destacar palabras clave dentro de títulos (ej. *"Buenaventura"*). |
| `--color-text-highlight-blue` | `#0284C7` | Azul vibrante para destacar nombres de producto o acciones secundarias. |

### 3.4 Estados y Retroalimentación

| Estado | Token / Color | Aplicación |
| :--- | :--- | :--- |
| **Éxito / Activo** | `#10B981` (Fondo `#ECFDF3`) | Operaciones completadas, rutas en circulación y confirmaciones. |
| **Alerta / Prototipo** | `#F59E0B` (Fondo `#FEFCE8` / Borde `#A16207`) | Avisos de contingencia, demoras y advertencia obligatoria de datos simulados. |
| **Error / Peligro** | `#B91C1C` (Fondo `#FEF2F2`) | Mensajes de error en formularios, campos inválidos o acciones destructivas. |

---

## 4. Tipografía Oficial

El proyecto utiliza dos familias tipográficas complementarias, cargadas con soporte para pesos variables y óptima legibilidad en pantallas:

* **Títulos y Display:** `Manrope` (`--font-display`, sans-serif)  
  * *Pesos:* 500 (Medium), 600 (SemiBold), 750 / 800 (ExtraBold).  
  * *Rasgos:* Formas geométricas, interletraje cerrado (`letter-spacing: -0.02em` a `-0.045em`) y alturas de línea compactas (`1.08` a `1.2`).
* **Cuerpo de Texto y UI:** `Plus Jakarta Sans` (`--font-sans`, sans-serif)  
  * *Pesos:* 400 (Regular), 600 (SemiBold), 700 (Bold).  
  * *Rasgos:* Interlineado amplio (`1.6` a `1.7`), ideal para lectura continuada y controles interactivos.

### Escala Tipográfica de la Interfaz

| Nivel / Rol | Familia | Tamaño / Regla | Peso | Ejemplo de Uso |
| :--- | :--- | :--- | :---: | :--- |
| **Título Principal (Hero)** | Manrope | `clamp(2.3rem, 4.6vw, 3.5rem)` | 500 - 800 | Portada principal y bienvenida en módulos clave. |
| **Título de Sección (H2)** | Manrope | `clamp(1.7rem, 3.5vw, 2.8rem)` | 500 - 600 | Título de bloques ("Contexto", "Nuestra Solución"). |
| **Subtítulo / Tarjeta (H3)** | Manrope | `1.1rem` - `1.25rem` (18-20px) | 600 - 700 | Títulos dentro de tarjetas operativas y modales. |
| **Cuerpo de Lectura** | Plus Jakarta Sans | `1.0rem` - `1.02rem` (16px) | 400 | Párrafos informativos y explicaciones. |
| **Botones y Enlaces** | Manrope / Sans | `0.98rem` - `1.0rem` (15-16px) | 700 - 750 | Botones primarios, secundarios e ítems de menú. |
| **Badges / Kickers** | Plus Jakarta Sans | `0.72rem` - `0.85rem` (12-13px) | 700 - 800 | Etiquetas superiores en mayúsculas y etiquetas de estado. |

---

## 5. Espaciado, Formas y Radios

Para mantener coherencia espacial y estética curva contemporánea, se estandarizan las siguientes dimensiones:

### 5.1 Radios de Borde (Border Radius)

* **Botones e Insignias (Pill style):** `border-radius: 999px` (Completamente redondeados).
* **Campos de Formulario (Inputs):** `border-radius: 12px`.
* **Tarjetas y Paneles Informativos:** `border-radius: 16px` a `20px`.
* **Imágenes y Módulos Gráficos:** `border-radius: 12px`.
* **Alertas y Mensajes de Validación:** `border-radius: 10px`.

### 5.2 Márgenes y Relleno (Padding)

* **Botones:** `padding: 8px 18px` (compactos / navegación) o `padding: 12px 20px` (formularios principales).
* **Campos de Entrada (Inputs):** `padding: 12px 16px` (altura total resultante de ~46px a 48px).
* **Tarjetas:** `padding: 24px` a `28px`.
* **Secciones de Contenido:** `padding: 72px 40px 80px` en pantallas grandes; `padding: 44px 20px 64px` en móviles.
* **Separación entre Campos de Formulario:** `gap: 18px`.

---

## 6. Especificación de Componentes Clave

### 6.1 Botones

1. **Botón Primario (`.hero__btn--primary`, `.auth-btn`):**  
   * Fondo: `--color-btn-bg` (`#10B981`).
   * Color de texto: Blanco (`#FFFFFF`).
   * Borde: Ninguno. Radio: `999px`.
   * Sombra de elevación: `box-shadow: 0 12px 26px rgba(113, 187, 209, 0.35)`.
   * **Hover:** Transición suave a `#047857` o `#0F4E61`, elevación con `transform: translateY(-2px)` y sombra incrementada.
   * **Foco accesible (`:focus-visible`):** Anillo exterior `outline: 3px solid var(--color-tl-blue-sky)` con `outline-offset: 3px`.
2. **Botón Secundario / Outline (`.hero__btn--secondary`):**  
   * Variante para acciones secundarias o de exploración sin competir con la acción prioritaria.
3. **Estado Deshabilitado:**  
   * `opacity: 0.6`, `cursor: not-allowed` y supresión de traslaciones o efectos de hover.

### 6.2 Cabecera y Navegación (`LandingHeader`)

* **Posición:** `position: sticky; top: 0; z-index: 40`.
* **Superficie:** Fondo translúcido `rgba(247, 251, 252, 0.85)` con `backdrop-filter: blur(10px)` para lectura limpia sobre contenido desplazado.
* **Marca:** Logotipo SVG `TuraLimpiaLogo` junto al nombre institucional en Manrope 800.
* **Acceso de Usuario:** Botón pill de *"Iniciar sesión"* siempre visible en la cabecera.

### 6.3 Campos de Formulario (`auth-field`, `auth-input`)

* **Etiqueta (Label):** Visible y persistente sobre el campo, peso 700 en `var(--color-text-main)`.
* **Caja de Entrada (Input):**  
  * Fondo blanco (`#FFFFFF`), borde sutil de 1px.
  * Texto de entrada en `var(--color-text-main)`, placeholder en `var(--color-text-muted)`.
  * **Al hacer foco (`:focus-visible`):** Borde coloreado en `--color-btn-bg` (`#10B981`) y halo exterior `outline: 3px solid var(--color-tl-blue-sky)` con offset de 2px.
* **Mensajes de Error:**  
  * Caja tipo banner debajo del campo o formulario: fondo `#FEF2F2`, texto `#B91C1C`, radio `10px`, `padding: 10px 14px`.

### 6.4 Tarjetas (Cards) y Microinteracciones

* Fondo blanco puro (`#FFFFFF`) con bordes suaves o halos de resplandor mediante sombras compuestas:
  `box-shadow: 0 6px 24px rgba(18, 40, 76, 0.06);`
* **Comportamiento Hover:** En dispositivos que admiten cursor, la tarjeta asciende con `transform: translateY(-6px)`, acentuando su sombra y resaltando su borde hacia un tono verde suave (`#8BD3AC`).

### 6.5 Insignias con Indicador de Estado (Badge Dots)

Utilizadas para categorizar secciones e indicar operatividad:
* **Estructura:** Contenedor pill con fondo `var(--color-tl-glow-green)` y tipografía pequeña en peso 700.
* **Punto central (Dot):** Círculo de 6px en `--color-tl-green-dark` con sombra/anillo exterior `box-shadow: 0 0 0 4px var(--color-btn-bg)`.

---

## 7. Norma Obligatoria: Señalización de "Dato de Prueba"

Al tratarse de una solución desarrollada en un entorno académico y en fase de validación con datos preliminares, **toda sección, tabla o componente que represente recorridos, horarios o frecuencias simuladas debe incluir de forma visible la siguiente advertencia:**

```text
[!] DATO DE PRUEBA / EN VALIDACIÓN
Información generada con fines académicos y de prototipo. No corresponde a la programación oficial en tiempo real.
```

* **Estilo del Banner:**
  * **Fondo:** `#FEFCE8` (Amarillo muy claro).
  * **Borde:** 1px sólido en `#F59E0B` (Amarillo Sol / Ámbar).
  * **Texto e Icono:** `#A16207` (Ámbar oscuro de alto contraste).
  * **Radio:** `10px` a `12px`.
  * **Padding:** `12px 16px`.

---

## 8. Criterios de Accesibilidad y Responsividad

1. **Navegación por Teclado:**  
   Todo enlace, botón y campo interactivo debe conservar su indicador visible de foco (`:focus-visible`) mediante el token `--color-tl-blue-sky` (`#71BBD1`), sin depender exclusivamente del cambio de color de fondo.
2. **Contraste de Color:**  
   Los pares cromáticos principales (`#0B2545` sobre `#F7FBFC`, y `#FFFFFF` sobre `#10B981`) satisfacen el nivel **WCAG 2.1 AA** para legibilidad óptima.
3. **Puntos de Interrupción Responsiva (Breakpoints):**  
   * **Desktop grande:** Contenedor máximo acotado a `1200px` centrado.
   * **Tablets y pantallas medianas (`<= 1100px`):** Reorganización de columnas en rejillas (grid) y reducción moderada de espaciados.
   * **Móviles (`<= 860px`):** Conversión a columna única (1fr), despliegue de menú hamburguesa móvil en cabecera y ocultamiento de paneles ornamentales en vistas de autenticación para priorizar el formulario.

