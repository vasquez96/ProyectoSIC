from django.shortcuts import render
import json as simplejson
from django.http import JsonResponse
from datetime import datetime
from entidades.models import CicloContable
from entidades.models import CategoriaCuenta
from entidades.models import TipoCuenta
from entidades.models import Cuenta
from entidades.models import PartidaDiario
from entidades.models import Mayorizado
from entidades.models import PartidaCuenta

import json

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
        fecha_ciclo=ciclo[0].fecha_inicio.date()
        sin_ciclo=False
        
        partidasDiarioUsuario= PartidaDiario.objects.filter(usuario_responsable=idusuario)

        for p in partidasDiarioUsuario:
            fecha_p = p.fecha_partida

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

def finalizar_ciclo_contable(requestContext):

    finalizado = True

    ciclo = CicloContable.objects.filter(activo=True)
    id_ciclo = ciclo[0].id_ciclo

    ciclo = CicloContable.objects.filter(id_ciclo = id_ciclo).update(activo=False, fecha_fin = datetime.now().date())
    ciclo = CicloContable.objects.get(id_ciclo = id_ciclo)

    cuentas = Cuenta.objects.all()

    for c in cuentas:
        m = Mayorizado()
        m.id_cuenta = c
        m.id_ciclo = ciclo
        m.fecha_inicio = ciclo.fecha_inicio
        m.fecha_final= ciclo.fecha_fin

        partidas_diario = PartidaDiario.objects.all()

        partidas_filtradas =[]

        for pd in partidas_diario:

            if pd.fecha_partida >= ciclo.fecha_inicio.date() and pd.fecha_partida <= ciclo.fecha_fin:
                partidas_filtradas.append(pd)

        saldo_debe=0
        saldo_haber=0

        for pf in partidas_filtradas:

            c_partidas=PartidaCuenta.objects.filter(id_cuenta = c, id_partida = pf)

            for c_pa in c_partidas:

                if c_pa.naturaleza_cuentapartida == "Debe":
                    saldo_debe = saldo_debe + c_pa.saldo_partidacuenta
                else:
                    saldo_haber = saldo_haber + c_pa.saldo_partidacuenta
        
            m.saldo_mayorizado=abs(saldo_debe - saldo_haber)

            if saldo_debe > saldo_haber:
                m.naturaleza_mayorizado = "Debe"
            else:
                if saldo_debe == saldo_haber:
                    m.naturaleza_mayorizado == "Saldado"
                else:
                    m.naturaleza_mayorizado = "Haber"
            m.save()
    
    cuentas = Cuenta.objects.all()
    idusuario=requestContext.user.id



    return render(requestContext, "partida_ajuste.html", {"cuentas": cuentas, "usuario":idusuario})

def crear_partida_diario_ajuste(request):

    n_partida=PartidaDiario()
    descripcion = request.GET.get("descripcion_partida")
    saldo_partida = request.GET.get("saldo_partida")
    usuario_r = request.GET.get("usuario_responsable")

    n_partida.fecha_partida = datetime.now().date()
    n_partida.descripcion_partida=descripcion
    n_partida.saldo_partida=saldo_partida
    n_partida.usuario_responsable=usuario_r
    n_partida.ajuste = True
    n_partida.save()

    guardado = True
    data=[]

    r={"guardado": guardado, "id_partida":n_partida.id_partida}
    data.append(r)


    return JsonResponse(data, safe=False)

def obtener_ciclo_contable(request):
    id_ciclo = request.GET.get('id_ciclo')

    ciclo=CicloContable.objects.get(id_ciclo=id_ciclo)

    data=[]

    r={"fecha_inicio":ciclo.fecha_inicio, "fecha_fin":ciclo.fecha_fin, "id_ciclo":ciclo.id_ciclo}

    data.append(r)

    return JsonResponse(data, safe=False)




def ingresar_partida_diario(requestContext):

    cuentas= Cuenta.objects.all()
    idusuario=requestContext.user.id


    return render(requestContext, "partidaDiario.html",{"cuentas":cuentas, "usuario":idusuario})

def crear_partida_diario(request):

    n_partida=PartidaDiario()
    descripcion = request.GET.get("descripcion_partida")
    saldo_partida = request.GET.get("saldo_partida")
    usuario_r = request.GET.get("usuario_responsable")

    n_partida.fecha_partida = datetime.now().date()
    n_partida.descripcion_partida=descripcion
    n_partida.saldo_partida=saldo_partida
    n_partida.usuario_responsable=usuario_r
    n_partida.ajuste = False
    n_partida.save()

    guardado = True
    data=[]

    r={"guardado": guardado, "id_partida":n_partida.id_partida}
    data.append(r)


    return JsonResponse(data, safe=False)

def obtener_partida_ajuste(request):
    id_ciclo = request.GET.get("id_ciclo")

    ciclo=CicloContable.objects.get(id_ciclo=id_ciclo)

    partida_a = PartidaDiario.objects.get(fecha_partida=ciclo.fecha_fin, ajuste=True)

    r={"id_partida": partida_a.id_partida}
    data=[]
    data.append(r)

    return JsonResponse(data, safe=False)

def crear_partida_cuenta(request):
    codigo_cuenta = request.GET.get("codigo_c")
    naturaleza = request.GET.get("naturaleza_transaccion")
    saldo = request.GET.get("saldo_transaccion")
    id_partida = request.GET.get("id_partida")

    print("valor id")
    print(id_partida)
    print("codigo_c")
    print(codigo_cuenta)
    print("saldo_partida")
    print(saldo)

    pc=PartidaCuenta()

    cuenta = Cuenta.objects.filter(codigo_cuenta=codigo_cuenta)
    partida = PartidaDiario.objects.get(id_partida=id_partida)

    pc=PartidaCuenta()
    pc.id_cuenta=cuenta[0]
    pc.id_partida=partida
    pc.naturaleza_cuentapartida=naturaleza
    pc.saldo_partidacuenta=saldo
    pc.save()

    guardado=True
    data=[]
    r={"guardado":guardado}
    data.append(r)
    

    return JsonResponse(data, safe=False)

