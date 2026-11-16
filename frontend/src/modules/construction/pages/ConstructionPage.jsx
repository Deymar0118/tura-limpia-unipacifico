
import { Link } from 'react-router-dom'
import { getUsuario } from '../../../app/session'

export default function ConstructionPage() {
  const usuario = getUsuario()

  const rol = usuario?.rol || 'usuario'

  const nombreRol = {
    gerente: 'Gerente',
    trabajador: 'Trabajador',
    ciudadano: 'Ciudadano',
  }

  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '30px 20px',
        background: 'linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%)',
        fontFamily: 'inherit',
      }}
    >
      <section
        style={{
          width: '100%',
          maxWidth: '760px',
          padding: '55px 35px',
          textAlign: 'center',
          background: '#ffffff',
          borderRadius: '24px',
          boxShadow: '0 20px 60px rgba(15, 23, 42, 0.08)',
          border: '1px solid #e2e8f0',
        }}
      >
        <div
          style={{
            width: '100px',
            height: '100px',
            margin: '0 auto 25px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '50%',
            background: '#dcfce7',
            color: '#15803d',
            fontSize: '48px',
          }}
        >
          🚧
        </div>

        <span
          style={{
            display: 'inline-block',
            padding: '8px 16px',
            borderRadius: '30px',
            background: '#eff6ff',
            color: '#1d4ed8',
            fontSize: '12px',
            fontWeight: '700',
            letterSpacing: '1px',
            textTransform: 'uppercase',
          }}
        >
          Tura Limpia
        </span>

        <h1
          style={{
            margin: '22px 0 14px',
            color: '#0f172a',
            fontSize: 'clamp(28px, 5vw, 42px)',
            fontWeight: '800',
            lineHeight: '1.2',
          }}
        >
          ¡Estamos trabajando en ello!
        </h1>

        <p
          style={{
            maxWidth: '550px',
            margin: '0 auto',
            color: '#64748b',
            fontSize: '16px',
            lineHeight: '1.8',
          }}
        >
          El módulo al que intentas acceder todavía se encuentra
          en desarrollo. Nuestro equipo está preparando nuevas
          funcionalidades para mejorar la gestión de residuos
          sólidos en Buenaventura.
        </p>

        <div
          style={{
            maxWidth: '420px',
            margin: '32px auto',
            padding: '18px',
            borderRadius: '14px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
          }}
        >
          <p
            style={{
              margin: '0 0 7px',
              color: '#64748b',
              fontSize: '13px',
            }}
          >
            Tu perfil actual
          </p>

          <strong
            style={{
              color: '#0f172a',
              fontSize: '17px',
            }}
          >
            {nombreRol[rol] || rol}
          </strong>

          <p
            style={{
              margin: '10px 0 0',
              color: '#64748b',
              fontSize: '13px',
            }}
          >
            Estamos preparando tu espacio de trabajo.
          </p>
        </div>

        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            flexWrap: 'wrap',
            gap: '12px',
          }}
        >
          <Link
            to="/"
            style={{
              display: 'inline-block',
              padding: '13px 24px',
              borderRadius: '10px',
              background: '#15803d',
              color: '#ffffff',
              fontWeight: '700',
              fontSize: '14px',
              textDecoration: 'none',
            }}
          >
            Volver al inicio
          </Link>
        </div>

        <footer
          style={{
            marginTop: '45px',
            paddingTop: '20px',
            borderTop: '1px solid #e2e8f0',
            color: '#94a3b8',
            fontSize: '12px',
          }}
        >
          © 2026 Tura Limpia. Por una Buenaventura más limpia.
        </footer>
      </section>
    </main>
  )
}
