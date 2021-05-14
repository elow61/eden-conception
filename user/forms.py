from django.contrib.auth.forms import UserCreationForm
from user.models import User


class UserCreationFormInherit(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        new_fields = ('first_name', 'last_name', 'email')
        fields = UserCreationForm.Meta.fields + new_fields
