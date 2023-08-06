from django.conf import settings
from django.conf.urls import url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.users.widgets import UserListingButton

from wagtail_2fa import views


@hooks.register("register_admin_urls")
def urlpatterns():
    return [
        url(r"^2fa/auth$", views.LoginView.as_view(), name="wagtail_2fa_auth"),
        url(
            r"^2fa/devices/(?P<user_id>\d+)$",
            views.DeviceListView.as_view(),
            name="wagtail_2fa_device_list",
        ),
        url(
            r"^2fa/devices/new$",
            views.DeviceCreateView.as_view(),
            name="wagtail_2fa_device_new",
        ),
        url(
            r"^2fa/devices/(?P<pk>\d+)/update$",
            views.DeviceUpdateView.as_view(),
            name="wagtail_2fa_device_update",
        ),
        url(
            r"^2fa/devices/(?P<pk>\d+)/remove$",
            views.DeviceDeleteView.as_view(),
            name="wagtail_2fa_device_remove",
        ),
        url(
            r"^2fa/devices/qr-code$",
            views.DeviceQRCodeView.as_view(),
            name="wagtail_2fa_device_qrcode",
        ),
    ]


@hooks.register("construct_main_menu")
def remove_menu_if_unverified(request, menu_items):
    if not request.user.is_verified() and settings.WAGTAIL_2FA_REQUIRED:
        menu_items.clear()
        menu_items.append(MenuItem("2FA Setup", reverse('wagtail_2fa_device_list', kwargs={'user_id': request.user.id})))


@hooks.register("register_account_menu_item")
def register(request):
    return {
        "url": reverse('wagtail_2fa_device_list', kwargs={'user_id': request.user.id}),
        "label": _("Manage your 2FA devices"),
        "help_text": _("Add or remove devices for 2 factor authentication."),
    }

@hooks.register('register_user_listing_buttons')
def register_user_listing_buttons(context, user):
    yield UserListingButton(    
        _('Manage 2FA'),    
        reverse('wagtail_2fa_device_list', kwargs={'user_id': user.id}),
        attrs={'title': _('Edit this user')}, priority=100)
