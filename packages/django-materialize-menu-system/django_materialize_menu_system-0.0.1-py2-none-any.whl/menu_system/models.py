from django.db import models


class Menu( models.Model ):
    name = models.CharField( max_length = 20 )
    summary = models.CharField( max_length = 20, blank = True, null = True )
    details = models.TextField( blank = True, null = True )
    link_view_name = models.CharField( max_length = 50, blank = True, null =
    True )
    link_view_path = models.CharField( max_length = 50, blank = True, null =
    True )
    icon = models.ImageField( blank = True, null = True )
    superuser_only = models.BooleanField( default = True, blank = True, null =
    True )
    account_req = models.BooleanField(default = False)


    def __str__( self ):
        return self.name


class App( models.Model ):
    name = models.CharField( max_length = 20 )
    summary = models.CharField( max_length = 20, blank = True, null = True )
    details = models.TextField( blank = True, null = True )
    link_view_name = models.CharField( max_length = 50, blank = True, null =
    True )
    link_view_path = models.CharField( max_length = 50, blank = True, null =
    True )
    icon = models.ImageField( blank = True, null = True )
    superuser_only = models.BooleanField( default = True, blank = True, null =
    True )
    account_req = models.BooleanField(default = True)


    def __str__( self ):
        return self.name


class UserLink( models.Model ):
    name = models.CharField( max_length = 20 )
    summary = models.CharField( max_length = 20, blank = True, null = True )
    details = models.TextField( blank = True, null = True )
    link_view_name = models.CharField( max_length = 50, blank = True, null =
    True )
    link_view_path = models.CharField( max_length = 50, blank = True, null =
    True )
    icon = models.ImageField( blank = True, null = True )
    superuser_only = models.BooleanField( default = True, blank = True, null =
    True )
    account_req = models.BooleanField(default = True)

    def __str__( self ):
        return self.name


class Social( models.Model ):
    name = models.CharField( blank = True, null = True, max_length = 20 )
    icon_name = models.CharField( blank = True, null = True, max_length = 50 )
    icon_class = models.CharField( max_length = 50, blank = True, null = True )
    icon_color = models.CharField( max_length = 50, blank = True, null = True )
    icon_shade = models.CharField( max_length = 50, blank = True, null = True )
    social_url = models.URLField( blank = True, null = True )
    account_req = models.BooleanField(default = False)


    def __str__( self ):
        return self.name
