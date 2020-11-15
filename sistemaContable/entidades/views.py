from django.shortcuts import render
import json as simplejson
from django.http import JsonResponse
from datetime import datetime
from entidades.models import CicloContable
from entidades.models import CategoriaCuenta
from entidades.models import TipoCuenta
from entidades.models import Cuenta

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

    return render(requestContext, "informacionCostos.html", {"modulo":modulo})

def parametros_inventarios(requestContext):

    modulo="parametrosInventario"
    return render(requestContext, "parametrosInventario.html", {"modulo":modulo})

def informacion_inventario(requestContext):

    modulo="informacionInventario"

    return render(requestContext, "informacionInventario.html", {"modulo":modulo})