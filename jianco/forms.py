from django import forms
from .models import MNR

class MNRForm(forms.ModelForm):
    class Meta:
        model = MNR
        fields = ['dayDay', 'start_inventory', 'gallons_delivered', 'gallons_pumped', 'book_inventory', 'inches', 'gallons', 'daily', 'initials', 'regular', 'super', 'premium', 'start_inventory_p', 'gallons_delivered_p', 'gallons_pumped_p', 'book_inventory_p', 'inches_p', 'gallons_p', 'daily_p', 'initials_p']
        # Add other fields as needed
