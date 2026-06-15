import { screen, fireEvent } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import { CalendarExportButton } from '../../components/CalendarExportButton'
import type { Plan } from '@/types'

const makePlan = (): Plan => ({
  id: 'plan-cal-1',
  title: 'Plan para 10/07/2026',
  date: '2026-07-10',
  budget: '3000',
  people_count: 1,
  city: 'Buenos Aires',
  slug: 'plan-cal-1-abc',
  is_public: false,
  status: 'generated',
  items: [
    {
      id: 'item-1',
      entity_type: 'activity',
      entity_id: 'ent-1',
      slot: 'morning',
      order: 0,
      note: '',
      generation_reason: 'Actividad de mañana',
      created_at: '2026-07-10T09:00:00Z',
    },
  ],
  created_at: '2026-07-10T08:00:00Z',
  updated_at: '2026-07-10T08:00:00Z',
})

describe('CalendarExportButton', () => {
  it('renders the export button', () => {
    renderWithProviders(<CalendarExportButton plan={makePlan()} />)
    expect(screen.getByRole('button', { name: /exportar/i })).toBeInTheDocument()
  })

  it('opens dropdown with two options on click', () => {
    renderWithProviders(<CalendarExportButton plan={makePlan()} />)
    fireEvent.click(screen.getByRole('button', { name: /exportar/i }))
    expect(screen.getByText(/descargar .ics/i)).toBeInTheDocument()
    expect(screen.getByText(/agregar a google calendar/i)).toBeInTheDocument()
  })

  it('closes dropdown when clicking the button again', () => {
    renderWithProviders(<CalendarExportButton plan={makePlan()} />)
    const btn = screen.getByRole('button', { name: /exportar/i })
    fireEvent.click(btn)
    expect(screen.getByText(/descargar .ics/i)).toBeInTheDocument()
    fireEvent.click(btn)
    expect(screen.queryByText(/descargar .ics/i)).not.toBeInTheDocument()
  })
})
