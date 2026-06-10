import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { remindersService } from '@/services/remindersService'

export function useReminders() {
  return useQuery({
    queryKey: ['reminders'],
    queryFn: remindersService.list,
  })
}

export function useCreateReminder() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ eventId, reminderDate }: { eventId: string; reminderDate: string }) =>
      remindersService.create(eventId, reminderDate),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['reminders'] })
      qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })
}

export function useRemoveReminder() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => remindersService.remove(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['reminders'] }),
  })
}
