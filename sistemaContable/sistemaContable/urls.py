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
from entidades.views import catalogo_de_cuentas, crear_cuenta, obtener_cuenta, parametros_costos, informacion_costos, parametros_inventarios, informacion_inventario

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
    path('informacionCostos', informacion_costos, name="informacionCostos"),
    path('parametrosInventario', parametros_inventarios, name="parametrosInventario"),
    path('informacionInventario/', informacion_inventario, name="informacionInventario"),
]
