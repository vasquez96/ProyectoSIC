/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     21/11/2020 18:34:57                          */
/*==============================================================*/


drop table if exists CATEGORIA_CUENTA;

drop table if exists CICLO_CONTABLE;

drop table if exists COSTO_CIF;

drop table if exists COSTO_INDIRECTO;

drop table if exists COSTO_INVENTARIO;

drop table if exists COSTO_MOD;

drop table if exists CUENTA;

drop table if exists MAYORIZADO;

drop table if exists PARTIDA_CUENTA;

drop table if exists PARTIDA_DIARIO;

drop table if exists TIPO_CUENTA;

drop table if exists TRANSACCION_INVENTARIO;

/*==============================================================*/
/* Table: CATEGORIA_CUENTA                                      */
/*==============================================================*/
create table CATEGORIA_CUENTA
(
   ID_CATEGORIA_CUENTA  int not null auto_increment,
   NOMBRE_CATEGORIA     varchar(20) not null,
   CODIGO_CATEGORIA     int not null,
   primary key (ID_CATEGORIA_CUENTA)
);

/*==============================================================*/
/* Table: CICLO_CONTABLE                                        */
/*==============================================================*/
create table CICLO_CONTABLE
(
   ID_CICLO             int not null auto_increment,
   FECHA_INICIO         datetime not null,
   FECHA_FIN            date,
   ID_USUARIO           int not null,
   ACTIVO               bool not null,
   primary key (ID_CICLO)
);

/*==============================================================*/
/* Table: COSTO_CIF                                             */
/*==============================================================*/
create table COSTO_CIF
(
   ID_COSTO_CIF         int not null auto_increment,
   ID_CICLO             int not null,
   METODO_BASE          varchar(40) not null,
   VALOR_BASE           decimal(10,2) not null,
   primary key (ID_COSTO_CIF)
);

/*==============================================================*/
/* Table: COSTO_INDIRECTO                                       */
/*==============================================================*/
create table COSTO_INDIRECTO
(
   ID_COSTO_INDIRECTO   int not null auto_increment,
   ID_COSTO_CIF         int not null,
   NOMBRE_COSTO_INDIRECTO varchar(30) not null,
   DESCRIPCION_COSTO_INDIRECTO varchar(200) not null,
   VALOR_COSTO_INDIRECTO decimal(10,2) not null,
   primary key (ID_COSTO_INDIRECTO)
);

/*==============================================================*/
/* Table: COSTO_INVENTARIO                                      */
/*==============================================================*/
create table COSTO_INVENTARIO
(
   ID_COSTO_INVENTARIO  int not null auto_increment,
   ID_CICLO             int not null,
   TIPO_COSTO_INVENTARIO varchar(15) not null,
   NOMBRE_INVENTARIO    varchar(30) not null,
   primary key (ID_COSTO_INVENTARIO)
);

/*==============================================================*/
/* Table: COSTO_MOD                                             */
/*==============================================================*/
create table COSTO_MOD
(
   ID_COSTO_MOD         int not null auto_increment,
   ID_CICLO             int not null,
   SALARIO_DIARIO       decimal(10,2) not null,
   DIAS_TRABAJADOS      int not null,
   DIAS_AGUINALDO       int not null,
   DIAS_VACACIONES      int not null,
   PORCENTAJE_VACACIONES decimal(10,2) not null,
   PORCENTAJE_SEGURO    decimal(10,2) not null,
   PORCENTAJE_AFP       decimal(10,2) not null,
   NUMERO_TRABAJADORES  int not null,
   PORCENTAJE_INSAFORP  decimal(10,2),
   FACTOR_RECARGO       decimal(10,2),
   HORAS_TRABAJADAS     decimal(10,2) not null,
   primary key (ID_COSTO_MOD)
);

/*==============================================================*/
/* Table: CUENTA                                                */
/*==============================================================*/
create table CUENTA
(
   ID_CUENTA            int not null auto_increment,
   ID_TIPO_CUENTA       int not null,
   NOMBRE_CUENTA        varchar(30) not null,
   CODIGO_CUENTA        int not null,
   NATURALEZA_CUENTA    varchar(20) not null,
   CUENTA_ACTIVA        bool not null,
   primary key (ID_CUENTA)
);

/*==============================================================*/
/* Table: MAYORIZADO                                            */
/*==============================================================*/
create table MAYORIZADO
(
   ID_MAYORIZADO        int not null auto_increment,
   ID_CUENTA            int,
   ID_CICLO             int not null,
   SALDO_MAYORIZADO     decimal(10,2) not null,
   FECHA_INICIO         datetime not null,
   FECHA_FINAL          datetime not null,
   NATURALEZA_MAYORIZADO varchar(20) not null,
   primary key (ID_MAYORIZADO)
);

