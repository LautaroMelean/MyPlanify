import { useState, useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import { ChevronUp } from 'lucide-react'
import Navbar from './Navbar'
import BottomNav from './BottomNav'

export default function MainLayout() {
  const [showBackToTop, setShowBackToTop] = useState(false)

  useEffect(() => {
    const onScroll = () => setShowBackToTop(window.scrollY > 400)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <div className="min-h-screen flex flex-col relative">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary-600 focus:text-white focus:rounded-lg focus:text-sm focus:font-medium focus:shadow-neon-sm"
      >
        Ir al contenido principal
      </a>
      <Navbar />
      {/* pb-20 on mobile so content isn't hidden behind the bottom nav */}
      <main id="main-content" className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8 page-enter">
        <Outlet />
      </main>

      <BottomNav />

      {/* Back to top — positioned above bottom nav on mobile */}
      {showBackToTop && (
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          aria-label="Volver arriba"
          className="fixed bottom-20 right-4 md:bottom-6 md:right-6 z-40 p-3 bg-primary-600/90 text-white rounded-full shadow-neon hover:bg-primary-700 hover:shadow-neon transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40 backdrop-blur-sm"
        >
          <ChevronUp className="h-5 w-5" aria-hidden="true" />
        </button>
      )}
    </div>
  )
}
