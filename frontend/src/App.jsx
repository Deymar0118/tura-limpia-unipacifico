import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

import LandingPage from './modules/landing/pages/LandingPage'
import AuthPage from './modules/auth/pages/AuthPage'
import UsersManagementPage from './modules/admin/pages/UsersManagementPage'
import AdminDashboardPage from './modules/admin/pages/AdminDashboardPage'
import ConstructionPage from './modules/construction/pages/ConstructionPage'

import { getSession } from './app/session'
import { getAccessToken } from './shared/api/apiClient'

// Protección de las rutas administrativas
function AdminRoute({ children }) {
  const token = getAccessToken()
  const session = getSession()

  // Si no existe una sesión autenticada, ir al login
  if (!token || !session) {
    return <Navigate to="/login" replace />
  }

  // Solo los administradores pueden entrar
  if (session.rol?.toLowerCase() !== 'admin') {
    return <Navigate to="/construccion" replace />
  }

  return children
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Autenticación */}
        <Route
          path="/login"
          element={<AuthPage initialTab="login" />}
        />

        <Route
          path="/registro"
          element={<AuthPage initialTab="registro" />}
        />

        {/* Módulos administrativos protegidos */}
        <Route
          path="/dashboard"
          element={
            <AdminRoute>
              <AdminDashboardPage />
            </AdminRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminDashboardPage />
            </AdminRoute>
          }
        />

        <Route
          path="/admin/usuarios"
          element={
            <AdminRoute>
              <UsersManagementPage />
            </AdminRoute>
          }
        />

        <Route
          path="/usuarios"
          element={
            <AdminRoute>
              <UsersManagementPage />
            </AdminRoute>
          }
        />

        {/* Ruta para módulos en desarrollo */}
        <Route
          path="/construccion"
          element={<ConstructionPage />}
        />

        {/* Página principal */}
        <Route path="/" element={<LandingPage />} />

        {/* Redirección de rutas desconocidas */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
