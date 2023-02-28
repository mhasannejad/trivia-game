from django.contrib.auth.base_user import BaseUserManager




class UserAccountManager(BaseUserManager):
    def create_user(self, email, name='', password=None):
        if not email:
            return ValueError('no email found ')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            return ValueError('no email found ')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.admin = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user
