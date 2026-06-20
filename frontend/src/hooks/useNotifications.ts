import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { notificationsService } from '@/services/notificationsService'

export function useNotifications() {
  return useQuery({
    queryKey: ['notifications'],
    queryFn: notificationsService.list,
    refetchInterval: 60_000,
  })
}

export function useUnreadCount() {
  const { data = [] } = useNotifications()
  return data.filter((n) => !n.read).length
}

export function useMarkNotificationRead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => notificationsService.markRead(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notifications'] }),
  })
}

export function useMarkAllNotificationsRead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: () => notificationsService.markAllRead(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notifications'] }),
  })
}
