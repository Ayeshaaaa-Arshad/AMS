from django import forms
from core.models import Announcement
from users.models import CustomUser


#AnnouncementForm
class AnnouncementForm(forms.ModelForm):
    creator = forms.ModelChoiceField(queryset=CustomUser.objects.none(), required=False)  

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'creator']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['creator'].queryset = CustomUser.objects.filter(id=user.id)
            self.fields['creator'].initial = user
 