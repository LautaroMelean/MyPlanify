import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import Button from '@/components/ui/Button'
import { localDateString } from '@/lib/format'

interface Props {
  isOpen: boolean
  onClose: () => void
  onConfirm: (date: string) => void
  isLoading?: boolean
  title?: string
}

export function ClonePlanModal({ isOpen, onClose, onConfirm, isLoading, title = 'Usar como base' }: Props) {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const defaultDate = localDateString(tomorrow)

  const [date, setDate] = useState(defaultDate)

  useEffect(() => {
    if (!isOpen) return
    const handleKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handleKey)
    return () => document.removeEventListener('keydown', handleKey)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleConfirm = () => {
    if (date) onConfirm(date)
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="clone-modal-title"
      onClick={(e) => { if (e.target === e.currentTarget) onClose() }}
    >
      <div className="bg-white rounded-xl shadow-glass border border-white/10 w-full max-w-sm">
        <div className="flex items-center justify-between p-4 border-b border-gray-200/30">
          <h2 id="clone-modal-title" className="text-base font-semibold text-gray-900">{title}</h2>
          <button onClick={onClose} aria-label="Cerrar" className="text-gray-400 hover:text-gray-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40 rounded">
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="p-4">
          <label htmlFor="clone-plan-date" className="block text-sm font-medium text-gray-600 mb-1">
            ¿Para qué fecha querés usar este plan?
          </label>
          <input
            id="clone-plan-date"
            type="date"
            value={date}
            min={defaultDate}
            onChange={(e) => setDate(e.target.value)}
            className="w-full border border-gray-200 bg-gray-100 text-gray-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/40"
          />
        </div>

        <div className="flex gap-2 p-4 pt-0">
          <Button variant="secondary" size="sm" onClick={onClose} className="flex-1">
            Cancelar
          </Button>
          <Button size="sm" onClick={handleConfirm} isLoading={isLoading} disabled={!date} className="flex-1">
            Crear mi plan
          </Button>
        </div>
      </div>
    </div>
  )
}
