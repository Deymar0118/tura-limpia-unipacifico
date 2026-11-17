
import { useNavigate, Link } from 'react-router-dom'
import { getSession } from '../../../app/session'
import { cerrarSesion } from '../../auth/services/authService'
import TuraLimpiaLogo from '../../../shared/assets/TuraLimpiaLogo.png'
import './AdminDashboardPage.css'

const modulos = [
  {
    titulo: 'Personal y Cuadrillas',
    historias: 'HU-02 y HU-03',
    descripcion:
      'Registro y administración de trabajadores y conductores, control de licencias y organización de cuadrillas de recolección y barrido.',
    funcionalidades: [
      'Registro y consulta de trabajadores.',
      'Gestión de conductores y licencias.',
      'Creación y administración de cuadrillas.',
      'Asignación de trabajadores a cuadrillas.',
    ],
  },
  {
    titulo: 'Territorio y Rutas',
    historias: 'HU-04 y HU-05',
    descripcion:
      'Administración de la división territorial de Buenaventura y configuración de las rutas de recolección.',
    funcionalidades: [
      'Registro de barrios y comunas.',
      'Configuración de macrorutas.',
      'Creación de microrutas.',
      'Organización de paradas de las rutas.',
    ],
  },
  {
    titulo: 'Programación y Flota',
    historias: 'HU-06 y HU-07',
    descripcion:
      'Planificación de las jornadas de recolección y administración de los vehículos asignados al servicio.',
    funcionalidades: [
      'Programación de frecuencias semanales.',
      'Asignación de turnos y fechas.',
      'Registro y administración de vehículos.',
      'Asignación de vehículos a las rutas.',
    ],
  },
  {
    titulo: 'Monitoreo GPS e Incidencias',
    historias: 'HU-08 a HU-10',
    descripcion:
      'Seguimiento de las operaciones de recolección, control de recorridos y registro de novedades durante la prestación del servicio.',
    funcionalidades: [
      'Visualización de vehículos en el mapa.',
      'Seguimiento de recorridos mediante GPS.',
      'Registro de ejecución de rutas.',
      'Reporte y gestión de novedades e incidencias.',
    ],
  },
]

