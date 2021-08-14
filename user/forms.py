''' Forms to the user application '''
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class UserCreationFormInherit(UserCreationForm):
    ''' Inherit the form class to create a user '''

    class Meta(UserCreationForm.Meta):
        ''' Add the new fields create in the inherit model user
            to the form for create a user.
        '''
        model = User
        new_fields = ('first_name', 'last_name', 'email', 'image')
        fields = UserCreationForm.Meta.fields + new_fields
