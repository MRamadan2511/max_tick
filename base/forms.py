# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, UserType, Ticket, Comment



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['order_id', 'description', 'post_image',]



class AgentLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        try:
            agent_type = UserType.objects.get(type='Agent')
            user = User.objects.get(email=username, user_type=agent_type)
            if not user.is_active or not user.is_staff:
                raise ValidationError("Invalid agent credentials")
        except (UserType.DoesNotExist, User.DoesNotExist):
            raise ValidationError("Agent user does not exist or is not active")
        return username

class CourierLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        try:
            courier_type = UserType.objects.get(type='Courier')
            user = User.objects.get(email=username, user_type=courier_type)
            if not user.is_active or not user.is_staff:
                raise ValidationError("Invalid courier credentials")
        except (UserType.DoesNotExist, User.DoesNotExist):
            raise ValidationError("Courier user does not exist or is not active")
        return username


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'comment_image']

        labels = {
            'comment': '',
            'comment_image': ''
        }

