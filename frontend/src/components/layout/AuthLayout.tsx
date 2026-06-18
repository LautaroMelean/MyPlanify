import { Outlet, Link } from 'react-router-dom'
import { MapPin } from 'lucide-react'

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-12">
      <Link to="/" className="flex items-center gap-2 font-bold text-2xl mb-8 neon-text">
        <MapPin className="h-7 w-7 text-primary-600" />
        Planify
      </Link>
      <Outlet />
    </div>
  )
}