/*==============================================================*/
/* Table: PARTIDA_CUENTA                                        */
/*==============================================================*/
create table PARTIDA_CUENTA
(
   ID_PARTIDACUENTA     int not null auto_increment,
   ID_CUENTA            int not null,
   ID_PARTIDA           int not null,
   NATURALEZA_CUENTAPARTIDA varchar(20) not null,
   SALDO_PARTIDACUENTA  decimal(10,2) not null,
   primary key (ID_PARTIDACUENTA)
);

/*==============================================================*/
/* Table: PARTIDA_DIARIO                                        */
/*==============================================================*/
create table PARTIDA_DIARIO
(
   ID_PARTIDA           int not null auto_increment,
   FECHA_PARTIDA        date not null,
   SALDO_PARTIDA        decimal(10,2) not null,
   DESCRIPCION_PARTIDA  varchar(200) not null,
   USUARIO_RESPONSABLE  int,
   primary key (ID_PARTIDA)
);

/*==============================================================*/
/* Table: TIPO_CUENTA                                           */
/*==============================================================*/
create table TIPO_CUENTA
(
   ID_TIPO_CUENTA       int not null auto_increment,
   ID_CATEGORIA_CUENTA  int not null,
   NOMBRE_TIPO_CUENTA   varchar(30) not null,
   CODIGO_TIPO          int not null,
   primary key (ID_TIPO_CUENTA)
);

/*==============================================================*/
/* Table: TRANSACCION_INVENTARIO                                */
/*==============================================================*/
create table TRANSACCION_INVENTARIO
(
   ID_TRANSACCION_INVENTARIO int not null auto_increment,
   ID_COSTO_INVENTARIO  int not null,
   FECHA_TRANSACCION_INVENTARIO date not null,
   MONTO_TRANSACCION_INVENTARIO decimal(10,2) not null,
   COMPRA               bool not null,
   CANTIDAD_TRANSACCION_INVENTARIO int not null,
   primary key (ID_TRANSACCION_INVENTARIO)
);

alter table COSTO_CIF add constraint FK_SE_CALCULAN foreign key (ID_CICLO)
      references CICLO_CONTABLE (ID_CICLO) on delete restrict on update restrict;

alter table COSTO_INDIRECTO add constraint FK_REGISTRA_CIFS_EN foreign key (ID_COSTO_CIF)
      references COSTO_CIF (ID_COSTO_CIF) on delete restrict on update restrict;

alter table COSTO_INVENTARIO add constraint FK_PERTENECE_A_UN foreign key (ID_CICLO)
      references CICLO_CONTABLE (ID_CICLO) on delete restrict on update restrict;

alter table COSTO_MOD add constraint FK_SE_REGISTRAN_COSTOS foreign key (ID_CICLO)
      references CICLO_CONTABLE (ID_CICLO) on delete restrict on update restrict;

alter table CUENTA add constraint FK_TIPOCUENTA_CUENTA foreign key (ID_TIPO_CUENTA)
      references TIPO_CUENTA (ID_TIPO_CUENTA) on delete restrict on update restrict;

alter table MAYORIZADO add constraint FK_PERTENECE_A foreign key (ID_CICLO)
      references CICLO_CONTABLE (ID_CICLO) on delete restrict on update restrict;

alter table MAYORIZADO add constraint FK_RESULTADO_DE foreign key (ID_CUENTA)
      references CUENTA (ID_CUENTA) on delete restrict on update restrict;

alter table PARTIDA_CUENTA add constraint FK_CONTIENE_TRANSACCIONES foreign key (ID_PARTIDA)
      references PARTIDA_DIARIO (ID_PARTIDA) on delete restrict on update restrict;

alter table PARTIDA_CUENTA add constraint FK_RELACIONA_UNA_TRANSACCION foreign key (ID_CUENTA)
      references CUENTA (ID_CUENTA) on delete restrict on update restrict;

alter table TIPO_CUENTA add constraint FK_SE_CLASIFICA_EN foreign key (ID_CATEGORIA_CUENTA)
      references CATEGORIA_CUENTA (ID_CATEGORIA_CUENTA) on delete restrict on update restrict;

alter table TRANSACCION_INVENTARIO add constraint FK_REGISTRA foreign key (ID_COSTO_INVENTARIO)
      references COSTO_INVENTARIO (ID_COSTO_INVENTARIO) on delete restrict on update restrict;

