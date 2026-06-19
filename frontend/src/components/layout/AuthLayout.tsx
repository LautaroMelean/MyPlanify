import { Outlet, Link } from 'react-router-dom'
import { MapPin } from 'lucide-react'

export default function AuthLayout() {
  return (
    <div className="min-h-screen relative flex flex-col items-center justify-center px-4 py-12 overflow-hidden">
      {/* Decorative background orbs */}
      <div className="pointer-events-none absolute -top-32 -left-32 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" aria-hidden="true" />
      <div className="pointer-events-none absolute -bottom-32 -right-32 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl" aria-hidden="true" />

      <div className="relative z-10 flex flex-col items-center w-full">
        <Link to="/" className="flex items-center gap-2 font-bold text-2xl mb-2 neon-text">
          <MapPin className="h-7 w-7 text-primary-600" />
          Planify
        </Link>
        <p className="text-sm text-gray-500 mb-8">Planeá tu próxima salida en segundos</p>
        <Outlet />
      </div>
    </div>
  )
}
