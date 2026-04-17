import { Routes, Route, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Onboarding from './pages/Onboarding'
import Assessment from './pages/Assessment'
import CodingSession from './pages/CodingSession'
import SystemDesignSession from './pages/SystemDesignSession'
import StudyPlan from './pages/StudyPlan'

// Wrapper that forces a full remount of CodingSession whenever the question ID
// changes (React Router reuses the same component instance across query-param
// navigation, so without a key the useEffect init never re-fires).
function CodingRoute() {
  const { search } = useLocation()
  return <CodingSession key={search} />
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/assessment" element={<Assessment />} />
      <Route path="/coding" element={<CodingRoute />} />
      <Route path="/system-design" element={<SystemDesignSession />} />
      <Route path="/study" element={<StudyPlan />} />
    </Routes>
  )
}
