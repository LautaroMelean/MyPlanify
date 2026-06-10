import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useRegister } from '@/hooks/useAuth'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'

const registerSchema = z
  .object({
    email: z.string().email('Ingresá un correo electrónico válido'),
    first_name: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
    last_name: z.string().min(2, 'El apellido debe tener al menos 2 caracteres'),
    password: z.string().min(8, 'La contraseña debe tener al menos 8 caracteres'),
    password_confirm: z.string(),
  })
  .refine((d) => d.password === d.password_confirm, {
    message: 'Las contraseñas no coinciden',
    path: ['password_confirm'],
  })

type RegisterForm = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const register_ = useRegister()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({ resolver: zodResolver(registerSchema) })

  const onSubmit = (data: RegisterForm) => register_.mutate(data)

  return (
    <Card className="w-full max-w-sm">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Crear cuenta</h1>
      <p className="text-sm text-gray-500 mb-6">Empezá a descubrir planes con Planify</p>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
        <div className="flex gap-3">
          <Input label="Nombre" error={errors.first_name?.message} {...register('first_name')} />
          <Input label="Apellido" error={errors.last_name?.message} {...register('last_name')} />
        </div>
        <Input label="Correo electrónico" type="email" autoComplete="email" error={errors.email?.message} {...register('email')} />
        <Input
          label="Contraseña"
          type="password"
          autoComplete="new-password"
          error={errors.password?.message}
          {...register('password')}
        />
        <Input
          label="Confirmar contraseña"
          type="password"
          autoComplete="new-password"
          error={errors.password_confirm?.message}
          {...register('password_confirm')}
        />

        {register_.isError && (
          <p className="text-sm text-red-600 text-center">
            {(register_.error as any)?.response?.data?.error?.message ?? 'Error al registrarse. Intentá de nuevo.'}
          </p>
        )}

        <Button type="submit" isLoading={register_.isPending} className="w-full mt-2">
          Crear cuenta
        </Button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-500">
        ¿Ya tenés cuenta?{' '}
        <Link to="/login" className="text-primary-600 font-medium hover:underline">
          Ingresar
        </Link>
      </p>
    </Card>
  )
}
