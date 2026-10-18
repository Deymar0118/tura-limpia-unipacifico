import React from 'react'

function TuraLimpiaLogo({ size = 32, title = 'Tura Limpia' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label={title}
    >
      {/* Contenedor principal: Pin de localización de fondo */}
      <path
        d="M16 2C10.48 2 6 6.48 6 12C6 18.5 14.2 28.3 15.25 29.53C15.64 29.99 16.36 29.99 16.75 29.53C17.8 28.3 26 18.5 26 12C26 6.48 21.52 2 16 2Z"
        fill="var(--color-tl-primary, #10B981)"
      />

      {/* Círculo central blanco (Lienzo interno) */}
      <circle cx="16" cy="12" r="8.5" fill="#FFFFFF" />

      {/* Ilustración de Buenaventura: Sol/Amanecer */}
      <circle cx="16" cy="9.5" r="3" fill="var(--color-tl-sun, #F59E0B)" />

      {/* Olas del mar / Puerto */}
      <path
        d="M9.5 13.5C11 12.5 12.5 14 14 13.5C15.5 13 17 14 18 13.5C19.5 13 21 14 22.5 13.5"
        stroke="var(--color-tl-ocean, #0284C7)"
        strokeWidth="1.2"
        strokeLinecap="round"
      />

      {/* Ruta optimizada de recolección (Camino trazado) */}
      <path
        d="M10 17.5C12 16 14.5 18 17 16.5C19 15.2 20.5 16 22 15.5"
        stroke="var(--color-tl-route, #059669)"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeDasharray="0.8 1.5"
      />

      {/* Hoja ecológica / Sostenibilidad ambiental */}
      <path
        d="M18.5 12.5C18.5 12.5 22.5 12.5 23.5 15.5C21 16.5 19 14.5 18.5 12.5Z"
        fill="var(--color-tl-leaf, #22C55E)"
      />
      <path
        d="M19 13.2C20.5 14.2 21.8 14.8 23 15"
        stroke="#FFFFFF"
        strokeWidth="0.8"
        strokeLinecap="round"
      />
    </svg>
  )
}

export default TuraLimpiaLogo