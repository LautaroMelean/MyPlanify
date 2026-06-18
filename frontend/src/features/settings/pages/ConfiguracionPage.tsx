import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Settings, Lock, AlertTriangle } from 'lucide-react'
import apiClient from '@/lib/axios'
import Card from '@/components/ui/Card'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'

const passwordSchema = z
  .object({
    old_password: z.string().min(1, 'Ingresá tu contraseña actual'),
    new_password: z.string().min(8, 'La nueva contraseña debe tener al menos 8 caracteres'),
    new_password_confirm: z.string(),
  })
  .refine((d) => d.new_password === d.new_password_confirm, {
    message: 'Las contraseñas no coinciden',
    path: ['new_password_confirm'],
  })

type PasswordForm = z.infer<typeof passwordSchema>

export default function ConfiguracionPage() {
  const [success, setSuccess] = useState(false)
  const [apiError, setApiError] = useState('')

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<PasswordForm>({ resolver: zodResolver(passwordSchema) })

  const onSubmit = async (data: PasswordForm) => {
    setApiError('')
    setSuccess(false)
    try {
      await apiClient.post('/users/me/change-password/', data)
      setSuccess(true)
      reset()
    } catch (err: any) {
      setApiError(
        err?.response?.data?.error?.message ?? 'Error al cambiar la contraseña. Verificá tu contraseña actual.',
      )
    }
  }

  return (
    <div className="max-w-2xl mx-auto flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1 flex items-center gap-2">
          <Settings className="h-6 w-6 text-primary-600" />
          Configuración
        </h1>
        <p className="text-gray-500 text-sm">Ajustá las opciones de tu cuenta.</p>
      </div>

      {/* Cambiar contraseña */}
      <Card>
        <div className="flex items-center gap-3 mb-5">
          <div className="bg-primary-500/10 p-2 rounded-lg">
            <Lock className="h-5 w-5 text-primary-600" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-800">Cambiar contraseña</h2>
            <p className="text-xs text-gray-500">Usá una contraseña segura de al menos 8 caracteres.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
          <Input
            label="Contraseña actual"
            type="password"
            autoComplete="current-password"
            error={errors.old_password?.message}
            {...register('old_password')}
          />
          <Input
            label="Nueva contraseña"
            type="password"
            autoComplete="new-password"
            error={errors.new_password?.message}
            {...register('new_password')}
          />
          <Input
            label="Confirmar nueva contraseña"
            type="password"
            autoComplete="new-password"
            error={errors.new_password_confirm?.message}
            {...register('new_password_confirm')}
          />

          {apiError && (
            <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 rounded-lg p-3">
              <AlertTriangle className="h-4 w-4 flex-shrink-0" />
              {apiError}
            </div>
          )}

          {success && (
            <div className="text-green-400 text-sm bg-green-500/10 rounded-lg p-3">
              Contraseña cambiada correctamente.
            </div>
          )}

          <Button type="submit" isLoading={isSubmitting} className="self-start">
            Cambiar contraseña
          </Button>
        </form>
      </Card>

      {/* Info de cuenta */}
      <Card>
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-red-500/10 p-2 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-500" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-800">Zona de peligro</h2>
            <p className="text-xs text-gray-500">Acciones irreversibles sobre tu cuenta.</p>
          </div>
        </div>
        <Button variant="danger" size="sm" disabled>
          Eliminar cuenta (próximamente)
        </Button>
      </Card>
    </div>
  )
}