def obtener_partida_cuenta(request):

    id_partida = request.GET.get('id_partida')

    partida = PartidaDiario.objects.get(id_partida = id_partida)

    partidasCuenta= PartidaCuenta.objects.filter(id_partida = partida)

    data=[]

    for pc in partidasCuenta:
        cuenta = pc.id_cuenta

        r={"codigo": cuenta.codigo_cuenta, "nombre":cuenta.nombre_cuenta, "naturaleza": pc.naturaleza_cuentapartida, "saldo":pc.saldo_partidacuenta, "total":partida.saldo_partida}

        data.append(r)

    return JsonResponse(data, safe=False)

def mayorizacion(requestContext):

    modulo="mayorizacion"
    cuentas = Cuenta.objects.filter(cuenta_activa =True)
    ciclos_finalizados=CicloContable.objects.filter(activo=False)

    return render(requestContext, "mayorizacion.html", {"modulo":modulo, "cuentas": cuentas, "ciclos_finalizados":ciclos_finalizados})

def obtener_mayorizacion_cuenta(request):

    data=[]
    id_cuenta = request.GET.get("id_cuenta")
    id_ciclo = request.GET.get("id_ciclo")
    mayorizacion_cuenta = Mayorizado.objects.get(id_cuenta = id_cuenta, id_ciclo = id_ciclo)

    fecha_inicio = mayorizacion_cuenta.fecha_inicio
    fecha_final = mayorizacion_cuenta.fecha_final

    partidasDiario = PartidaDiario.objects.filter(ajuste = False)
    partidas=[]
    registros=[]

    for p in partidasDiario:
        fecha_p = p.fecha_partida

        if fecha_p >= fecha_inicio.date() and fecha_p <= fecha_final.date():
            partidas.append(p)
    
    for p in partidas:
        id_partida = p.id_partida

        registro = PartidaCuenta.objects.filter(id_cuenta= id_cuenta, id_partida = id_partida).exists()

        if ( registro == True):
            registro = PartidaCuenta.objects.filter(id_cuenta= id_cuenta, id_partida = id_partida)

            for r in registro:
                registros.append({"id_partida": r.id_partida.id_partida, "saldo_partidacuenta": r.saldo_partidacuenta, "naturaleza_cuentapartida":r.naturaleza_cuentapartida})




    return JsonResponse(registros, safe=False)

def obtener_mayorizaciones_ciclo(request):

    data=[]

    id_ciclo = request.GET.get("id_ciclo")

    mayorizaciones = Mayorizado.objects.filter(id_ciclo = id_ciclo)

    for m in mayorizaciones:
        id_cuenta = m.id_cuenta.id_cuenta

        cuenta = Cuenta.objects.get(id_cuenta = id_cuenta)

        r = {"nombre": cuenta.nombre_cuenta, "naturaleza":m.naturaleza_mayorizado, "saldo": m.saldo_mayorizado}
        data.append(r)
    
    return JsonResponse(data, safe=False)


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

    categoria= CategoriaCuenta.objects.filter(id_categoria_cuenta=request.GET.get('categoriacbx'))
    id_tipo=request.GET.get('tipoCuentacbx')

    if categoria[0].id_categoria_cuenta == 2 or categoria[0].id_categoria_cuenta == 1:
        tipo=TipoCuenta.objects.filter(id_tipo_cuenta=id_tipo)
    
        cuenta.id_tipo_cuenta=tipo[0]

        cuenta.codigo_cuenta= str(categoria[0].codigo_categoria) + str(tipo[0].codigo_tipo) + str(conteo)

        cuenta.naturaleza_cuenta="Acreedora"

        cuenta.cuenta_activa=True

        cuenta.save()
    else:

        tipo=TipoCuenta.objects.filter(id_tipo_cuenta=2)
        cuenta.id_tipo_cuenta=tipo[0]
        cuenta.codigo_cuenta= str(categoria[0].codigo_categoria) + str(conteo)

        cuenta.naturaleza_cuenta="Deudora"

        cuenta.cuenta_activa=True

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

    if categoria[0].codigo_categoria <= 2:
        tipo = TipoCuenta.objects.filter(id_tipo_cuenta=n_tipo)

        cuenta[0].id_tipo_cuenta = tipo[0]
        codigo_cuenta= str(categoria[0].codigo_categoria) + str(tipo[0].codigo_tipo) + str(id_editar)

        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(id_tipo_cuenta=tipo[0])
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(nombre_cuenta=n_nombre)
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(codigo_cuenta = codigo_cuenta)
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(naturaleza_cuenta="debe")
    else:
        codigo_cuenta= str(categoria[0].codigo_categoria) + str(id_editar)
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(nombre_cuenta=n_nombre)
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(codigo_cuenta = codigo_cuenta)
        cuenta = Cuenta.objects.filter(id_cuenta=id_editar).update(naturaleza_cuenta="debe")

    resultado=True
    data=[]
    r={"resultado":resultado}
    data.append(r)


    return JsonResponse(data, safe=False)

def estadosFinancieros(requestContext):

    ciclos_finalizados = CicloContable.objects.filter(activo=False)

    return render(requestContext, "estadosFinancieros.html",{"ciclos_finalizados": ciclos_finalizados})

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