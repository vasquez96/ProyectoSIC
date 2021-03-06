# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CategoriaCuenta(models.Model):
    id_categoria_cuenta = models.AutoField(db_column='ID_CATEGORIA_CUENTA', primary_key=True)  # Field name made lowercase.
    nombre_categoria = models.CharField(db_column='NOMBRE_CATEGORIA', max_length=20)  # Field name made lowercase.
    codigo_categoria = models.IntegerField(db_column='CODIGO_CATEGORIA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoria_cuenta'


class CicloContable(models.Model):
    id_ciclo = models.AutoField(db_column='ID_CICLO', primary_key=True)  # Field name made lowercase.
    fecha_inicio = models.DateTimeField(db_column='FECHA_INICIO')  # Field name made lowercase.
    fecha_fin = models.DateField(db_column='FECHA_FIN', blank=True, null=True)  # Field name made lowercase.
    id_usuario = models.IntegerField(db_column='ID_USUARIO')  # Field name made lowercase.
    activo = models.IntegerField(db_column='ACTIVO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ciclo_contable'


class Cuenta(models.Model):
    id_cuenta = models.AutoField(db_column='ID_CUENTA', primary_key=True)  # Field name made lowercase.
    id_tipo_cuenta = models.ForeignKey('TipoCuenta', models.DO_NOTHING, db_column='ID_TIPO_CUENTA')  # Field name made lowercase.
    nombre_cuenta = models.CharField(db_column='NOMBRE_CUENTA', max_length=30)  # Field name made lowercase.
    codigo_cuenta = models.IntegerField(db_column='CODIGO_CUENTA')  # Field name made lowercase.
    naturaleza_cuenta = models.CharField(db_column='NATURALEZA_CUENTA', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cuenta'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Mayorizado(models.Model):
    id_mayorizado = models.AutoField(db_column='ID_MAYORIZADO', primary_key=True)  # Field name made lowercase.
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='ID_CUENTA', blank=True, null=True)  # Field name made lowercase.
    id_ciclo = models.ForeignKey(CicloContable, models.DO_NOTHING, db_column='ID_CICLO')  # Field name made lowercase.
    saldo_mayorizado = models.DecimalField(db_column='SALDO_MAYORIZADO', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fecha_inicio = models.DateTimeField(db_column='FECHA_INICIO')  # Field name made lowercase.
    fecha_final = models.DateTimeField(db_column='FECHA_FINAL')  # Field name made lowercase.
    naturaleza_mayorizado = models.CharField(db_column='NATURALEZA_MAYORIZADO', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mayorizado'


class PartidaCuenta(models.Model):
    id_partidacuenta = models.AutoField(db_column='ID_PARTIDACUENTA', primary_key=True)  # Field name made lowercase.
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='ID_CUENTA')  # Field name made lowercase.
    id_partida = models.ForeignKey('PartidaDiario', models.DO_NOTHING, db_column='ID_PARTIDA')  # Field name made lowercase.
    naturaleza_cuentapartida = models.CharField(db_column='NATURALEZA_CUENTAPARTIDA', max_length=20)  # Field name made lowercase.
    saldo_partidacuenta = models.DecimalField(db_column='SALDO_PARTIDACUENTA', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partida_cuenta'


class PartidaDiario(models.Model):
    id_partida = models.AutoField(db_column='ID_PARTIDA', primary_key=True)  # Field name made lowercase.
    fecha_partida = models.DateField(db_column='FECHA_PARTIDA')  # Field name made lowercase.
    saldo_partida = models.DecimalField(db_column='SALDO_PARTIDA', max_digits=10, decimal_places=2)  # Field name made lowercase.
    descripcion_partida = models.CharField(db_column='DESCRIPCION_PARTIDA', max_length=200)  # Field name made lowercase.
    usuario_responsable = models.IntegerField(db_column='USUARIO_RESPONSABLE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partida_diario'


class TipoCuenta(models.Model):
    id_tipo_cuenta = models.AutoField(db_column='ID_TIPO_CUENTA', primary_key=True)  # Field name made lowercase.
    id_categoria_cuenta = models.ForeignKey(CategoriaCuenta, models.DO_NOTHING, db_column='ID_CATEGORIA_CUENTA')  # Field name made lowercase.
    nombre_tipo_cuenta = models.CharField(db_column='NOMBRE_TIPO_CUENTA', max_length=30)  # Field name made lowercase.
    codigo_tipo = models.IntegerField(db_column='CODIGO_TIPO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipo_cuenta'
