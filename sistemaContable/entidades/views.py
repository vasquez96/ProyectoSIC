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
from entidades.models import CostoMod
from entidades.models import CostoCif
from entidades.models import CostoIndirecto

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

def obtener_cuentas_resultado(request):
    cuentas_r = []
    data=[]

    cuentas = Cuenta.objects.all()

    for c in cuentas:

        codigo = str(c.codigo_cuenta)

        categoria = codigo[0]

        if categoria == "4" or categoria == "5":

            cuentas_r.append(c)
    
    for cu in cuentas_r:

        suma_debe =0
        suma_haber =0

        partidascuenta = PartidaCuenta.objects.filter(id_cuenta = cu)

        for p in partidascuenta:

            if p.naturaleza_cuentapartida == "Debe":
                suma_debe+=p.saldo_partidacuenta
            else:
                suma_haber+=p.saldo_partidacuenta
        
        if (suma_debe > suma_haber):
            suma = suma_debe - suma_haber

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Debe"}
            data.append(r)
        else:
            suma = suma_haber - suma_debe

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Haber"}
            data.append(r)

    return JsonResponse(data, safe=False)

def obtener_cuentas_capital(request):

    cuentas = Cuenta.objects.all()
    cuentas_capital=[]
    data=[]

    for c in cuentas:
        codigo = str(c.codigo_cuenta)
        categoria = codigo[0]

        if categoria == "3":
            cuentas_capital.append(c)
    
    for cu in cuentas_capital:
        suma_debe =0
        suma_haber =0

        partidascuenta = PartidaCuenta.objects.filter(id_cuenta = cu)

        for p in partidascuenta:

            if p.naturaleza_cuentapartida == "Debe":
                suma_debe+=p.saldo_partidacuenta
            else:
                suma_haber+=p.saldo_partidacuenta
        
        if (suma_debe > suma_haber):
            suma = suma_debe - suma_haber

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Debe"}
            data.append(r)
        else:
            suma = suma_haber - suma_debe

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Haber"}
            data.append(r)

    return JsonResponse(data, safe=False)

def obtener_cuenta_balance(request):
    cuentas = Cuenta.objects.all()
    cuentas_capital=[]
    data=[]

    for c in cuentas:
        codigo = str(c.codigo_cuenta)
        categoria = codigo[0]

        if categoria == "1" or categoria =="2":
            cuentas_capital.append(c)
    
    for cu in cuentas_capital:
        suma_debe =0
        suma_haber =0

        partidascuenta = PartidaCuenta.objects.filter(id_cuenta = cu)

        for p in partidascuenta:

            if p.naturaleza_cuentapartida == "Debe":
                suma_debe+=p.saldo_partidacuenta
            else:
                suma_haber+=p.saldo_partidacuenta
        
        if (suma_debe > suma_haber):
            suma = suma_debe - suma_haber

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Debe"}
            data.append(r)
        else:
            suma = suma_haber - suma_debe

            r ={"nombre":cu.nombre_cuenta, "saldo":suma, "naturaleza":"Haber"}
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


