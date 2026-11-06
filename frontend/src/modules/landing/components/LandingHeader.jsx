import { useState } from 'react';
import TuraLimpiaLogo from '../../../shared/ui/TuraLimpiaLogo';
import './LandingHeader.css'

const navItems = [
  { label: 'Inicio', href: '#inicio' },
  { label: 'El Contexto', href: '#contexto' },
  { label: 'Solución', href: '#solucion' },
  { label: 'Características', href: '#caracteristicas' },
  { label: 'Impacto y Metas', href: '#impacto' },
  { label: 'Consultar horarios', href: '#buscar' },
]


export const LandingHeader = () => {

  const [open, setOpen] = useState(false)

  return (
    <header className="landing-header">
      <nav className="landing-nav" aria-label="Navegación principal">
        <a className="landing-nav__brand" href="#inicio">
          <span className="landing-nav__logo">
            <TuraLimpiaLogo />
          </span>
          <span className="landing-nav__name">Tura Limpia</span>
        </a>

        <ul className={open ? 'landing-nav__links is-open' : 'landing-nav__links'}>

            <li className="landing-nav__mobile-action">
              <a className="landing-nav__login" href="/login">
                Iniciar sesión
              </a>
           </li>

          {navItems.map((item) => (
            <li key={item.label}>
              <a className="landing-nav__link" href={item.href}>
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="landing-nav__actions">
          <a className="landing-nav__login" href="/login">
            Iniciar sesión
          </a>

          <button
            type="button"
            className="landing-nav__toggle"
            aria-expanded={open}
            aria-label={open ? 'Cerrar menú de navegación' : 'Abrir menú de navegación'}
            onClick={() => setOpen((value) => !value)}
          >
            <span className="landing-nav__toggle-bar" />
            <span className="landing-nav__toggle-bar" />
            <span className="landing-nav__toggle-bar" />
          </button>
        </div>
      </nav>
    </header>
  );
};
