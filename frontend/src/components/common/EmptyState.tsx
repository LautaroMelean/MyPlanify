import { SearchX } from 'lucide-react'
import Button from '@/components/ui/Button'

interface EmptyStateProps {
  title?: string
  description?: string
  icon?: React.ReactNode
  action?: {
    label: string
    onClick: () => void
  }
}

export default function EmptyState({
  title = 'Sin resultados',
  description = 'Intentá ajustar tu búsqueda o filtros.',
  icon,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="mb-4 p-4 bg-gray-300/5 rounded-2xl border border-gray-200/20 text-gray-400" aria-hidden="true">
        {icon ?? <SearchX className="h-12 w-12" />}
      </div>
      <h3 className="text-lg font-semibold text-gray-800 mb-1">{title}</h3>
      <p className="text-sm text-gray-500 max-w-sm">{description}</p>
      {action && (
        <Button className="mt-4" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  )
}
