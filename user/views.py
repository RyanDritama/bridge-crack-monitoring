  
from django.urls import reverse_lazy
from registration.backends.default.views import RegistrationView

from .forms import CustomUserCreationForm

class SignUpView(RegistrationView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
# Create your views here.
