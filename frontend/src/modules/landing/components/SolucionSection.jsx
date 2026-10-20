import "./SolucionSection.css";

/* Iconos inline (stroke = currentColor). Si ya los tienes en shared/icons.jsx,
   puedes reemplazarlos por esos para mantener consistencia con ImpactoMetas. */
const Svg = ({ children }) => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    {children}
  </svg>
);

const IconGps = () => (
  <Svg>
    <path d="M12 21s-6.5-5.6-6.5-11A6.5 6.5 0 0 1 18.5 10c0 5.4-6.5 11-6.5 11z" />
    <circle cx="12" cy="10" r="2.3" />
  </Svg>
);

const IconFlota = () => (
  <Svg>
    <path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z" />
    <circle cx="7" cy="17.5" r="1.8" />
    <circle cx="17" cy="17.5" r="1.8" />
  </Svg>
);

const IconIncidencias = () => (
  <Svg>
    <path d="M12 3 2.5 20h19L12 3z" />
    <path d="M12 10v4.5M12 17.2v.1" />
  </Svg>
);

const IconMetricas = () => (
  <Svg>
    <path d="M4 20V4M4 20h16" />
    <path d="m7.5 15 4-4 3 3 5-6" />
  </Svg>
);

const TARJETAS = [
  {
    id: "gps",
    titulo: "Monitoreo & GPS",
    texto:
      "Aprovecha la infraestructura GPS preexistente para el seguimiento satelital de las rutas de los camiones compactadores (15 yd³ y 18 yd³).",
    Icono: IconGps,
    tono: "verde",
  },
  {
    id: "flota",
    titulo: "Control de Flota y Mantenimientos",
    texto:
      "Registro y control del estado operativo de los vehículos: activos, en mantenimiento (preventivo/correctivo) y fuera de servicio.",
    Icono: IconFlota,
    tono: "violeta",
  },
  {
    id: "incidencias",
    titulo: "Control de Incidencias",
    texto:
      "Reporte y seguimiento de novedades en ruta, como bloqueos, inundaciones o averías, para reaccionar a tiempo.",
    Icono: IconIncidencias,
    tono: "ambar",
  },
  {
    id: "metricas",
    titulo: "Métricas de Eficiencia",
    texto:
      "Tableros para apoyar la meta operativa: reducir el tiempo medio de recolección de 4,0 h a 3,5 h por ruta.",
    Icono: IconMetricas,
    tono: "azul",
  },
];

export default function SolucionSection() {
  return (
    <section
      id="solucion"
      className="solucion"
      aria-labelledby="solucion-titulo"
    >
      <div className="solucion__contenedor">
        <header className="solucion__encabezado">
          <span className="solucion__etiqueta">Nuestra Solución</span>
          <h2 id="solucion-titulo" className="solucion__titulo">
            Gestión Centralizada e Inteligente para Pacífico Limpio S.A.S. E.S.P.
          </h2>
        </header>

        <div className="solucion__tarjetas">
          {TARJETAS.map(({ id, titulo, texto, Icono, tono }) => (
            <article key={id} className="solucion__tarjeta">
              <span className={`solucion__icono solucion__icono--${tono}`}>
                <Icono />
              </span>
              <h3>{titulo}</h3>
              <p>{texto}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
