import { screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import { InspireFeed } from '../../components/InspireFeed'

vi.mock('@/hooks/usePlanner', () => ({
  useTrendingPlans: vi.fn(),
  useClonePlan: () => ({ mutate: vi.fn(), isPending: false }),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return { ...actual, useNavigate: () => vi.fn() }
})

import { useTrendingPlans } from '@/hooks/usePlanner'

describe('InspireFeed', () => {
  it('shows empty state when no trending plans', () => {
    ;(useTrendingPlans as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [],
      isLoading: false,
    })
    renderWithProviders(<InspireFeed />)
    expect(screen.getByText(/todavía no hay planes populares/i)).toBeInTheDocument()
  })

  it('shows trending plan cards when data exists', () => {
    ;(useTrendingPlans as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [
        {
          id: 'p1',
          title: 'Plan Verano',
          city: 'Mendoza',
          date: '2026-07-15',
          slug: 'plan-verano-abc',
          item_count: 2,
          view_count: 5,
          share_count: 1,
        },
      ],
      isLoading: false,
    })
    renderWithProviders(<InspireFeed />)
    expect(screen.getByText('Plan Verano')).toBeInTheDocument()
  })

  it('shows loading state', () => {
    ;(useTrendingPlans as ReturnType<typeof vi.fn>).mockReturnValue({
      data: [],
      isLoading: true,
    })
    renderWithProviders(<InspireFeed />)
    expect(screen.getByText(/cargando planes populares/i)).toBeInTheDocument()
  })
})
