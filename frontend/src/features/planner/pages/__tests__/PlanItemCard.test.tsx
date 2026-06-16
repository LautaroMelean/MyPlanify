import { screen, fireEvent } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import { PlanItemCard } from '../../components/PlanItemCard'
import type { PlanItem } from '@/types'

const makeItem = (overrides: Partial<PlanItem> = {}): PlanItem => ({
  id: 'item-1',
  entity_type: 'activity',
  entity_id: 'ent-1',
  entity_name: 'Visita al MALBA',
  entity_description: 'Recorrido por el museo.',
  entity_category: 'Museo',
  slot: 'morning',
  order: 0,
  note: '',
  generation_reason: 'Coincide con tus preferencias.',
  created_at: '2026-07-01T10:00:00Z',
  ...overrides,
})

describe('PlanItemCard', () => {
  it('shows generation reason', () => {
    renderWithProviders(<PlanItemCard item={makeItem()} />)
    expect(screen.getByText('Coincide con tus preferencias.')).toBeInTheDocument()
  })

  it('shows reorder buttons when onReorder is provided', () => {
    renderWithProviders(<PlanItemCard item={makeItem()} onReorder={vi.fn()} />)
    expect(screen.getByLabelText('Mover arriba')).toBeInTheDocument()
    expect(screen.getByLabelText('Mover abajo')).toBeInTheDocument()
  })

  it('does not show reorder buttons without onReorder', () => {
    renderWithProviders(<PlanItemCard item={makeItem()} />)
    expect(screen.queryByLabelText('Mover arriba')).not.toBeInTheDocument()
  })

  it('calls onReorder with up direction when up button clicked', () => {
    const onReorder = vi.fn()
    renderWithProviders(<PlanItemCard item={makeItem()} onReorder={onReorder} />)
    fireEvent.click(screen.getByLabelText('Mover arriba'))
    expect(onReorder).toHaveBeenCalledWith('item-1', 'up')
  })

  it('calls onReorder with down direction when down button clicked', () => {
    const onReorder = vi.fn()
    renderWithProviders(<PlanItemCard item={makeItem()} onReorder={onReorder} />)
    fireEvent.click(screen.getByLabelText('Mover abajo'))
    expect(onReorder).toHaveBeenCalledWith('item-1', 'down')
  })

  it('enters edit mode when note placeholder is clicked', () => {
    const onSaveNote = vi.fn()
    renderWithProviders(<PlanItemCard item={makeItem()} onSaveNote={onSaveNote} />)
    fireEvent.click(screen.getByText(/agregar nota/i))
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('calls onSaveNote with new value when Enter is pressed', () => {
    const onSaveNote = vi.fn()
    renderWithProviders(<PlanItemCard item={makeItem()} onSaveNote={onSaveNote} />)
    fireEvent.click(screen.getByText(/agregar nota/i))
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'Mi nota nueva' } })
    fireEvent.keyDown(input, { key: 'Enter' })
    expect(onSaveNote).toHaveBeenCalledWith('item-1', 'Mi nota nueva')
  })

  it('cancels edit without saving when Escape is pressed', () => {
    const onSaveNote = vi.fn()
    renderWithProviders(<PlanItemCard item={makeItem()} onSaveNote={onSaveNote} />)
    fireEvent.click(screen.getByText(/agregar nota/i))
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'No guardar esto' } })
    fireEvent.keyDown(input, { key: 'Escape' })
    expect(onSaveNote).not.toHaveBeenCalled()
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
  })
})
