from django.urls import path 
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.Index,name="Index"),
    path('SignIn',views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("MakerIndex",views.MakerIndex,name="MakerIndex"),
    path("ViewMed/<int:pk>",views.ViewMed,name="ViewMed"),
    path("ValidateMedicine/<int:pk>",views.ValidateMedicine,name="ValidateMedicine"),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)