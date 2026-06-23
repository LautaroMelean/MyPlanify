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
      <div
        className="mb-5 p-5 bg-gradient-to-br from-primary-500/8 to-primary-500/4 rounded-3xl border border-primary-400/15 text-gray-400 shadow-glass-sm"
        aria-hidden="true"
      >
        {icon ?? <SearchX className="h-12 w-12 text-gray-300" />}
      </div>
      <h3 className="text-base font-semibold text-gray-800 mb-1.5">{title}</h3>
      <p className="text-sm text-gray-500 max-w-xs leading-relaxed">{description}</p>
      {action && (
        <Button className="mt-5" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  )
}
