import TuraLimpiaLogo from '../../../shared/assets/TuraLimpiaLogo.png'
import './LandingFooter.css'

function LandingFooter() {
  return (
    <footer className="landing-footer">
      <div className="landing-footer__inner">
        <div className="landing-footer__main">
          <div className="landing-footer__brand">
            <img src={TuraLimpiaLogo} alt="" width="44" height="44" />
            <div>
              <p className="landing-footer__name">Tura Limpia</p>
              <p className="landing-footer__message">Cuidemos juntos a Buenaventura</p>
            </div>
          </div>

          <nav className="landing-footer__nav" aria-label="Enlaces del pie de página">
            <a className="landing-footer__link" href="/contacto">
              <span>Contáctanos</span>
              <span aria-hidden="true">↗</span>
            </a>
            <a className="landing-footer__link" href="/privacidad">
              <span>Política de privacidad</span>
              <span aria-hidden="true">↗</span>
            </a>
          </nav>
        </div>

        <div className="landing-footer__bottom">
          <span>© 2026 Tura Limpia</span>
          <span className="landing-footer__bottom-accent">Tecnología al servicio de Buenaventura</span>
        </div>
      </div>
    </footer>
  )
}

export default LandingFooter
