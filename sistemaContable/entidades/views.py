from django.shortcuts import render
import json as simplejson
from django.http import JsonResponse
from datetime import datetime
from entidades.models import CicloContable
from entidades.models import CategoriaCuenta
from entidades.models import TipoCuenta
from entidades.models import Cuenta
from entidades.models import PartidaDiario

# Create your views here.

def menu_usuario(requestContext):

    usuario = requestContext.user.username
    idusuario=requestContext.user.id
    partidasCiclo=[]
    fecha_hoy = datetime.now().date()
    sin_ciclo=False

    #obteniendo el ciclo activo actual, de haberlo
    ciclo=CicloContable.objects.filter(activo=True).exists()

    if ciclo == False:
        sin_ciclo=True
        modulo = "menu_usuario"
        fecha_ciclo=None
        return render(requestContext, "index.html",{"modulo":modulo, "partidas":partidasCiclo, "fecha_hoy":fecha_hoy,"fecha_inicio_ciclo":fecha_ciclo, "sin_ciclo":sin_ciclo, "ciclo_id": 0})
    else:
        #obteniendo las partidas de diario responsabilidad del usuario logeado y a partir del ciclo activo
        ciclo=CicloContable.objects.filter(activo=True)
        fecha_ciclo=ciclo[0].fecha_inicio
        sin_ciclo=False
        
        partidasDiarioUsuario= PartidaDiario.objects.filter(usuario_responsable=idusuario)

        for p in partidasDiarioUsuario:
            fecha_p = p.fecha_partida.date()

            if fecha_ciclo <= fecha_p and fecha_p <= fecha_hoy:
                partidasCiclo.append(p)
        
        modulo = "menu_usuario"
        return render(requestContext, "index.html",{"modulo":modulo, "partidas":partidasCiclo, "fecha_hoy":fecha_hoy,"fecha_inicio_ciclo":fecha_ciclo, "sin_ciclo":sin_ciclo, "ciclo_id": ciclo[0].id_ciclo})

    

def iniciar_ciclo_contable(requestContext):

    creado = True

    nciclo = CicloContable()
    fecha = datetime.now().date()
    nciclo.fecha_inicio = fecha
    nciclo.id_usuario = requestContext.user.id
    nciclo.activo=True

    nciclo.save()

    data=[]
    r={"creado":creado}
    data.append(r)
    return JsonResponse(data,safe=False)

def finalizar_ciclo_contable(request):

    finalizado = True

    id_ciclo = request.GET.get('id_ciclo')

    ciclo = CicloContable.objects.filter(id_ciclo = id_ciclo).update(activo=False)

    r={"finalizado": finalizado}
    data=[]
    data.append(r)


    return JsonResponse(data, safe=False)


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
    categoria= CategoriaCuenta.objects.filter(id_categoria_cuenta=request.GET.get('categoriacbx'))
    cuenta.id_tipo_cuenta=tipo[0]

    cuenta.codigo_cuenta= str(categoria[0].codigo_categoria) + str(tipo[0].codigo_tipo) + str(conteo)

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
    r={"codigo_cuenta":cuenta[0].codigo_cuenta, "nombre_cuenta":cuenta[0].nombre_cuenta, "id_cuenta":cuenta[0].id_cuenta}

    data.append(r)

    return JsonResponse(data, safe=False)

def editar_cuenta(request):
    id_editar=request.GET.get('id_actualizar_cuenta')
    n_categoria=request.GET.get('editcategoriacbx')
    n_tipo=request.GET.get('edittipoCuentacbx')
    n_nombre=request.GET.get('editnombreCuentaIbx')

    cuenta = Cuenta.objects.filter(id_cuenta=id_editar)
    categoria = CategoriaCuenta.objects.filter(id_categoria_cuenta=n_categoria)
    tipo = TipoCuenta.objects.filter(id_tipo_cuenta=n_tipo)

    cuenta[0].id_tipo_cuenta = tipo[0]
    codigo_cuenta= str(categoria[0].codigo_categoria) + str(tipo[0].codigo_tipo) + str(id_editar)

    cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(id_tipo_cuenta=tipo[0])
    cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(nombre_cuenta=n_nombre)
    cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(codigo_cuenta = codigo_cuenta)
    cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(naturaleza_cuenta="debe")


    resultado=True
    data=[]
    r={"resultado":resultado}
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