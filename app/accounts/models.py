from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class UserManage(UserManager):
	@staticmethod
	def update_user(user, cleaned_data):
		user_fields = ['username', 'first_name', 'last_name', 'email', 'password']
		user = User.objects.get(id=user.id)

		if User.objects.filter(username=cleaned_data.get('username', False)).exists():
			return None

		fields_to_update = {'user': []}

		for key in user_fields:
			value = cleaned_data.get(key, False)
			if value:
				fields_to_update['user'].append(key)
				setattr(user, key, value)

		user.save(update_fields=fields_to_update['user'])

		return user


class User(AbstractUser):
	objects = UserManage()
	avatar = models.ImageField(upload_to=f'accounts/static/avatars/', null=True, blank=True)

	def __str__(self):
		return self.username
