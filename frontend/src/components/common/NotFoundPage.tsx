import { useNavigate } from 'react-router-dom'
import { MapPin } from 'lucide-react'
import Button from '@/components/ui/Button'

export default function NotFoundPage() {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center">
      <MapPin className="h-16 w-16 text-primary-400 mb-4" />
      <h1 className="text-4xl font-bold text-gray-800 mb-2">404</h1>
      <p className="text-lg text-gray-500 mb-6">Página no encontrada</p>
      <Button onClick={() => navigate('/')}>Ir al inicio</Button>
    </div>
  )
}
