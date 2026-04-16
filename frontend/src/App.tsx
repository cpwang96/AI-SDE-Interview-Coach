import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import CodingSession from './pages/CodingSession'
import SystemDesignSession from './pages/SystemDesignSession'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/coding" element={<CodingSession />} />
      <Route path="/system-design" element={<SystemDesignSession />} />
    </Routes>
  )
}
