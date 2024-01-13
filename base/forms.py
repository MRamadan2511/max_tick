# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, UserType, Ticket, Comment

from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField





class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        if user_type == 'Courier':
            self.fields['order_id'].label = 'رقم الاوردر'
            self.fields['post_image'].label = 'أضف صورة'

    class Meta:
        model = Ticket
        fields = ['order_id', 'description', 'post_image',]

        labels = {
            # 'order_id': 'Order ID',
            'description': '',

        }

        widgets = {
                'description': CKEditorWidget(),

            }
   

class AgentLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        try:
            agent_type = UserType.objects.get(type='agent')
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

        widgets = {
                'comment': CKEditorWidget(),

            }
   
    
    


class UpdateLocationForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['location']
        # Add a widget to use a dropdown for the location field
        widgets = {
                'location': forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
            'location': '',

        }

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']


        widgets = {
                'status': forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
            'status': '',

        }

class UpdateTagForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['tag']


        widgets = {
                'tag': forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
            'tag': '',

        }
class UpdateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['department']


        widgets = {
                'department': forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
            'department': '',

        }


class UpdateAssignedToForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['assigned_to']


        widgets = {
                'assigned_to': forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
            'assigned_to': '',

        }



class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='')
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='')


    reset = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
        initial=True,
    )

  