import { Link } from 'react-router-dom'
import TuraLimpiaLogo from '../../../shared/ui/TuraLimpiaLogo'
import TuraLimpiaPreview from '../../landing/components/TuraLimpiaAssistant'
import './AuthLayout.css'

export default function AuthLayout({ title, accent, description, children, footer }) {
  return (
    <main className="auth">
      <section className="auth__panel">
        <Link className="auth__brand" to="/">
          <span className="auth__logo">
            <TuraLimpiaLogo />
          </span>
          <span>Tura Limpia</span>
        </Link>

        <span className="auth__badge">
          <span className="auth__badge-dot" />
          Buenaventura más limpio, juntos
        </span>

        <h1 className="auth__title">
          {title} <span className="auth__title-accent">{accent}</span>
        </h1>
        <p className="auth__description">{description}</p>

        <div className="auth__card">{children}</div>

        {footer && <p className="auth__footer">{footer}</p>}
      </section>

      <aside className="<TuraLimpiaPreview />">
        <div className="auth__preview">
          <TuraLimpiaPreview />
        </div>
      </aside>
    </main>
  )
}