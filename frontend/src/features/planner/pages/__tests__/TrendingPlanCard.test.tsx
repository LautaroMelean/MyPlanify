import { screen, fireEvent } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import { TrendingPlanCard } from '../../components/TrendingPlanCard'
import type { TrendingPlan } from '@/types'

const makeTrendingPlan = (overrides: Partial<TrendingPlan> = {}): TrendingPlan => ({
  id: 'plan-trend-1',
  title: 'Plan Cultural Buenos Aires',
  city: 'Buenos Aires',
  date: '2026-07-10',
  slug: 'plan-trend-1-abc',
  item_count: 3,
  view_count: 10,
  share_count: 2,
  ...overrides,
})

describe('TrendingPlanCard', () => {
  it('shows the plan title', () => {
    renderWithProviders(<TrendingPlanCard plan={makeTrendingPlan()} onUseAsBase={vi.fn()} />)
    expect(screen.getByText('Plan Cultural Buenos Aires')).toBeInTheDocument()
  })

  it('shows the city', () => {
    renderWithProviders(<TrendingPlanCard plan={makeTrendingPlan()} onUseAsBase={vi.fn()} />)
    expect(screen.getByText('Buenos Aires')).toBeInTheDocument()
  })

  it('shows the item count', () => {
    renderWithProviders(<TrendingPlanCard plan={makeTrendingPlan()} onUseAsBase={vi.fn()} />)
    expect(screen.getByText(/3 ítems/i)).toBeInTheDocument()
  })

  it('calls onUseAsBase when button is clicked', () => {
    const onUseAsBase = vi.fn()
    const plan = makeTrendingPlan()
    renderWithProviders(<TrendingPlanCard plan={plan} onUseAsBase={onUseAsBase} />)
    fireEvent.click(screen.getByRole('button', { name: /usar como base/i }))
    expect(onUseAsBase).toHaveBeenCalledWith(plan)
  })
})