function AdminDashboardPage() {
  const navigate = useNavigate()
  const sesion = getSession()

  const nombreUsuario =
    sesion?.nombre || sesion?.nombre_usuario || 'Administrador'

  const rolUsuario = sesion?.rol || 'Administrador'

  const handleCerrarSesion = async () => {
    try {
      await cerrarSesion()
    } catch {
      // Ignorar fallos de red al cerrar sesión local
    } finally {
      navigate('/login', { replace: true })
    }
  }

  const abrirModulo = (modulo) => {
    navigate('/construccion', {
      state: { modulo },
    })
  }

  const iconos = {
    personal: (
      <>
        <rect x="2" y="7" width="20" height="14" rx="2" />
        <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
      </>
    ),
    territorio: (
      <>
        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" />
        <line x1="8" y1="2" x2="8" y2="18" />
        <line x1="16" y1="6" x2="16" y2="22" />
      </>
    ),
    flota: (
      <>
        <rect x="1" y="3" width="15" height="13" />
        <polygon points="16 8 20 8 23 11 23 16 16 16 16 8" />
        <circle cx="5.5" cy="18.5" r="2.5" />
        <circle cx="18.5" cy="18.5" r="2.5" />
      </>
    ),
    monitoreo: (
      <>
        <circle cx="12" cy="12" r="10" />
        <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
      </>
    ),
  }

  const tarjetas = [
    {
      modulo: modulos[0],
      icono: iconos.personal,
    },
    {
      modulo: modulos[1],
      icono: iconos.territorio,
    },
    {
      modulo: modulos[2],
      icono: iconos.flota,
    },
    {
      modulo: modulos[3],
      icono: iconos.monitoreo,
    },
  ]

  return (
    <div className="admin-dash-page">
      <header className="admin-dash-header">
        <div className="admin-dash-header-inner">
          <div className="admin-dash-brand">
            <img src={TuraLimpiaLogo} alt="Logo Tura Limpia" />
            <div className="admin-dash-brand-info">
              <span className="admin-dash-brand-title">Tura Limpia</span>
              <span className="admin-dash-brand-sub">
                Panel Administrativo
              </span>
            </div>
          </div>

          <div className="admin-dash-user-menu">
            <div className="admin-dash-user-info">
              <span className="admin-dash-user-name">
                {nombreUsuario}
              </span>
              <span className="admin-dash-user-role">
                {rolUsuario}
              </span>
            </div>

            <button
              type="button"
              className="btn-logout"
              onClick={handleCerrarSesion}
              title="Cerrar sesión segura"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <main className="admin-dash-container">
        <section className="admin-welcome-banner">
          <div className="admin-welcome-text">
            <div className="admin-welcome-badge">
              <span className="admin-welcome-dot" />
              Sistema Operativo Conectado
            </div>

            <h1>Bienvenido, {nombreUsuario}</h1>

            <p>
              Gestiona los accesos del personal y supervisa los módulos
              operativos para la optimización del servicio de aseo en
              Buenaventura.
            </p>
          </div>
        </section>

        <section>
          <div className="admin-section-header">
            <h2 className="admin-section-title">
              Módulos del Sistema
            </h2>
            <p className="admin-section-subtitle">
              Selecciona un área de trabajo para comenzar
            </p>
          </div>

          <div
            className="admin-modules-grid"
            style={{ marginTop: '18px' }}
          >
            <article className="admin-module-card admin-module-card--active">
              <div>
                <div className="admin-card-top">
                  <div className="admin-card-icon-box admin-card-icon-box--active">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      aria-hidden="true"
                    >
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                      <circle cx="9" cy="7" r="4" />
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                  </div>
                  <span className="admin-card-badge admin-card-badge--ready">
                    Disponible
                  </span>
                </div>

                <h3 className="admin-card-title">
                  Gestión de Usuarios
                </h3>

                <p className="admin-card-desc">
                  Consulta, registra y edita información de funcionarios,
                  actualiza documentos de identidad y asigna o modifica
                  roles en el sistema (HU-01).
                </p>
              </div>

              <Link
                to="/admin/usuarios"
                className="admin-card-btn-action"
              >
                Gestionar Usuarios &rarr;
              </Link>
            </article>

            {tarjetas.map(({ modulo, icono }) => (
              <article
                key={modulo.titulo}
                className="admin-module-card admin-module-card--disabled"
              >
                <div>
                  <div className="admin-card-top">
                    <div className="admin-card-icon-box admin-card-icon-box--disabled">
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        aria-hidden="true"
                      >
                        {icono}
                      </svg>
                    </div>

                    <span className="admin-card-badge admin-card-badge--soon">
                      En desarrollo
                    </span>
                  </div>

                  <h3 className="admin-card-title">
                    {modulo.titulo}
                  </h3>

                  <p className="admin-card-desc">
                    {modulo.descripcion}
                  </p>

                  <span className="admin-card-historias">
                    {modulo.historias}
                  </span>
                </div>

                <button
                  type="button"
                  className="admin-card-btn-disabled"
                  style={{
                    cursor: 'pointer',
                    border: 'none',
                    width: '100%',
                    font: 'inherit',
                  }}
                  onClick={() => abrirModulo(modulo)}
                >
                  Conocer módulo &rarr;
                </button>
              </article>
            ))}
          </div>
        </section>

        <footer className="admin-dash-footer">
          Tura Limpia &copy; {new Date().getFullYear()} &mdash;
          Universidad del Pacífico &amp; Pazífico Limpio S.A.S. E.S.P.
        </footer>
      </main>
    </div>
  )
}

export default AdminDashboardPage
