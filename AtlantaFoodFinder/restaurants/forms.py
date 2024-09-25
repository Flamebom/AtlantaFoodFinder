from django import forms

class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Restaurant Name')
    cuisine_type = forms.CharField(required=False, label='Cuisine Type')
    location = forms.CharField(required=False, label='Location')
    rating = forms.FloatField(required=False, label='Minimum Rating', min_value=0, max_value=5)
