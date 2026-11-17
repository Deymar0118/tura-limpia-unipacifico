import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './modules/landing/pages/LandingPage'
import AuthPage from './modules/auth/pages/AuthPage'
import UsersManagementPage from './modules/admin/pages/UsersManagementPage'
import AdminDashboardPage from './modules/admin/pages/AdminDashboardPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>      
        <Route path="/login" element={<AuthPage initialTab="login" />} />
        <Route path="/registro" element={<AuthPage initialTab="registro" />} />
        <Route path="/dashboard" element={<AdminDashboardPage />} />
        <Route path="/admin" element={<AdminDashboardPage />} />
        <Route path="/admin/usuarios" element={<UsersManagementPage />} />
        <Route path="/usuarios" element={<UsersManagementPage />} />
        <Route path="*" element={<LandingPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App