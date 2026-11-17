
import { Link, useLocation } from 'react-router-dom'
import { getUsuario } from '../../../app/session'

export default function ConstructionPage() {
  const location = useLocation()
  const usuario = getUsuario()

  const rol = (usuario?.rol || 'usuario').toLowerCase()

  const nombreRol = {
    admin: 'Administrador',
    gerente: 'Gerente',
    trabajador: 'Trabajador',
    ciudadano: 'Ciudadano',
  }

  // Información recibida desde el Dashboard
  const modulo = location.state?.modulo

  const titulo = modulo?.titulo || 'Módulo en construcción'
  const historias = modulo?.historias || 'Próximamente'
  const descripcion =
    modulo?.descripcion ||
    'Este módulo todavía se encuentra en desarrollo. Estamos preparando nuevas funcionalidades para mejorar la gestión de residuos sólidos en Buenaventura.'

  const funcionalidades = modulo?.funcionalidades || []

  const rutaRegreso = rol === 'admin' ? '/dashboard' : '/'

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
          padding: '45px 35px',
          textAlign: 'center',
          background: '#ffffff',
          borderRadius: '24px',
          boxShadow: '0 20px 60px rgba(15, 23, 42, 0.08)',
          border: '1px solid #e2e8f0',
        }}
      >
        <div
          style={{
            width: '90px',
            height: '90px',
            margin: '0 auto 22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '50%',
            background: '#dcfce7',
            color: '#15803d',
            fontSize: '42px',
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
            margin: '22px 0 12px',
            color: '#0f172a',
            fontSize: 'clamp(27px, 5vw, 38px)',
            fontWeight: '800',
            lineHeight: '1.2',
          }}
        >
          {titulo}
        </h1>

        <span
          style={{
            display: 'inline-block',
            marginBottom: '20px',
            padding: '7px 14px',
            borderRadius: '20px',
            background: '#fef3c7',
            color: '#92400e',
            fontSize: '12px',
            fontWeight: '700',
          }}
        >
          En desarrollo · {historias}
        </span>

        <p
          style={{
            maxWidth: '570px',
            margin: '0 auto',
            color: '#64748b',
            fontSize: '15px',
            lineHeight: '1.8',
          }}
        >
          {descripcion}
        </p>

        {funcionalidades.length > 0 && (
          <div
            style={{
              margin: '30px auto',
              padding: '24px',
              textAlign: 'left',
              borderRadius: '16px',
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
            }}
          >
            <h2
              style={{
                margin: '0 0 18px',
                color: '#0f172a',
                fontSize: '17px',
                fontWeight: '800',
              }}
            >
              Funcionalidades previstas
            </h2>

            <ul
              style={{
                display: 'grid',
                gap: '13px',
                margin: 0,
                padding: 0,
                listStyle: 'none',
              }}
            >
              {funcionalidades.map((funcionalidad, index) => (
                <li
                  key={index}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '10px',
                    color: '#475569',
                    fontSize: '14px',
                    lineHeight: '1.6',
                  }}
                >
                  <span
                    style={{
                      color: '#16a34a',
                      fontWeight: '800',
                    }}
                  >
                    ✓
                  </span>
                  {funcionalidad}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div
          style={{
            maxWidth: '420px',
            margin: '28px auto',
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
            to={rutaRegreso}
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
            ← Volver al Dashboard
          </Link>
        </div>

        <footer
          style={{
            marginTop: '40px',
            paddingTop: '20px',
            borderTop: '1px solid #e2e8f0',
            color: '#94a3b8',
            fontSize: '12px',
          }}
        >
          © {new Date().getFullYear()} Tura Limpia. Por una Buenaventura más limpia.
        </footer>
      </section>
    </main>
  )
}
