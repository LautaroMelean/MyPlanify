import { useNavigate } from 'react-router-dom'
import { MapPin, Home, Search } from 'lucide-react'
import Button from '@/components/ui/Button'

export default function NotFoundPage() {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center">
      <div className="mb-6 relative">
        <div className="absolute inset-0 rounded-full bg-primary-500/20 blur-2xl scale-150" />
        <div className="relative p-5 bg-primary-500/10 rounded-2xl border border-primary-400/20">
          <MapPin className="h-14 w-14 text-primary-500" />
        </div>
      </div>

      <p className="text-6xl font-black neon-text mb-3">404</p>
      <h1 className="text-xl font-semibold text-gray-800 mb-2">Página no encontrada</h1>
      <p className="text-sm text-gray-500 max-w-xs mb-8">
        No pudimos encontrar lo que buscás. Puede que la URL esté mal escrita o que la página ya no exista.
      </p>

      <div className="flex flex-wrap gap-3 justify-center">
        <Button onClick={() => navigate('/')} leftIcon={<Home className="h-4 w-4" />}>
          Ir al inicio
        </Button>
        <Button variant="secondary" onClick={() => navigate('/explorar')} leftIcon={<Search className="h-4 w-4" />}>
          Explorar
        </Button>
      </div>
    </div>
  )
}
