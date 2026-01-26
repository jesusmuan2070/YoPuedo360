/**
 * YoPuedo360 - Main App Component
 */

import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { StatsProvider } from './context/StatsContext';
import LandingPage from './pages/LandingPage';
import OnboardingPage from './pages/OnboardingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MascotSelectPage from './pages/MascotSelectPage';
import WorldMapPage from './pages/WorldMapPage';
import ScenarioPage from './pages/ScenarioPage';
import LessonPage from './pages/LessonPage';
import MascotBuddy from './components/game/MascotBuddy';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <StatsProvider>
        <Router>
          <Routes>
            {/* Landing */}
            <Route path="/" element={<LandingPage />} />

            {/* Onboarding Flow */}
            <Route path="/onboarding" element={<OnboardingPage />} />

            {/* Auth */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Mascot Selection (after signup) */}
            <Route path="/select-mascot" element={<MascotSelectPage />} />

            {/* Main Game */}
            <Route path="/world" element={<WorldMapPage />} />
            <Route path="/scenario/:slug" element={<ScenarioPage />} />
            <Route path="/lesson/:milestoneId" element={<LessonPage />} />

            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </StatsProvider>
    </AuthProvider>
  );
}

export default App;
