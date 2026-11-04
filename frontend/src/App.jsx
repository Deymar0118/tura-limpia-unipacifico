import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './modules/landing/pages/LandingPage'
import LoginPage from './modules/auth/pages/LoginPage'
import RegisterPage from './modules/auth/pages/RegisterPage'
import AuthPage from './modules/auth/pages/AuthPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>      
        <Route path="/login" element={<AuthPage initialTab="login" />} />
        <Route path="*" element={<LandingPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

