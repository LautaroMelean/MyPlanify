import type { Plan, PlanItem, PlanSlot } from '@/types'
import { PlanItemCard } from './PlanItemCard'
import { SlotBadge } from './SlotBadge'

const SLOTS: PlanSlot[] = ['morning', 'afternoon', 'evening']

const SLOT_LABELS: Record<PlanSlot, string> = {
  morning: 'Mañana',
  afternoon: 'Tarde',
  evening: 'Noche',
}

interface Props {
  plan: Plan
  onRemoveItem?: (itemId: string) => void
  onFeedbackItem?: (item: PlanItem) => void
  onSaveNote?: (itemId: string, note: string) => void
  onReorderItem?: (itemId: string, direction: 'up' | 'down') => void
  readonly?: boolean
}

export function ItineraryView({ plan, onRemoveItem, onFeedbackItem, onSaveNote, onReorderItem, readonly = false }: Props) {
  return (
    <div className="space-y-6">
      {SLOTS.map((slot) => {
        const items = plan.items.filter((i) => i.slot === slot)

        return (
          <div key={slot}>
            <div className="flex items-center gap-2 mb-3">
              <SlotBadge slot={slot} />
              <h3 className="text-sm font-semibold text-gray-600">{SLOT_LABELS[slot]}</h3>
            </div>

            {items.length === 0 ? (
              <div className="border border-dashed border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-400">
                Sin actividades para este horario
              </div>
            ) : (
              <div className="space-y-2">
                {items.map((item) => (
                  <PlanItemCard
                    key={item.id}
                    item={item}
                    onRemove={onRemoveItem}
                    onFeedback={onFeedbackItem}
                    onSaveNote={onSaveNote}
                    onReorder={onReorderItem}
                    readonly={readonly}
                  />
                ))}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
