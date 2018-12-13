from django.db import models


# Create your models here.


class Menu(models.Model):
    title = models.CharField(verbose_name='一级菜单名称', max_length=32)
    icon = models.CharField(verbose_name='菜单图标', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128, unique=True)

    menu = models.ForeignKey(verbose_name='二级菜单所属菜单的一级菜单', to='Menu', on_delete=True, null=True,
                             blank=True, help_text='null表示该项不是菜单，非null表示二级菜单')

    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)

    # is_menu = models.BooleanField(verbose_name='是否可以做菜单', default=False)  # 是否可以做菜单，默认都是不可以
    # # null是数据库可以为空，blank是指Django-admin可以为空
    # icon = models.CharField(verbose_name='菜单图标',max_length=32,null=True,blank=True)

    # name = models.CharField(verbose_name='代码', max_length=64, unique=True, null=False, blank=False)
    #
    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='patents', null=True, blank=True,
                            help_text="对于无法作为菜单的URL，可以为其选择一个可以作为菜单的权限，那么访问时，则默认选中此权限",
                            limit_choices_to={'menu__isnull': False}, on_delete=models.SET_NULL)
    #
    # menu = models.ForeignKey(verbose_name='是否可以做菜单', to='Menu', null=True, blank=True, help_text='null表示非菜单',
    #                          on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64, null=True, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)

    def __str__(self):
        return self.name

# class Meta:
# abstract = True  # 如果将一个类设置为abstract，则此类必须被继承使用。此类不可生成对象，必须被继承使用
