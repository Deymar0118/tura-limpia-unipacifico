
import {
  Clock3,
  ChartNoAxesColumnIncreasing,
  MapPinned,
} from 'lucide-react'

import './ImpactoMetas.css'

const indicadores = [
  {
    id: 'tiempos',
    titulo: 'Reducción de Tiempos',
    descripcion:
      'Optimización de los tiempos de recolección mediante una mejor planificación de las rutas.',
    icono: Clock3,
    color: 'verde',
  },
  {
    id: 'datos',
    titulo: 'Toma de Decisiones Basada en Datos',
    descripcion:
      'Análisis de reportes e incidencias para identificar retrasos y mejorar la operación.',
    icono: ChartNoAxesColumnIncreasing,
    color: 'azul',
  },
  {
    id: 'cobertura',
    titulo: 'Mayor Cobertura Urbana',
    descripcion:
      'Seguimiento de las zonas atendidas para identificar oportunidades de mejora en el servicio.',
    icono: MapPinned,
    color: 'azul',
  },
]

function ImpactoMetas() {
  return (
    <section
      className="impacto-metas"
      id="impacto"
      aria-labelledby="impacto-metas-titulo"
    >
      <div className="impacto-metas__encabezado">
        <span className="impacto-metas__etiqueta">
          Impacto y Metas
        </span>

        <h2 id="impacto-metas-titulo">
          Resultados que se ven en la ciudad.
        </h2>

        <p>
          Conoce cómo Tura Limpia busca mejorar la eficiencia
          de la recolección de residuos en Buenaventura.
        </p>
      </div>

      <div className="impacto-metas__grid">
        {indicadores.map((indicador) => {
          const Icono = indicador.icono

          return (
            <article
              className="impacto-metas__tarjeta"
              key={indicador.id}
            >
              <div
                className={`impacto-metas__icono impacto-metas__icono--${indicador.color}`}
                aria-hidden="true"
              >
                <Icono size={25} strokeWidth={2} />
              </div>

              <h3>{indicador.titulo}</h3>

              <p>{indicador.descripcion}</p>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default ImpactoMetas
