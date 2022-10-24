import os
from datetime import *

from crum import get_current_request
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict

from config import settings
from core.security.choices import *
from core.user.models import User


class Dashboard(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='dashboard/%Y/%m/%d', null=True, blank=True, verbose_name='Logo')
    icon = models.CharField(max_length=500, verbose_name='Icono FontAwesome')
    layout = models.IntegerField(choices=LAYOUT_OPTIONS, default=LAYOUT_OPTIONS[0][0], verbose_name='Diseño')
    card = models.CharField(max_length=50, choices=CARD, default=CARD[0][0], verbose_name='Card')
    navbar = models.CharField(max_length=50, choices=NAVBAR, default=NAVBAR[0][0], verbose_name='Navbar')
    brand_logo = models.CharField(max_length=50, choices=BRAND_LOGO, default=BRAND_LOGO[0][0], verbose_name='Brand Logo')
    sidebar = models.CharField(max_length=50, choices=SIDEBAR, default=SIDEBAR[0][0], verbose_name='Sidebar')

    def __str__(self):
        return self.name

    def get_template_from_layout(self):
        if self.layout == LAYOUT_OPTIONS[0][0]:
            return 'vtc_body.html'
        return 'hzt_body.html'

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-cubes'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        default_permissions = ()
        permissions = (
            ('view_dashboard', 'Can view Dashboard'),
        )
        ordering = ['-id']


class ModuleType(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    icon = models.CharField(max_length=100, unique=True, verbose_name='Icono')
    is_active = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_modules_vertical(self):
        listmodules = []
        try:
            request = get_current_request()
            group_id = request.user.get_group_id_session()
            if group_id:
                listmodules = self.module_set.filter(is_active=True, is_vertical=True,
                                                     groupmodule__group_id=group_id).order_by('name')
        except:
            pass
        return listmodules

    def get_modules_horizontal(self):
        listmodules = []
        try:
            request = get_current_request()
            group_id = request.user.get_group_id_session()
            if group_id:
                listmodules = self.module_set.filter(is_active=True, is_vertical=False,
                                                     groupmodule__group_id=group_id).order_by('name')
        except:
            pass
        return listmodules

    def toJSON(self):
        item = model_to_dict(self)
        item['icon'] = self.get_icon()
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    class Meta:
        verbose_name = 'Tipo de Módulo'
        verbose_name_plural = 'Tipos de Módulos'
        default_permissions = ()
        permissions = (
            ('view_module_type', 'Can view Tipo de Módulo'),
            ('add_module_type', 'Can add Tipo de Módulo'),
            ('change_module_type', 'Can change Tipo de Módulo'),
            ('delete_module_type', 'Can delete Tipo de Módulo'),
        )
        ordering = ['-id']


class Module(models.Model):
    url = models.CharField(max_length=100, unique=True, verbose_name='Url')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    module_type = models.ForeignKey(ModuleType, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Tipo de Módulo')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name='Icono')
    image = models.ImageField(upload_to='module/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_vertical = models.BooleanField(default=False, verbose_name='Vertical')
    is_active = models.BooleanField(default=True, verbose_name='Estado')
    is_visible = models.BooleanField(default=True, verbose_name='Visible')
    permits = models.ManyToManyField(Permission, blank=True, verbose_name='Permisos')

    def __str__(self):
        return f'{self.name} [{self.url}]'

    def toJSON(self):
        item = model_to_dict(self)
        item['icon'] = self.get_icon()
        item['module_type'] = {} if self.module_type is None else self.module_type.toJSON()
        item['icon'] = self.get_icon()
        item['image'] = self.get_image()
        item['permits'] = [{'id': i.id, 'name': i.name, 'codename': i.codename, 'state': 0} for i in self.permits.all()]
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_image_icon(self):
        if self.image:
            return self.get_image()
        if self.icon:
            return self.get_icon()
        return f'{settings.STATIC_URL}img/default/empty.png'

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Module, self).delete()

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['-name']


class GroupModule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name = 'Grupo Módulo'
        verbose_name_plural = 'Grupos Módulos'
        default_permissions = ()
        ordering = ['-id']


class GroupPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name = 'Grupo Permiso'
        verbose_name_plural = 'Grupos Permisos'
        default_permissions = ()
        ordering = ['-id']


class DatabaseBackups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    remote_addr = models.CharField(max_length=100, null=True, blank=True)
    http_user_agent = models.CharField(max_length=150, null=True, blank=True)
    archive = models.FileField(upload_to='backup/%Y/%m/%d')

    def __str__(self):
        return self.remote_addr

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['hour'] = self.hour.strftime('%H:%M %p')
        item['archive'] = self.get_archive()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            request = get_current_request()
            self.http_user_agent = str(request.user_agent)
            self.remote_addr = request.META.get('REMOTE_ADDR', None)
        except:
            pass
        super(DatabaseBackups, self).save()

    def get_archive(self):
        if self.archive:
            return f'{settings.MEDIA_URL}{self.archive}'
        return ''

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.archive.path)
        except:
            pass
        super(DatabaseBackups, self).delete()

    class Meta:
        verbose_name_plural = 'Respaldo de BD'
        verbose_name = 'Respaldos de BD'
        default_permissions = ()
        permissions = (
            ('view_database_backups', 'Can view Respaldo de BD'),
            ('add_database_backups', 'Can add Respaldo de BD'),
            ('delete_database_backups', 'Can delete Respaldo de BD'),
        )
        ordering = ['-id']


class AccessUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    remote_addr = models.CharField(max_length=100, null=True, blank=True)
    http_user_agent = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.remote_addr

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['hour'] = self.hour.strftime('%H:%M %p')
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            request = get_current_request()
            self.http_user_agent = str(request.user_agent)
            self.remote_addr = request.META.get('REMOTE_ADDR', None)
        except:
            pass
        super(AccessUsers, self).save()

    class Meta:
        verbose_name = 'Acceso del usuario'
        verbose_name_plural = 'Accesos de los usuarios'
        default_permissions = ()
        permissions = (
            ('view_access_users', 'Can view Acceso del usuario'),
            ('delete_access_users', 'Can delete Acceso del usuario'),
        )
        ordering = ['-id']
