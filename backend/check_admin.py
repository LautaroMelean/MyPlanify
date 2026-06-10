from apps.users.models import User
u = User.objects.filter(email="admin@planify.com").first()
print("Exists:", bool(u))
if u:
    print("PwdOK:", u.check_password("admin123"))
    print("Active:", u.is_active)
