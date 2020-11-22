"""sistemaContable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sistemaContable.views import index
from entidades.views import menu_usuario, iniciar_ciclo_contable, finalizar_ciclo_contable, ingresar_partida_diario
from entidades.views import editar_cuenta, mayorizacion, obtener_ciclo_contable, obtener_mayorizacion_cuenta, crear_partida_diario
from entidades.views import crear_partida_cuenta, obtener_partida_cuenta, estadosFinancieros, obtener_mayorizaciones_ciclo, crear_partida_diario_ajuste
from entidades.views import obtener_partida_ajuste, obtener_cuentas_resultado, obtener_cuentas_capital, obtener_cuenta_balance
from entidades.views import catalogo_de_cuentas, crear_cuenta, obtener_cuenta, parametros_costos, informacion_costos, parametros_inventarios, informacion_inventario, guardarParametrosCostosEmpleado, guardarCostoDeFabricacion, guardarCostosCIF

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,  name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('menu_usuario/', menu_usuario, name="menu_usuario"),
    path('iniciarCicloContable/', iniciar_ciclo_contable, name="iniciarCicloContable"),
    path('finalizarCicloContable/', finalizar_ciclo_contable, name="finalizarCicloContable"),
    path('ingresarPartidaDiario/',ingresar_partida_diario, name="ingresarPartidaDiario"),
    path('catalogoDeCuentas/',catalogo_de_cuentas, name="catalogoDeCuentas"),
    path('crearCuenta/', crear_cuenta, name="crearCuenta"),
    path('obtenerCuenta/', obtener_cuenta, name="obtenerCuenta"),
    path('parametrosCosto/', parametros_costos, name="parametrosCostos"),
    path('guardarParametrosCostosEmpleado/', guardarParametrosCostosEmpleado, name= "guardarParametrosCostosEmpleado"),
    path('guardarCostoDeFabricacion/', guardarCostoDeFabricacion, name ="guardarCostoDeFabricacion"),
    path('guardarCostosCIF/', guardarCostosCIF, name = "guardarCostosCIF"),
    path('informacionCostos', informacion_costos, name="informacionCostos"),
    path('parametrosInventario', parametros_inventarios, name="parametrosInventario"),
    path('informacionInventario/', informacion_inventario, name="informacionInventario"),
    path('editarCuenta/', editar_cuenta, name="editarCuenta"),
    path('mayorizacion', mayorizacion, name="mayorizacion"),
    path('obtenerCicloContable/', obtener_ciclo_contable, name="obtenerCicloContable"),
    path('obtenerMayorizacionCuenta/', obtener_mayorizacion_cuenta, name="obtenerMayorizacionCuenta"),
    path('crearPartidaDiario/', crear_partida_diario, name="crearPartidaDiario"),
    path('crearPartidaCuenta/', crear_partida_cuenta, name="crearPartidaCuenta"),
    path('obtenerPartidaCuenta/', obtener_partida_cuenta, name="obtenerPartidaCuenta"),
    path('estadosFinancieros/', estadosFinancieros, name="estadosFinancieros"),
    path('obtenerMayorizacionesCiclo/', obtener_mayorizaciones_ciclo, name="obtenerMayorizacionesCiclo"),
    path('crearPartidaDiarioAjuste/', crear_partida_diario_ajuste, name="crearPartidaDiarioAjuste"),
    path('obtenerPartidaAjuste/', obtener_partida_ajuste, name="obtenerPartidaAjuste"),
    path('obtenerCuentasResultado/', obtener_cuentas_resultado, name="obtenerCuentasResultado"),
    path('obtenerCuentasCapital/', obtener_cuentas_capital, name="obtenerCuentasCapital"),
    path('obtenerCuentaBalance/', obtener_cuenta_balance, name="obtenerCuentasBalance"),

]
