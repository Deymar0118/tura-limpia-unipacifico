import TuraLimpiaPreview from './TuraLimpiaAssistant'
import './HeroSection.css'


const checks = [
  'Control de flota activa',
  'Registro de incidencias',
  'Optimización de rutas',
  'Trazabilidad operativa',
]

function CheckIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <circle cx="8" cy="8" r="7.2" fill="var(--color-tl-bg-3, #E6F4EA)" />
      <path
        d="M4.4 8.3 6.6 10.5 11.7 5.4"
        stroke="var(--color-tl-primary, #10B981)"
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function HeroSection() {
  return (
    <section className="hero" id="inicio">
      <div className="hero__content">
        <span className="hero__badge">
          <span className="hero__badge-dot" aria-hidden="true" />
          Buenaventura más limpio, juntos
        </span>

        <h1 className="hero__title">
          Optimización e Inteligencia Operativa para la Recolección de 
          Residuos en <span className="hero__title-accent">Buenaventura.</span>
        </h1>

        <p className="hero__description">
          Una plataforma tecnológica orientada al seguimiento en tiempo real,
          trazabilidad de rutas y control de incidencias para 
          mejorando la eficiencia sobre el servicio de aseo 
          en el Distrito de Buenaventura.
        </p>

        <div className="hero__actions">
          <a className="hero__btn hero__btn--primary" href="#contexto">
            Saber más
            <span aria-hidden="true">→</span>
          </a>
          <a className="hero__btn hero__btn--secondary" href="/dashboard">
            Ver rutas
          </a>
        </div>

        <ul className="hero__checks">
          {checks.map((check) => (
            <li key={check} className="hero__check">
              <CheckIcon />
              <span>{check}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className='here__preview' id='robot-ecologico'>
        <TuraLimpiaPreview/>
      </div>

    </section>
  )
}

export default HeroSection