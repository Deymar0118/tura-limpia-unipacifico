import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './modules/landing/pages/LandingPage'
import LoginPage from './modules/auth/pages/LoginPage'
import RegisterPage from './modules/auth/pages/RegisterPage'
import ForgotPasswordPage from './modules/auth/pages/ForgotPasswordPage'
import ResetPasswordPage from './modules/auth/pages/ResetPasswordPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/registro" element={<RegisterPage />} />
        <Route path="/recuperar-contrasena" element={<ForgotPasswordPage />} />
        <Route path="/restablecer-contrasena" element={<ResetPasswordPage />} />
        <Route path="*" element={<LandingPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
