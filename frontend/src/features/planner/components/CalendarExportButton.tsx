import { useState } from 'react'
import { Calendar, ChevronDown, Download, ExternalLink } from 'lucide-react'
import type { Plan, PlanItem, PlanSlot } from '@/types'

const SLOT_TIMES: Record<PlanSlot, { start: string; end: string }> = {
  morning: { start: '09:00', end: '11:00' },
  afternoon: { start: '14:00', end: '16:00' },
  evening: { start: '20:00', end: '22:00' },
}

function formatIcsDate(date: string, time: string): string {
  return `${date.replace(/-/g, '')}T${time.replace(':', '')}00`
}

function generateIcs(plan: Plan): string {
  const lines: string[] = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Planify//ES',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
  ]

  plan.items.forEach((item: PlanItem) => {
    const times = SLOT_TIMES[item.slot]
    const dtstart = formatIcsDate(plan.date, times.start)
    const dtend = formatIcsDate(plan.date, times.end)
    const uid = `${plan.id}-${item.id}@planify`
    const summary = `Planify: ${item.entity_type} (${item.slot})`
    const description = item.generation_reason.replace(/\n/g, '\\n') || 'Plan generado con Planify'

    lines.push(
      'BEGIN:VEVENT',
      `UID:${uid}`,
      `DTSTART:${dtstart}`,
      `DTEND:${dtend}`,
      `SUMMARY:${summary}`,
      `DESCRIPTION:${description}`,
      'END:VEVENT'
    )
  })

  lines.push('END:VCALENDAR')
  return lines.join('\r\n')
}

function googleCalendarUrl(plan: Plan, item: PlanItem): string {
  const times = SLOT_TIMES[item.slot]
  const dateStr = plan.date.replace(/-/g, '')
  const dates = `${dateStr}T${times.start.replace(':', '')}00/${dateStr}T${times.end.replace(':', '')}00`
  const text = encodeURIComponent(`Planify: ${item.entity_type}`)
  const details = encodeURIComponent(item.generation_reason || 'Plan generado con Planify')
  return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${text}&dates=${dates}&details=${details}`
}

interface Props {
  plan: Plan
}

export function CalendarExportButton({ plan }: Props) {
  const [open, setOpen] = useState(false)

  const handleDownloadIcs = () => {
    const ics = generateIcs(plan)
    const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `plan-${plan.slug}.ics`
    a.click()
    URL.revokeObjectURL(url)
    setOpen(false)
  }

  const handleGoogleCalendar = () => {
    if (plan.items.length === 0) return
    // Open first item; user can repeat for others
    const url = googleCalendarUrl(plan, plan.items[0])
    window.open(url, '_blank', 'noopener,noreferrer')
    setOpen(false)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 border border-gray-200 rounded-lg hover:bg-white/5 hover:text-gray-800 transition-colors"
      >
        <Calendar className="h-4 w-4" />
        Exportar
        <ChevronDown className="h-3 w-3" />
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute right-0 mt-1 w-52 bg-white border border-white/10 rounded-xl shadow-glass z-20 py-1">
            <button
              onClick={handleDownloadIcs}
              className="flex items-center gap-2 w-full px-4 py-2 text-sm text-gray-600 hover:bg-white/5 hover:text-gray-800"
            >
              <Download className="h-4 w-4 text-gray-400" />
              Descargar .ics
            </button>
            <button
              onClick={handleGoogleCalendar}
              className="flex items-center gap-2 w-full px-4 py-2 text-sm text-gray-600 hover:bg-white/5 hover:text-gray-800"
              disabled={plan.items.length === 0}
            >
              <ExternalLink className="h-4 w-4 text-gray-400" />
              Agregar a Google Calendar
            </button>
          </div>
        </>
      )}
    </div>
  )
}
