import RobotEcologico from '../../../shared/assets/Robot_ecologico_en_Buenaventura.png'
import './TuraLimpiaAssistant.css'

const procesamiento = [
  'Reporte recibido',
  'Ruta analizada',
  'Incidencia detectada',
  'Flota asignada',
  'Operación optimizada',
]

const documentos = [
  { nombre: 'optimizacion_rutas', pos: 'tl', tipo: 'map' },
  { nombre: 'mapa_puntos_criticos', pos: 'tr', tipo: 'map' },
  { nombre: 'telemetria_flota', pos: 'bl', tipo: 'data' },
  { nombre: 'registro_incidencias', pos: 'br', tipo: 'doc' },
]

function FileIcon({ tipo }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      {/* Fondo del pin o marcador */}
      <path
        d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"
        fill="var(--color-tl-bg-2, #E6F4EA)"
        stroke="var(--color-tl-green-dark, #047857)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Icono interior según el tipo */}
      {tipo === 'map' ? (
        <path
          d="M9 11l3-3 3 3m-3-3v8"
          stroke="var(--color-tl-sky, #0284C7)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ) : tipo === 'data' ? (
        <circle 
          cx="12" 
          cy="9" 
          r="3" 
          fill="var(--color-tl-sky, #0284C7)" 
        />
      ) : (
        <path
          d="M9 9h6M9 12h4"
          stroke="var(--color-tl-sky, #0284C7)"
          strokeWidth="2"
          strokeLinecap="round"
        />
      )}
    </svg>
  )
}

function TuraLimpiaAssistant({ className = '' }) {
  return (
    <div className={`tura ${className}`.trim()}>
      <svg
        className="tura__lines"
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <line x1="17" y1="15" x2="50" y2="50" className="tura__line" />
        <line x1="83" y1="15" x2="50" y2="50" className="tura__line" />
        <line x1="17" y1="85" x2="50" y2="50" className="tura__line" />
        <line x1="83" y1="85" x2="50" y2="50" className="tura__line" />
      </svg>

      {documentos.map((doc) => (
        <div key={doc.nombre} className={`tura__doc tura__doc--${doc.pos}`}>
          <FileIcon tipo={doc.tipo} />
          <span className="tura__doc-name">{doc.nombre}</span>
        </div>
      ))}

      <div className="tura__figure">
        <img
          className="tura__character"
          src={RobotEcologico}
          alt="Proceso de gestión Tura Limpia"
        />
        <ul className="tura__chips">
          {procesamiento.map((item) => (
            <li key={item} className="tura__chip">
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default TuraLimpiaAssistant