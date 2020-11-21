# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class CostoCif(models.Model):
    id_costo_cif = models.AutoField(db_column='ID_COSTO_CIF', primary_key=True)  # Field name made lowercase.
    id_ciclo = models.ForeignKey(CicloContable, models.DO_NOTHING, db_column='ID_CICLO')  # Field name made lowercase.
    metodo_base = models.CharField(db_column='METODO_BASE', max_length=40)  # Field name made lowercase.
    valor_base = models.DecimalField(db_column='VALOR_BASE', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'costo_cif'


class CostoIndirecto(models.Model):
    id_costo_indirecto = models.AutoField(db_column='ID_COSTO_INDIRECTO', primary_key=True)  # Field name made lowercase.
    id_costo_cif = models.ForeignKey(CostoCif, models.DO_NOTHING, db_column='ID_COSTO_CIF')  # Field name made lowercase.
    nombre_costo_indirecto = models.CharField(db_column='NOMBRE_COSTO_INDIRECTO', max_length=30)  # Field name made lowercase.
    descripcion_costo_indirecto = models.CharField(db_column='DESCRIPCION_COSTO_INDIRECTO', max_length=200)  # Field name made lowercase.
    valor_costo_indirecto = models.DecimalField(db_column='VALOR_COSTO_INDIRECTO', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'costo_indirecto'


class CostoInventario(models.Model):
    id_costo_inventario = models.AutoField(db_column='ID_COSTO_INVENTARIO', primary_key=True)  # Field name made lowercase.
    id_ciclo = models.ForeignKey(CicloContable, models.DO_NOTHING, db_column='ID_CICLO')  # Field name made lowercase.
    tipo_costo_inventario = models.CharField(db_column='TIPO_COSTO_INVENTARIO', max_length=15)  # Field name made lowercase.
    nombre_inventario = models.CharField(db_column='NOMBRE_INVENTARIO', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'costo_inventario'


class CostoMod(models.Model):
    id_costo_mod = models.AutoField(db_column='ID_COSTO_MOD', primary_key=True)  # Field name made lowercase.
    id_ciclo = models.ForeignKey(CicloContable, models.DO_NOTHING, db_column='ID_CICLO')  # Field name made lowercase.
    salario_diario = models.DecimalField(db_column='SALARIO_DIARIO', max_digits=10, decimal_places=2)  # Field name made lowercase.
    dias_trabajados = models.IntegerField(db_column='DIAS_TRABAJADOS')  # Field name made lowercase.
    dias_aguinaldo = models.IntegerField(db_column='DIAS_AGUINALDO')  # Field name made lowercase.
    dias_vacaciones = models.IntegerField(db_column='DIAS_VACACIONES')  # Field name made lowercase.
    porcentaje_vacaciones = models.DecimalField(db_column='PORCENTAJE_VACACIONES', max_digits=10, decimal_places=2)  # Field name made lowercase.
    porcentaje_seguro = models.DecimalField(db_column='PORCENTAJE_SEGURO', max_digits=10, decimal_places=2)  # Field name made lowercase.
    porcentaje_afp = models.DecimalField(db_column='PORCENTAJE_AFP', max_digits=10, decimal_places=2)  # Field name made lowercase.
    numero_trabajadores = models.IntegerField(db_column='NUMERO_TRABAJADORES')  # Field name made lowercase.
    porcentaje_insaforp = models.DecimalField(db_column='PORCENTAJE_INSAFORP', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    factor_recargo = models.DecimalField(db_column='FACTOR_RECARGO', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    horas_trabajadas = models.DecimalField(db_column='HORAS_TRABAJADAS', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'costo_mod'


class Cuenta(models.Model):
    id_cuenta = models.AutoField(db_column='ID_CUENTA', primary_key=True)  # Field name made lowercase.
    id_tipo_cuenta = models.ForeignKey('TipoCuenta', models.DO_NOTHING, db_column='ID_TIPO_CUENTA')  # Field name made lowercase.
    nombre_cuenta = models.CharField(db_column='NOMBRE_CUENTA', max_length=30)  # Field name made lowercase.
    codigo_cuenta = models.IntegerField(db_column='CODIGO_CUENTA')  # Field name made lowercase.
    naturaleza_cuenta = models.CharField(db_column='NATURALEZA_CUENTA', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cuenta'


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


class TransaccionInventario(models.Model):
    id_transaccion_inventario = models.AutoField(db_column='ID_TRANSACCION_INVENTARIO', primary_key=True)  # Field name made lowercase.
    id_costo_inventario = models.ForeignKey(CostoInventario, models.DO_NOTHING, db_column='ID_COSTO_INVENTARIO')  # Field name made lowercase.
    fecha_transaccion_inventario = models.DateField(db_column='FECHA_TRANSACCION_INVENTARIO')  # Field name made lowercase.
    monto_transaccion_inventario = models.DecimalField(db_column='MONTO_TRANSACCION_INVENTARIO', max_digits=10, decimal_places=2)  # Field name made lowercase.
    compra = models.IntegerField(db_column='COMPRA')  # Field name made lowercase.
    cantidad_transaccion_inventario = models.IntegerField(db_column='CANTIDAD_TRANSACCION_INVENTARIO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaccion_inventario'
