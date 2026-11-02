import './CaracteristicasSection.css';
import { MapPin, Truck, AlertTriangle, LayoutDashboard } from 'lucide-react';

const features = [
  {
    icono: MapPin, 
    title: 'Registro y consulta de rutas',
    description: 'Módulo para visualizar la programación, frecuencias y sectores asignados a la recolección.',
  },
  {
    icono: Truck,
    title: 'Inventario y estado de flota',
    description: 'Listado detallado de los vehículos disponibles, activos o en mantenimiento.',
  },
  {
    icono: AlertTriangle,
    title: 'Registro de incidencias',
    description: 'Espacio práctico para reportar novedades operativas como bloqueos, congestiones o vías de difícil acceso.',
  },
  {
    icono: LayoutDashboard,
    title: 'Seguimiento operativo',
    description: 'Panel centralizado para consultar los datos generales de la operación de forma organizada.',
  },
];

function CaracteristicasSection() {
  return (
    <section className="landing-section landing-section--features" id="caracteristicas" aria-labelledby="features-title">
        <div className="container">
            <span className="etiqueta"><span className='badge-dot ' aria-hidden="true" />Características</span>
          <h2 className="landing-section__title" id="features-title">Características</h2>
          <div className="landing-section__features-grid">
            {features.map((feature) => (
                <article className="landing-feature" key={feature.title}>
                    <div className="landing-feature__icon"><feature.icono /></div>
                    <h3 className="landing-feature__title">{feature.title}</h3>
                    <p className="landing-feature__description">{feature.description}</p>
                </article>
            ))}
          </div>
        </div>
      </section>
  );
}

export default CaracteristicasSection