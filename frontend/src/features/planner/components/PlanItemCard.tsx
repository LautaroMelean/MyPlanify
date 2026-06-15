import { useState, useRef, useEffect } from 'react'
import { X, Star, ChevronUp, ChevronDown } from 'lucide-react'
import type { PlanItem } from '@/types'
import { SlotBadge } from './SlotBadge'

interface Props {
  item: PlanItem
  onRemove?: (itemId: string) => void
  onFeedback?: (item: PlanItem) => void
  onSaveNote?: (itemId: string, note: string) => void
  onReorder?: (itemId: string, direction: 'up' | 'down') => void
  readonly?: boolean
}

const ENTITY_LABELS: Record<string, string> = {
  place: 'Lugar',
  activity: 'Actividad',
  event: 'Evento',
}

export function PlanItemCard({ item, onRemove, onFeedback, onSaveNote, onReorder, readonly = false }: Props) {
  const [editingNote, setEditingNote] = useState(false)
  const [noteValue, setNoteValue] = useState(item.note)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (editingNote && inputRef.current) {
      inputRef.current.focus()
    }
  }, [editingNote])

  const handleNoteKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      commitNote()
    } else if (e.key === 'Escape') {
      setNoteValue(item.note)
      setEditingNote(false)
    }
  }

  const commitNote = () => {
    setEditingNote(false)
    if (noteValue !== item.note && onSaveNote) {
      onSaveNote(item.id, noteValue)
    }
  }

  return (
    <div className="flex items-start gap-3 p-3 bg-white border border-gray-200 rounded-lg shadow-sm group">
      {/* Reorder buttons */}
      {onReorder && (
        <div className="flex flex-col gap-0.5 pt-0.5 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
          <button
            onClick={() => onReorder(item.id, 'up')}
            className="p-0.5 text-gray-300 hover:text-gray-600 transition-colors"
            aria-label="Mover arriba"
          >
            <ChevronUp className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => onReorder(item.id, 'down')}
            className="p-0.5 text-gray-300 hover:text-gray-600 transition-colors"
            aria-label="Mover abajo"
          >
            <ChevronDown className="h-3.5 w-3.5" />
          </button>
        </div>
      )}

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <SlotBadge slot={item.slot} />
          <span className="text-xs text-gray-400 capitalize">
            {ENTITY_LABELS[item.entity_type] || item.entity_type}
          </span>
        </div>

        {item.generation_reason && (
          <p className="text-xs text-gray-500 italic mt-1">{item.generation_reason}</p>
        )}

        {/* Inline note edit */}
        {editingNote ? (
          <input
            ref={inputRef}
            value={noteValue}
            onChange={(e) => setNoteValue(e.target.value)}
            onKeyDown={handleNoteKeyDown}
            onBlur={commitNote}
            placeholder="Agregar nota..."
            className="mt-1 w-full text-sm border-b border-primary-300 focus:outline-none bg-transparent pb-0.5"
          />
        ) : (
          <div
            onClick={() => !readonly && onSaveNote && setEditingNote(true)}
            className={`mt-1 text-sm min-h-[1rem] ${
              !readonly && onSaveNote
                ? 'cursor-text hover:text-primary-600 transition-colors'
                : ''
            } ${item.note ? 'text-gray-700' : 'text-gray-300 italic'}`}
          >
            {item.note || (!readonly && onSaveNote ? 'Agregar nota...' : '')}
          </div>
        )}
      </div>

      <div className="flex items-center gap-1 flex-shrink-0">
        {onFeedback && (
          <button
            onClick={() => onFeedback(item)}
            className="p-1 text-gray-400 hover:text-yellow-500 transition-colors"
            aria-label="Calificar ítem"
            title="Dar feedback"
          >
            <Star className="h-4 w-4" />
          </button>
        )}
        {!readonly && onRemove && (
          <button
            onClick={() => onRemove(item.id)}
            className="p-1 text-gray-400 hover:text-red-500 transition-colors"
            aria-label="Quitar ítem"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
    </div>
  )
}
