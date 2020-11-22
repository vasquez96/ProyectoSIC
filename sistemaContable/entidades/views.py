from django.shortcuts import render
import json as simplejson
from django.http import JsonResponse
from datetime import datetime
from entidades.models import CicloContable
from entidades.models import CategoriaCuenta
from entidades.models import TipoCuenta
from entidades.models import Cuenta
from entidades.models import CostoMod
from entidades.models import CostoCif
from entidades.models import CostoIndirecto


# Create your views here.

def menu_usuario(requestContext):

    usuario = requestContext.user.username
    idusuario=requestContext.user.id
    modulo = "menu_usuario"
    return render(requestContext, "index.html",{"usuario":usuario, "id": idusuario, "modulo":modulo})

def iniciar_ciclo_contable(requestContext):

    creado = True
    nciclo = CicloContable()
    fecha = datetime.now()
    nciclo.fecha_inicio = fecha
    nciclo.id_usuario = requestContext.user.id
    return JsonResponse(creado,safe=False)

def finalizar_ciclo_contable(requestContext):

    finalizado = True


    return JsonResponse(finalizado, safe=False)


def ingresar_partida_diario(requestContext):

    cuentas= Cuenta.objects.all()

    return render(requestContext, "partidaDiario.html",{"cuentas":cuentas})



def catalogo_de_cuentas(requestContext):

    categorias_obtenidas=CategoriaCuenta.objects.all()

    cuentas = Cuenta.objects.all()

    tipos_de_cuenta = TipoCuenta.objects.all()

    modulo="CatalogoCuentas"


    return render(requestContext,"catalogoDeCuentas.html",{"modulo":modulo, "categorias":categorias_obtenidas, "tipos": tipos_de_cuenta,"cuentas":cuentas})

def crear_cuenta(request):

    cuenta = Cuenta()
    cuenta.nombre_cuenta=request.GET.get('nombreCuentaIbx')
    
    cuentas= Cuenta.objects.all()
    conteo=cuentas.count() + 1

    id_tipo=request.GET.get('tipoCuentacbx')
    tipo=TipoCuenta.objects.filter(id_tipo_cuenta=id_tipo)
    cuenta.id_tipo_cuenta=tipo[0]

    cuenta.codigo_cuenta= tipo[0].codigo_tipo + conteo

    cuenta.naturaleza_cuenta="Acreedora"

    cuenta.save()

    guardado = {"cierto":True,"salvado":"salvado"}
    data=[]
    data.append(guardado)

    return JsonResponse( guardado,safe=False)

def obtener_cuenta(request):

    id_cuenta= request.GET.get('id_cuenta_transaccion_cbx')

    cuenta = Cuenta.objects.filter(id_cuenta = id_cuenta)

    data=[]
    r={"codigo_cuenta":cuenta[0].codigo_cuenta, "nombre_cuenta":cuenta[0].nombre_cuenta}

    data.append(r)

    return JsonResponse(data, safe=False)

def parametros_costos(requestContext):

    modulo="parametrosCostos"
    return render(requestContext, "parametrosCostos.html", {"modulo":modulo})

def informacion_costos(requestContext):

    modulo="informacionCostos"

    #Pagos
    dias= 7
    semanas = 52
    ciclo= CicloContable.objects.get(activo=True)

    cMod= CostoMod.objects.get(id_ciclo=ciclo)
    pago_semanal = cMod.salario_diario * dias
    pago_diario= pago_semanal / cMod.dias_trabajados
    aguinaldo_semanal= ( cMod.dias_aguinaldo * cMod.salario_diario) / semanas
    pago_vacaiones_semanal=(( cMod.dias_aguinaldo * cMod.salario_diario) + cMod.porcentaje_vacaciones*( cMod.dias_aguinaldo * cMod.salario_diario)) / semanas
    pago_salud= ( pago_semanal + pago_vacaiones_semanal ) * cMod.porcentaje_seguro
    pago_afp= ( pago_semanal + pago_vacaiones_semanal) * cMod.porcentaje_afp
    pago_insaforp = ( pago_semanal + pago_vacaiones_semanal ) * cMod.porcentaje_insaforp
    
    #Salario Nonimal

    salario_nomSemanal = cMod.salario_diario * cMod.dias_trabajados
    salario_nomHora = cMod.salario_diario / cMod.horas_trabajadas
    salario_nomDia = cMod.salario_diario

    #Salario Real
    
    salario_realSemanal= pago_semanal + aguinaldo_semanal + pago_vacaiones_semanal + pago_salud + pago_afp + pago_insaforp
    salario_realDia = salario_realSemanal / cMod.dias_trabajados
    salario_realHora = salario_realDia / cMod.horas_trabajadas
    
    #Factor de recargo sin eficiencia

    factor_semana = ( salario_realSemanal / salario_nomSemanal )
    factor_dia = ( salario_realDia /  cMod.salario_diario)
    factor_hora = ( salario_realHora /  salario_nomHora )

    #Factor de recargo con eficiencia

    factor_semana_efi= salario_realSemanal / ( salario_nomSemanal * cMod.factor_recargo)
    factor_dia_efi= salario_realDia / ( cMod.salario_diario * cMod.factor_recargo)
    factor_hora_efi= salario_realHora / ( salario_nomHora * cMod.factor_recargo)

    #CIF
    costo_cif = CostoCif.objects.get(id_ciclo = ciclo)

    costos_i = CostoIndirecto.objects.filter(id_costo_cif=costo_cif)
    suma = 0

    for c in costos_i:
        suma += c.valor_costo_indirecto
    
    cost_cif= suma/costo_cif.valor_base


    return render(requestContext, "informacionCostos.html", {"modulo":modulo, "pago_semanal": round(pago_semanal,2), "pago_diario": round(pago_diario,2), "aguinaldo_semanal": round(aguinaldo_semanal, 2), "pago_vacaiones_semanal": pago_vacaiones_semanal,
    "pago_vacaiones_semanal":round(pago_vacaiones_semanal,2), "pago_salud": round(pago_salud), "pago_afp": round(pago_afp,2), "pago_insaforp": round(pago_insaforp,2),
    "salario_nomSemanal": round(salario_nomSemanal,2), "salario_nomHora": round(salario_nomHora,2), "salario_nomDia": round(salario_nomDia,2),
    "salario_realSemanal": round(salario_realSemanal,2), "salario_realDia": round(salario_realDia,2), "salario_realHora": round(salario_realHora,2),
    "factor_semana": round( factor_semana,2), "factor_dia": round(factor_dia,2), "factor_hora": round(factor_hora,2),
    "factor_semana_efi": round(factor_semana_efi,2), "factor_dia_efi": round(factor_dia_efi,2), "factor_hora_efi": round(factor_hora_efi,2), "suma_cif":suma, "tasa_cif":cost_cif})

