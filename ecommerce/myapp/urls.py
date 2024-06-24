from django.urls import path
from . import views
from . forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home, name="home"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    
    # Login Authentication
    path("registeration/", views.Signup, name="signup"),
    path("login/", views.Signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name = 'myapp/passwordchange.html', form_class=MyPasswordChangeForm, success_url = '/passwordchangedone'), name="passwordchange"),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name = 'myapp/passwordchangedone.html'), name="passwordchangedone"),
    
    # Password Reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_done'),   
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name='password_reset_complete'),
        
    # Profile
    path('profile/', views.ProfileView, name='profile'),
    path('address/', views.Address, name='address'),
    path('updateaddress/<int:pk>', views.UpdateAddress, name="updateaddress"),
    
    # About and Contact
    path("about/", views.About, name="about"),
    path("contact/", views.Contact, name="contact"),
    
    # Cart and Wishlist
    path("add-to-cart/", views.AddToCart, name="addtocart"),
    path("cart/", views.ShowCart, name="showcart"),
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path("paymentdone/", views.PaymentDone, name="paymentdone"),
    path("orders/", views.Home, name="orders"),
    
    path("pluscart/", views.PlusCart),
    path("minuscart/", views.MinusCart),
    path("removecart/", views.RemoveCart),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)