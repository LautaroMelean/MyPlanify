import { Loader2 } from 'lucide-react'

interface LoadingProps {
  message?: string
  fullPage?: boolean
}

export default function Loading({ message = 'Cargando...', fullPage = false }: LoadingProps) {
  if (fullPage) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-50/90 z-40 backdrop-blur-sm">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
          <p className="text-sm text-gray-600">{message}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-center justify-center p-8">
      <div className="flex flex-col items-center gap-3">
        <Loader2 className="h-6 w-6 animate-spin text-primary-600" />
        <p className="text-sm text-gray-500">{message}</p>
      </div>
    </div>
  )
}
