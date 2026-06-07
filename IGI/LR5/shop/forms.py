"""Forms with server-side validation (client-side via HTML5 attributes in templates)."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from shop.models import ClientProfile, Order, OrderItem, Product, Review
from shop.validators import validate_adult_age, validate_belarus_phone


class BelarusPhoneWidget(forms.TextInput):
    """HTML5 pattern for Belarus phone on the client."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update(
            {
                'placeholder': '+375 (29) 123-45-67',
                'pattern': r'\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}',
                'title': 'Format: +375 (29) XXX-XX-XX',
            }
        )
        super().__init__(*args, **kwargs)


class CustomerRegistrationForm(UserCreationForm):
    """Register new customer with profile fields."""

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=22, widget=BelarusPhoneWidget())
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'max': '2008-01-01'}),
        help_text='Must be 18+',
    )
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_belarus_phone(phone)
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_adult_age(birth_date)
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            ClientProfile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
            )
        return user


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
    )
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'required': True, 'minlength': 10}))

    class Meta:
        model = Review
        fields = ('rating', 'text')


class ProductFilterForm(forms.Form):
  q = forms.CharField(required=False, label='Search')
  min_price = forms.DecimalField(required=False, min_value=0, label='Min price')
  max_price = forms.DecimalField(required=False, min_value=0, label='Max price')
  sort = forms.ChoiceField(
      required=False,
      choices=[
          ('name', 'Name A-Z'),
          ('-name', 'Name Z-A'),
          ('price', 'Price low-high'),
          ('-price', 'Price high-low'),
      ],
  )
  category = forms.IntegerField(required=False)


class CheckoutForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=1, max_value=100)
    pickup_point = forms.IntegerField(required=False)
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'required': True}))
    promo_code = forms.CharField(required=False, max_length=50)


class OrderCRUDForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'employee', 'pickup_point', 'promo_code', 'delivery_date', 'delivery_cost', 'notes')


class ProductCRUDForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'unit', 'category', 'manufacturer', 'description', 'is_available')