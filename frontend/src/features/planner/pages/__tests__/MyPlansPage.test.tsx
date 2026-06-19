import { screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import MyPlansPage from '../MyPlansPage'
import * as usePlannerModule from '@/hooks/usePlanner'
import type { Plan } from '@/types'

vi.mock('@/hooks/usePlanner')

const makePlan = (id: string, title: string): Plan => ({
  id,
  title,
  date: '2026-07-01',
  budget: '5000',
  people_count: 2,
  city: 'Buenos Aires',
  slug: `plan-${id}`,
  is_public: false,
  status: 'generated',
  items: [],
  created_at: '2026-07-01T10:00:00Z',
  updated_at: '2026-07-01T10:00:00Z',
})

beforeEach(() => {
  vi.mocked(usePlannerModule.useDeletePlan).mockReturnValue({
    mutate: vi.fn(),
    isPending: false,
  } as unknown as ReturnType<typeof usePlannerModule.useDeletePlan>)
})

describe('MyPlansPage', () => {
  afterEach(() => vi.clearAllMocks())

  it('shows loading state', () => {
    vi.mocked(usePlannerModule.useMyPlans).mockReturnValue({
      data: undefined,
      isLoading: true,
    } as unknown as ReturnType<typeof usePlannerModule.useMyPlans>)

    renderWithProviders(<MyPlansPage />)
    expect(screen.getByTestId('plans-skeleton')).toBeInTheDocument()
  })

  it('shows list of plans', async () => {
    vi.mocked(usePlannerModule.useMyPlans).mockReturnValue({
      data: [makePlan('1', 'Plan para 01/07/2026'), makePlan('2', 'Plan para 15/08/2026')],
      isLoading: false,
    } as unknown as ReturnType<typeof usePlannerModule.useMyPlans>)

    renderWithProviders(<MyPlansPage />)
    await waitFor(() => {
      expect(screen.getByText('Plan para 01/07/2026')).toBeInTheDocument()
      expect(screen.getByText('Plan para 15/08/2026')).toBeInTheDocument()
    })
  })

  it('shows empty state when no plans', async () => {
    vi.mocked(usePlannerModule.useMyPlans).mockReturnValue({
      data: [],
      isLoading: false,
    } as unknown as ReturnType<typeof usePlannerModule.useMyPlans>)

    renderWithProviders(<MyPlansPage />)
    await waitFor(() => {
      expect(screen.getByText(/Todavía no tenés planes/i)).toBeInTheDocument()
    })
  })
})