def parametros_inventarios(requestContext):

    modulo="parametrosInventario"
    return render(requestContext, "parametrosInventario.html", {"modulo":modulo})

def informacion_inventario(requestContext):

    modulo="informacionInventario"

    return render(requestContext, "informacionInventario.html", {"modulo":modulo})
#NUEVO
def guardarCostosCIF(request):

    nombre= request.GET.get("nombre_costo")
    descripcion= request.GET.get("descripcion_costo")
    valor= request.GET.get("valor_costo")
    

    costo_indirecto = CostoIndirecto()
    ciclo= CicloContable.objects.get(activo=True)
    costo_act = CostoCif.objects.get(id_ciclo = ciclo)
    costo_indirecto.id_costo_cif = costo_act
    costo_indirecto.nombre_costo_indirecto= nombre
    costo_indirecto.descripcion_costo_indirecto= descripcion
    costo_indirecto.valor_costo_indirecto=valor

    costo_indirecto.save()
    data = []
    r= { "Encontrado":"guardado"}
    data.append(r)

    return JsonResponse(data, safe=False)


def guardarCostoDeFabricacion(request):
    
    valor_base= request.GET.get("valorBase")
    metodo_base= request.GET.get("NombreMod")

    costo=CostoCif()
    ciclo= CicloContable.objects.get(activo=True)
    costo.id_ciclo= ciclo
    costo.metodo_base= metodo_base
    costo.valor_base=valor_base

    costo.save()
    data = []
    r= { "Encontrado":"guardado"}
    data.append(r)

    return JsonResponse(data, safe=False)

def guardarParametrosCostosEmpleado(request):
    
    salarioDiario= request.GET.get("salarioDiario")
    diastrabajados= request.GET.get("diastrabajados")
    horasTrabajadas= request.GET.get("horasTrabajadas")
    diasAguinaldo= request.GET.get("diasAguinaldo")
    diasVacaciones= request.GET.get("diasVacaciones")
    recargoVacaciones= request.GET.get("recargoVacaciones")
    porcentajeSeguro= request.GET.get("porcentajeSeguro")
    porcentajeAFP= request.GET.get("porcentajeAFP")
    porcentajeInsaforp= request.GET.get("porcentajeInsaforp")
    eficiencia= request.GET.get("eficiencia")
    numTrabajadores= request.GET.get("numTrabajadores")

    empleado= CostoMod()
    ciclo= CicloContable.objects.get(activo=True)
    empleado.id_ciclo= ciclo
    empleado.salario_diario= salarioDiario
    empleado.dias_trabajados = diastrabajados
    empleado.dias_aguinaldo=diasAguinaldo
    empleado.dias_vacaciones=diasVacaciones
    empleado.porcentaje_vacaciones= recargoVacaciones
    empleado.porcentaje_seguro= porcentajeSeguro
    empleado.porcentaje_afp= porcentajeAFP
    empleado.numero_trabajadores= numTrabajadores
    empleado.porcentaje_insaforp= porcentajeInsaforp
    empleado.factor_recargo= eficiencia
    empleado.horas_trabajadas =horasTrabajadas
    empleado.save()

    data = []
    r= { "Encontrado":"guardado"}
    data.append(r)

    return JsonResponse(data, safe=False)


