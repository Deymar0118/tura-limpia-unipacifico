import './ContextSection.css'
import PaneRuta from '../../../shared/assets/panel-rutas.png'
import {Recycle,Construction,
  Truck,ClipboardX,} from "lucide-react"; 


const steps = [
  {
    icono: Recycle,
    title: 'Volumen masivo',
    description: 'En Buenaventura se generan aproximadamente 6.700 toneladas mensuales de residuos sólidos (5.500 t llevadas a disposición final).',
  },
  {
    icono: Construction,
    title: 'Retos en la movilidad',
    description: 'Factores como congestión vehicular, obras en la vía (ej. Av. Simón Bolívar), calles estrechas, inundaciones y bloqueos afectan los tiempos de viaje y la continuidad del servicio.',
  },
  {
    icono: Truck,
    title: 'Disponibilidad de flota',
    description: 'La falta de visibilidad unificada sobre mantenimientos o vehículos fuera de servicio impacta directamente la cobertura urbana.',
  },
  {
    icono: ClipboardX,
    title: 'Gestión de incidencias',
    description: 'La falta de reporte oportuno sobre puntos críticos, fallas mecánicas o bloqueos impide una respuesta rápida de la operación.',
  },
]

function ContexSection(){
   return (
    <section className="landing-section landing-section--how" id="contexto" aria-labelledby="how-title">
       <div className="landing-section__inner">

         <div className="landing-steps-container">        
            <div className="landing-section__heading">
                <span className="landing-kicker"><span className='badge-dot ' aria-hidden="true" />Contexto</span>
                <h2 className="dos" id="how-title">Transformando los desafios del servicio publico de aseo.</h2>
                <p className='description'>Plataforma tecnológica diseñada para optimizar las rutas de recolección, supervisar 
                    la flota activa y centralizar la atención de incidencias operativas en Buenaventura.</p>
            </div>    
            <div className="landing-steps__image">
                 <img
                 className="tura__character"
                 src={PaneRuta}
                 alt="Transformación del servicio publico de ase"
                />
             </div>        
          </div>

          <div className="landing-steps">
                {steps.map((step) => (
                    <article className="landing-step" key={step.title}>
                    <div className="landing-step__number"><step.icono /></div>
                    <h3>{step.title}</h3>
                    <p className='description'>{step.description}</p>
                    </article>
                ))}
          </div>

        </div>
    </section>

   )
}

export default ContexSection