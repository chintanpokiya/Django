from django import forms 
from . models import * 

class BecholerForm(forms.ModelForm):
    class Meta:
        model = Becholer
        fields= ['fname', 'lname', 'gender', 'mail', 'max_budget','theme_name', 'addr', 'sugg']
        
        labels={
            'oid':'Order ID',
            'fname':'First Name',
            'lname':'Last Name',
            'gender': 'Gender',
            'mail':'Email ID',
            'max_budget':'Max_Budget',
            'theme_name':'Theme_Name',
            'addr':'Address',
            'sugg':'Suggestion'
        }

        widgets={
            'oid':forms.NumberInput(attrs={'placeholder':'eg.101'}),
            'fname':forms.Textarea(attrs={'placeholder':'eg.femil'}),
            'gender': forms.Select(choices=Becholer.GENDER_CHOICES),
            'lname':forms.Textarea(attrs={'placeholder':'eg.nakarani'}),
            'max_budget': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'theme_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'mail':forms.EmailInput(attrs={'placeholder':'eg.abc@xyz.com'}),
            'addr':forms.Textarea(attrs={'placeholder':'eg.IN'}),
            'sugg': forms.TextInput(attrs={ 'placeholder': 'any SUggestion'}),
        }


class WeddingForm(forms.ModelForm):
    class Meta:
        model = Wedding
        fields = ['gname', 'bname', 'mail', 'mobile_number', 'date', 'time', 'max_budget', 'venue', 'sugg']
        
        labels={
            'oid':'Order ID',
            'gname':'Groom Name',
            'bname':'Bride Name',
            'mail':'Email ID',
            'mobile_number':'Mobile Number',
            'addr':'Address',
            'date':'Date',
            'time':"Time",
            'max_budget':'Max_Budget',
            'venue':'Venue',
            'sugg':'Suggestion'
            
        }
        
        widgets={
            'oid':forms.NumberInput(attrs={'placeholder':'eg.101'}),
            'gname':forms.Textarea(attrs={'placeholder':'eg.Groom FullName'}),
            'bname':forms.Textarea(attrs={'placeholder':'eg.Bride FullName'}),
            'max_budget':forms.NumberInput(attrs={'readonly': 'readonly'}),
            'mail':forms.EmailInput(attrs={'placeholder':'eg.abc@xyz.com'}),
            'addr':forms.Textarea(attrs={'placeholder':'eg.IN'}),
            'venue':forms.Textarea(attrs={'readonly': 'readonly'}),
            'sugg':forms.Textarea(attrs={'placeholder':'eg.Any SUggestion For Dishes and Menu,Venue'}),           
        }
        
        
        
        
class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ['gname', 'bname', 'mail', 'mobile_number', 'date', 'time', 'max_budget', 'venue', 'sugg']
        
        labels={
            'oid':'Order ID',
            'gname':'Groom Name',
            'bname':'Bride Name',
            'mail':'Email ID',
            'mobile_number':'Mobile Number',
            'addr':'Address',
            'date':'Date',
            'time':"Time",
            'max_budget':'Max_Budget',
            'venue':'Venue',
            'sugg':'Suggestion'
            
        }
        
        widgets={
            'oid':forms.NumberInput(attrs={'placeholder':'eg.101'}),
            'gname':forms.Textarea(attrs={'placeholder':'eg.Groom FullName'}),
            'bname':forms.Textarea(attrs={'placeholder':'eg.Bride FullName'}),
            'max_budget':forms.NumberInput(attrs={'readonly': 'readonly'}),
            'mail':forms.EmailInput(attrs={'placeholder':'eg.abc@xyz.com'}),
            'addr':forms.Textarea(attrs={'placeholder':'eg.IN'}),
            'venue':forms.Textarea(attrs={'readonly': 'readonly'}),
            'sugg':forms.Textarea(attrs={'placeholder':'eg.Any SUggestion For Dishes and Menu,Venue'}),           
        }