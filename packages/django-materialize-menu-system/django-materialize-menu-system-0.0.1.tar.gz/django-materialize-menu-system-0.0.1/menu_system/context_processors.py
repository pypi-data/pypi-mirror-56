from django.conf import settings
from menu_system import models


def menu_context( request ):
    links = models.Menu.objects.all().order_by( 'name' )
    return { 'links': links }


def app_context( request ):
    apps = models.App.objects.all().order_by( 'name' )
    return { 'apps': apps }


def social_context( request ):
    social_links = models.Social.objects.all().order_by( 'name' )
    return { 'social_links': social_links }


def user_context( request ):
    user_links = models.UserLink.objects.all().order_by( 'name' )
    return { 'user_links': user_links }


def WebsiteInfo( request ):
    return {
        'company_name': settings.WEBSITE_NAME,
        'company_short_name': settings.WEBSITE_SHORT_NAME,
        'company_tagline': settings.WEBSITE_TAGLINE,
        'company_website': settings.COMPANY_WEBSITE,
        'menu_color': settings.MENU_COLOR
        }
