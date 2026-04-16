import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Onboarding from './pages/Onboarding'
import Assessment from './pages/Assessment'
import CodingSession from './pages/CodingSession'
import SystemDesignSession from './pages/SystemDesignSession'
import StudyPlan from './pages/StudyPlan'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/assessment" element={<Assessment />} />
      <Route path="/coding" element={<CodingSession />} />
      <Route path="/system-design" element={<SystemDesignSession />} />
      <Route path="/study" element={<StudyPlan />} />
    </Routes>
  )
}
