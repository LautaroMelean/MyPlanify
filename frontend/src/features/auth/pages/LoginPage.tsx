import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useLogin } from '@/hooks/useAuth'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'

const loginSchema = z.object({
  email: z.string().email('Ingresá un correo electrónico válido'),
  password: z.string().min(1, 'La contraseña es obligatoria'),
})

type LoginForm = z.infer<typeof loginSchema>

export default function LoginPage() {
  const login = useLogin()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) })

  const onSubmit = (data: LoginForm) => login.mutate(data)

  return (
    <Card className="w-full max-w-sm">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Bienvenido de vuelta</h1>
      <p className="text-sm text-gray-500 mb-6">Iniciá sesión en tu cuenta de Planify</p>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
        <Input
          label="Correo electrónico"
          type="email"
          autoComplete="email"
          error={errors.email?.message}
          {...register('email')}
        />
        <Input
          label="Contraseña"
          type="password"
          autoComplete="current-password"
          error={errors.password?.message}
          {...register('password')}
        />

        {login.isError && (
          <p className="text-sm text-red-600 text-center">
            {(login.error as any)?.response?.data?.error?.message ?? 'Error al ingresar. Intentá de nuevo.'}
          </p>
        )}

        <Button type="submit" isLoading={login.isPending} className="w-full mt-2">
          Ingresar
        </Button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-500">
        ¿No tenés cuenta?{' '}
        <Link to="/register" className="text-primary-600 font-medium hover:underline">
          Registrate
        </Link>
      </p>
    </Card>
  )
}
