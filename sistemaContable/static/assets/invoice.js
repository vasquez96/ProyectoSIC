$(document).on('ready', funcMain);
var i=0;

function funcMain()
{
	$("#add_row").on('click',newRowTable);
	$("#add_row1").on('click',newRowTable2);
	
	$("loans_table").on('click','.fa-eraser',deleteProduct);
	$("loans_table").on('click','.fa-edit',editProduct);

	$("body").on('click',".fa-eraser",deleteProduct);
	$("body").on('click',".fa-edit",editProduct);
	
}

function deleteProduct(){
	//Guardando la referencia del objeto presionado
	var _this = this;
	//Obtener las filas los datos de la fila que se va a elimnar
	var array_fila=getRowSelected(_this);

	//Restar esos datos a los totales mostrados al finales
	//calculateTotals(cantidad, precio, subtotal, impuesto, totalneto, accioneliminar)
	calculateTotals(array_fila[1],array_fila[2],array_fila[3],array_fila[4],array_fila[5],array_fila[6],2);

	$(this).parent().parent().fadeOut("slow",function(){$(this).remove();});
}

function editProduct(){
	var _this = this;;
	var array_fila=getRowSelected(_this);
	console.log(array_fila[0]+" - "+array_fila[1]+" - "+array_fila[2]+" - "+array_fila[3]+" - "+array_fila[4]+" - "+array_fila[5]+" - "+array_fila[6]);
	//Codigo de editar una fila lo pueden agregar aqui
}

function getRowSelected(objectPressed){
	//Obteniendo la linea que se esta eliminando
	var a=objectPressed.parentNode.parentNode;
	//b=(fila).(obtener elementos de clase columna y traer la posicion 0).(obtener los elementos de tipo parrafo y traer la posicion0).(contenido en el nodo)
	var fecha=a.getElementsByTagName("td")[0].getElementsByTagName("p")[0].innerHTML;
	var cantComp=a.getElementsByTagName("td")[1].getElementsByTagName("p")[0].innerHTML;
	var costComp=a.getElementsByTagName("td")[2].getElementsByTagName("p")[0].innerHTML;
	var totalComp=a.getElementsByTagName("td")[3].getElementsByTagName("p")[0].innerHTML;
	var cantVent=a.getElementsByTagName("td")[4].getElementsByTagName("p")[0].innerHTML;
	var costVent=a.getElementsByTagName("td")[5].getElementsByTagName("p")[0].innerHTML;
	var totalVent=a.getElementsByTagName("td")[6].getElementsByTagName("p")[0].innerHTML;
	var cantSaldo=a.getElementsByTagName("td")[7].getElementsByTagName("p")[0].innerHTML;
	var costSaldo=a.getElementsByTagName("td")[8].getElementsByTagName("p")[0].innerHTML;
	var totalSaldo=a.getElementsByTagName("td")[9].getElementsByTagName("p")[0].innerHTML;	

	var array_fila = [fecha, cantComp, costComp, totalComp, cantVent, costVent, totalVent, cantSaldo, costSaldo, totalSaldo];

	return array_fila;
	//console.log(numero+' '+codigo+' '+descripcion);
}

var array_cantComp=[];
var array_cantComp2=[];
var array_cantComp3=[];

var array_costComp=[];
var array_costComp2=[];
var array_costComp3=[];

var array_cantSaldo=[];
var array_cantSaldo2=[];
var array_cantSaldo3=[];

var array_totalSaldo=[];
var array_totalSaldo2=[];
var array_totalSaldo3=[];

var array_totalVenta=[]; 

var sumCantSaldo1=0;
var sumCantSaldo2=0;
var sumCantSaldo3=0;

var sumTotalSaldo1=0;
var sumTotalSaldo2=0;
var sumTotalSaldo3=0;

var costSaldo3=0;

function newRowTable()
{
	var cantComp=0, costComp=0, cantVent=0.00, costVent=0.00, totalVent=0.00, totalSaldo=0;	
	var fecha="", x=0, y=0, cantSaldo=0, cantSaldo2=0, cantSaldo3=0, costoSaldo=0;	
	var sumCantSaldo=0;
	var sumTotalSaldo=0, sumTotalSald2=0, sumTotalSald3=0; sumTotalSaldo11=0;

	fecha=document.getElementById("fecha1").value;
	cantComp=document.getElementById("cantComp").value;
	costComp=document.getElementById("costComp").value;	
	var totalComp=(parseFloat(cantComp)*parseFloat(costComp));
	var input = document.getElementById('cantComp').value;
  	x = eval(input);  
	array_cantComp.unshift(x);
	array_cantComp2.unshift(x);
	array_cantComp3.unshift(x);
	var input = document.getElementById('costComp').value;
  	y = eval(input);  
	array_costComp.unshift(y);
	array_costComp2.unshift(y);
	array_costComp2.unshift(y);
	array_costComp3.unshift(y);

	var input = document.getElementById('cantComp').value;	  
	cantSaldo = eval(input);  
	array_cantSaldo.push(cantSaldo);		
	for (var i=0; i<array_cantSaldo.length; i++) {    	
		sumCantSaldo+=parseInt(array_cantSaldo[i]);				
	}
	
	var b = document.getElementById('cantComp').value;	  
	cantSaldo2 = eval(b);  
	array_cantSaldo2.push(cantSaldo2);		
	for (var i=0; i<array_cantSaldo2.length; i++) {    	
		sumCantSaldo2+=parseInt(array_cantSaldo2[i]);				
	}

	var n = document.getElementById('cantComp').value;	  
	cantSaldo3 = eval(n);
	array_cantSaldo3.push(cantSaldo2);		
	for (var i=0; i<array_cantSaldo3.length; i++) {    	
		sumCantSaldo3+=parseInt(array_cantSaldo3[i]);					
	}
	
	totalSaldo = parseFloat(totalComp);  
	  array_totalSaldo.push(totalSaldo);		
	for (var i=0; i<array_totalSaldo.length; i++) {    	
		sumTotalSaldo+=parseFloat(array_totalSaldo[i]);				
	}
	
	totalSaldo2 = parseFloat(totalComp);  
	  array_totalSaldo2.unshift(totalSaldo2);		
	for (var i=0; i<array_totalSaldo2.length; i++) {    	
		sumTotalSald2+=parseFloat(array_totalSaldo2[i]);				
	}
	totalSaldo3 = parseFloat(totalComp); 	 
	array_totalSaldo3.push(totalSaldo3);		
	for (var i=0; i<array_totalSaldo3.length; i++) {    	
		sumTotalSald3+=parseFloat(array_totalSaldo3[i]);					
	}
	
	if (array_totalVenta.length==0){
		sumTotalSaldo1=sumTotalSaldo;
		sumTotalSaldo2=sumTotalSald2;
		sumTotalSaldo3=sumTotalSald3;
		sumCantSaldo1=sumCantSaldo;
		sumCantSaldo2=sumCantSaldo2;
		sumCantSaldo3=sumCantSaldo3;		
	}else{			
		sumTotalSaldo1=sumTotalSaldo1+totalComp;
		sumTotalSaldo2=sumTotalSaldo2+totalComp;
		sumTotalSaldo3=sumTotalSaldo3+totalComp;
		sumCantSaldo1+=parseFloat(array_cantSaldo[0]);
		sumCantSaldo2+=parseFloat(array_cantSaldo2[0]);
		sumCantSaldo3+=parseFloat(array_cantSaldo3[0]);
	}
	
	var name_table=document.getElementById("tabla_inventario");
	var rowCount = name_table.rows.length;
    var row = name_table.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10);    

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo1+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo1.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';
	
	var name_table2=document.getElementById("tabla_inventario2");
	var rowCount = name_table2.rows.length;
    var row = name_table2.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10);    

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo2.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';

	var name_table3=document.getElementById("tabla_inventario3");
	var rowCount = name_table3.rows.length;
    var row = name_table3.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10); 
	
	costSaldo3=sumTotalSaldo1/sumCantSaldo1;

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo3.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';

    //Para calcular los totales enviando los parametros
	calculateTotals(parseFloat(cantComp), costComp, totalComp, cantVent, costVent, totalVent,1);	
    //Para calcular los totales sin enviar los parametros, solo adquiriendo los datos de la columna con mismo tipo de datos
	//calculateTotalsBySumColumn()	
}


function newRowTable2()
{
	var cantComp=0, costComp=0, cantVent=0.00, costVent=0, costVent2=0, costVent3=0, totalComp=0 ,totalVent1=0.00, totalVent2=0.00, totalVent3=0.00;	
	var fecha="", costoSaldo=0, sumTotalSaldo21=0, sumTotalSaldo31=0; var total1=0,total2=0;		
	
	fecha=document.getElementById("fecha1").value;
	cantVent=document.getElementById("cantVent").value;				
	
	//codigo para tabla peps

	if (parseFloat(array_cantComp[0].toPrecision(3))==parseFloat(cantVent)){		
		//listo
		var q = new Array();
		q=array_costComp.pop();
		array_cantComp.pop();				
		costVent=parseFloat(q);
		totalVent1=parseFloat(cantVent)*parseFloat(costVent);
		array_totalVenta.push(totalVent1);
		sumCantSaldo1-=parseFloat(cantVent);		
		sumTotalSaldo1-=parseFloat(totalVent1);
		sumTotalSaldo21=sumTotalSaldo1;
	}else{
		var a=0;
		if (parseFloat(array_cantComp[0].toPrecision(3))>=parseFloat(cantVent)){
			a=1;
		}else{
			a=2;
		}
		switch(a){
			case 1:		
				//listo						
				if ((parseFloat(array_cantComp[0].toPrecision(3))-cantVent)>0){				
					if (sumTotalSaldo1<=0){
					}else{
					var p = new Array();
					p = array_cantComp.pop();
					var nuevaCant = p-cantVent;
					array_cantComp.unshift(nuevaCant);
					var q = new Array();
					q=array_costComp.pop();
					costVent=parseFloat(q);
					totalVent1=parseFloat(cantVent)*parseFloat(costVent);
					array_totalVenta.unshift(totalVent1);
					array_costComp.push(q);
					sumCantSaldo1-=parseFloat(cantVent);
					array_cantSaldo.shift();					
					sumTotalSaldo1-=parseFloat(totalVent1);
					array_totalSaldo.pop();								
					sumTotalSaldo21=sumTotalSaldo1;
					}
				}else{
					if (array_cantComp[0]==0){
						array_cantComp.pop();
					}
					var p = new Array();
					p = array_cantComp.pop();
					var q = new Array();
					q=array_costComp.pop();
					var total1=parseFloat(p)*parseFloat(q);
					var diferencia = p-cantVent;
					var s = new Array();
					s=array_costComp.pop();
					var total2=(-(diferencia))*parseFloat(s);
					var k = new Array();
					k=array_cantComp.pop();
					var nuevaCant= parseFloat(k)-(-(diferencia));
					array_cantComp.unshift(nuevaCant);
					costVent=0;
					totalVent1=total1+total2;
					array_totalVenta.unshift(totalVent1);					
					sumCantSaldo1-=parseFloat(cantVent);				
					array_cantSaldo.shift();
					array_totalSaldo.shift();
					sumTotalSaldo1-=parseFloat(totalVent1);
					sumTotalSaldo21=sumTotalSaldo1;
				}				
			break;
			case 2:		
			//listo		
			if(parseFloat(array_cantComp[0].toPrecision(3))==parseFloat(cantVent)){
				var q = new Array();
				q=array_costComp.pop();
				array_cantComp.pop();				
				costVent=parseFloat(array_costComp[0].toPrecision(3));
				totalVent1=parseFloat(cantVent)*parseFloat(costVent);
				array_totalVenta.push(totalVent1);
				sumCantSaldo1-=parseFloat(cantVent);		
				sumTotalSaldo1-=parseFloat(totalVent1);
				sumTotalSaldo21=sumTotalSaldo1;	
			}else{							
				var p = new Array();
				p = array_cantComp.pop();
				var q = new Array();
				q=array_costComp.pop();
				total1=parseFloat(p)*parseFloat(q);
				var diferencia = p-cantVent;
				var diferenciaPositiva=(-(diferencia));
				var k= new Array();
				k= array_cantComp.pop();
				var nuevaCant=parseFloat(k)-(diferenciaPositiva);				
				array_cantComp.push(nuevaCant);				
				var l= new Array();
				l=array_costComp.pop();
				total2=parseFloat(diferenciaPositiva)*parseFloat(l);
				array_costComp.push(l);				
				costVent=0;				
				totalVent1=((total1)+(total2));
				sumCantSaldo1-=parseFloat(cantVent);				
				array_cantSaldo.shift();
				sumTotalSaldo1-=parseFloat(totalVent1);
				sumTotalSaldo21=sumTotalSaldo1;
			}
			break;
		};
	}	

	var name_table=document.getElementById("tabla_inventario");
	var rowCount = name_table.rows.length;
    var row = name_table.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10);    

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent1.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo1+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo21.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';

	//codigo para tabla ueps
	
	if (parseFloat(array_cantComp2[0].toPrecision(3))==parseFloat(cantVent)){		
		//listo
		var q = new Array();
		q=array_costComp2.shift();
		q=array_costComp2.shift();
		array_cantComp2.shift();				
		costVent2=parseFloat(q);
		totalVent2=parseFloat(cantVent)*parseFloat(costVent2);
		array_totalVenta.push(totalVent2);
		sumCantSaldo2-=parseFloat(cantVent);		
		sumTotalSaldo2-=parseFloat(totalVent2);
		sumTotalSaldo22=sumTotalSaldo2;
	}else{
		var a=0;
		if (parseFloat(array_cantComp2[0].toPrecision(3))>=parseFloat(cantVent)){
			a=1;
		}else{
			a=2;
		}
		switch(a){
			case 1:		
				//listo						
				if ((parseFloat(array_cantComp2[0].toPrecision(3))-cantVent)>0){				
					if (sumTotalSaldo2<=0){
					}else{
					var p = new Array();
					p = array_cantComp2.shift();
					var nuevaCant = p-cantVent;
					array_cantComp2.push(nuevaCant);
					var q = new Array();
					q=array_costComp2.shift();
					costVent2=parseFloat(q);
					totalVent2=parseFloat(cantVent)*parseFloat(costVent2);
					array_totalVenta.unshift(totalVent2);
					array_costComp2.push(q);
					sumCantSaldo2-=parseFloat(cantVent);
					array_cantSaldo2.shift();					
					sumTotalSaldo2-=parseFloat(totalVent2);
					array_totalSaldo2.shift();								
					sumTotalSaldo22=sumTotalSaldo2;
					}
				}else{
					if (array_cantComp2[0]==0){
						array_cantComp2.shift();
					}					 					
					var p = new Array();
					p = array_cantComp2.pop();
					var q = new Array();
					q=array_costComp2.pop();
					var total1=parseFloat(p)*parseFloat(q);
					var diferencia = p-cantVent;
					var s = new Array();
					s=array_costComp2.pop();
					var total2=(-(diferencia))*parseFloat(s);
					var k = new Array();
					k=array_cantComp2.pop();
					var nuevaCant= parseFloat(k)-(-(diferencia));
					array_cantComp2.unshift(nuevaCant);
					costVent=0;
					totalVent2=total1+total2;
					array_totalVenta.unshift(totalVent2);					
					sumCantSaldo2-=parseFloat(cantVent);				
					array_cantSaldo2.shift();
					array_totalSaldo2.shift();
					sumTotalSaldo2-=parseFloat(totalVent2);
					sumTotalSaldo22=sumTotalSaldo2;
				}				
			break;
			case 2:		
			//listo		
			if(parseFloat(array_cantComp2[0].toPrecision(3))==parseFloat(cantVent)){
				var q = new Array();
				q=array_costComp2.pop();
				array_cantComp2.pop();				
				costVent2=parseFloat(array_costComp2[0].toPrecision(3));
				totalVent2=parseFloat(cantVent)*parseFloat(costVent2);
				array_totalVenta.push(totalVent2);
				sumCantSaldo2-=parseFloat(cantVent);		
				sumTotalSaldo2-=parseFloat(totalVent2);
				sumTotalSaldo22=sumTotalSaldo2;	
			}else{							
				var p = new Array();
				p = array_cantComp2.shift();
				var q = new Array();
				q=array_costComp2.shift();
				total1=parseFloat(p)*parseFloat(q);
				var diferencia = p-cantVent;
				var diferenciaPositiva=(-(diferencia));
				var k= new Array();
				k= array_cantComp2.shift();
				var nuevaCant=parseFloat(k)-(diferenciaPositiva);				
				array_cantComp2.push(nuevaCant);				
				var l= new Array();
				l=array_costComp2.shift();
				total2=parseFloat(diferenciaPositiva)*parseFloat(l);
				array_costComp2.push(l);				
				costVent=0;				
				totalVent2=((total1)+(total2));
				sumCantSaldo2-=parseFloat(cantVent);				
				array_cantSaldo2.shift();
				sumTotalSaldo2-=parseFloat(totalVent2);
				sumTotalSaldo22=sumTotalSaldo2;
			}
			break;
		};
	}

	var name_table2=document.getElementById("tabla_inventario2");
	var rowCount = name_table2.rows.length;
    var row = name_table2.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10);    

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent2+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent2.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo2+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo22.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';
	
	costVent3=parseFloat(costSaldo3);

	totalVent3=parseFloat(cantVent)*parseFloat(costVent3);
	sumCantSaldo3-=parseFloat(cantVent);
	sumTotalSaldo3-=parseFloat(totalVent3);
	

	var name_table3=document.getElementById("tabla_inventario3");
	var rowCount = name_table3.rows.length;
    var row = name_table3.insertRow(rowCount-2);
	var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10 = row.insertCell(9);
	var cell11 = row.insertCell(10);    

	cell1.innerHTML = '<p name="fecha_p[]" class="non-margin">'+fecha+'</p>';
	cell2.innerHTML = '<p name="cantComp_p[]" class="non-margin">'+cantComp+'</p>';
    cell3.innerHTML = '<p name="costComp_p[]" class="non-margin">'+costComp+'</p>';
    cell4.innerHTML = '<p name="totalComp_p[]" class="non-margin">'+totalComp.toPrecision(3)+'</p>';
    cell5.innerHTML = '<p name="cantVent_p[]" class="non-margin">'+cantVent+'</p>';
    cell6.innerHTML = '<p name="costVent_p[]" class="non-margin">'+costVent3+'</p>';
	cell7.innerHTML = '<p name="totalVent_p[]" class="non-margin">'+totalVent3.toPrecision(3)+'</p>';
	cell8.innerHTML = '<p name="cantSaldo_p[]" class="non-margin">'+sumCantSaldo3+'</p>';
	cell9.innerHTML = '<p name="costoSaldo_p[]" class="non-margin">'+costoSaldo+'</p>';
	cell10.innerHTML = '<p name="totalSaldo_p[]" class="non-margin">'+sumTotalSaldo3.toPrecision(3)+'</p>'; 
	cell11.innerHTML = '<span class="icon fa-edit"></span><span class="icon fa-eraser"></span>';

    //Para calcular los totales enviando los parametros
	calculateTotals(cantComp, costComp, totalComp, cantVent, costVent, totalVent1,1);	
    //Para calcular los totales sin enviar los parametros, solo adquiriendo los datos de la columna con mismo tipo de datos
	//calculateTotalsBySumColumn()
}

function calculateTotalsBySumColumn(){
	var total_cantComp1=0;
	var array_cantComp1=document.getElementsByName("cantComp_p[]");
	for (var i=0; i<array_cantComp1.length; i++) {
		total_cantidad+=parseFloat(array_cantComp1[i].innerHTML);
	}
	document.getElementById("total_cantComp1").innerHTML=total_cantComp1;


	var total_cantComp1=0;
	var array_totalComp1=document.getElementsByName("totalComp_p[]");
	for (var i=0; i<array_totalComp1.length; i++) {
		subtotales+=parseFloat(array_totalComp1[i].innerHTML);
	}
	document.getElementById("total_totalComp1").innerHTML=totalComp1;


	var total_cantVent=0;
	var array_cantVent=document.getElementsByName("cantVent_p[]");
	for (var i=0; i<array_cantVent.length; i++) {
		total_impuesto+=parseFloat(array_cantVent[i].innerHTML);
	}
	document.getElementById("total_cantVent1").innerHTML=total_cantVent.toPrecision(3);


	var totales_totalVent=0;
	var array_totalVent=document.getElementsByName("totalVent_p[]");
	for (var i=0; i<array_totalVent.length; i++) {
		totales_n+=parseFloat(array_totalVent[i].innerHTML);
	}
	document.getElementById("total_totalVent1").innerHTML=totales_totalVent.toPrecision(3);
	
}



function calculateTotals(cantComp, costComp, totalComp, cantVent, costVent, TotalVent, accion){
	//funcTotalsConParametro(cantidad, precio,subtotal,impuesto,total_n);
	var t_cantComp=parseFloat(document.getElementById("total_cantComp1").innerHTML);
	var t_costComp=0.00;
	var t_totalComp=parseFloat(document.getElementById("total_totalComp1").innerHTML);
	var t_cantVent=parseFloat(document.getElementById("total_cantVent1").innerHTML);
	var t_costVent=0.00;
	var t_TotalVent=parseFloat(document.getElementById("total_totalVent1").innerHTML);	

	//accion=1		Sumarle al los totales
	//accion=2		Restarle al los totales
	if (accion==1) {
		document.getElementById("total_cantComp1").innerHTML=parseFloat(t_cantComp.toPrecision(3))+parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio1").innerHTML=0;
		document.getElementById("total_totalComp1").innerHTML=parseFloat(t_totalComp.toPrecision(3))+parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent1").innerHTML=parseFloat(t_cantVent.toPrecision(3))+parseFloat(cantVent);
		document.getElementById("total_total1").innerHTML=0;
		document.getElementById("total_totalVent1").innerHTML=parseFloat(t_TotalVent.toPrecision(3))+parseFloat(TotalVent.toPrecision(3));
		
		document.getElementById("total_cantComp2").innerHTML=parseFloat(t_cantComp.toPrecision(3))+parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio2").innerHTML=0;
		document.getElementById("total_totalComp2").innerHTML=parseFloat(t_totalComp.toPrecision(3))+parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent2").innerHTML=parseFloat(t_cantVent.toPrecision(3))+parseFloat(cantVent);
		document.getElementById("total_total2").innerHTML=0;
		document.getElementById("total_totalVent2").innerHTML=parseFloat(t_TotalVent.toPrecision(3))+parseFloat(TotalVent.toPrecision(3));	

		document.getElementById("total_cantComp3").innerHTML=parseFloat(t_cantComp.toPrecision(3))+parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio3").innerHTML=0;
		document.getElementById("total_totalComp3").innerHTML=parseFloat(t_totalComp.toPrecision(3))+parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent3").innerHTML=parseFloat(t_cantVent.toPrecision(3))+parseFloat(cantVent);
		document.getElementById("total_total3").innerHTML=0;
		document.getElementById("total_totalVent3").innerHTML=parseFloat(t_TotalVent.toPrecision(3))+parseFloat(TotalVent.toPrecision(3));	
	}else if(accion==2){
		document.getElementById("total_cantComp1").innerHTML=parseFloat(t_cantComp.toPrecision(3))-parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio1").innerHTML=0;
		document.getElementById("total_totalComp1").innerHTML=parseFloat(t_totalComp.toPrecision(3))-parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent1").innerHTML=parseFloat(t_cantVent.toPrecision(3))-parseFloat(cantVent);
		document.getElementById("total_total1").innerHTML=0;
		document.getElementById("total_totalVent1").innerHTML=parseFloat(t_TotalVent.toPrecision(3))-parseFloat(TotalVent.toPrecision(3));	
		
		document.getElementById("total_cantComp2").innerHTML=parseFloat(t_cantComp.toPrecision(3))-parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio2").innerHTML=0;
		document.getElementById("total_totalComp2").innerHTML=parseFloat(t_totalComp.toPrecision(3))-parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent2").innerHTML=parseFloat(t_cantVent.toPrecision(3))-parseFloat(cantVent);
		document.getElementById("total_total2").innerHTML=0;
		document.getElementById("total_totalVent2").innerHTML=parseFloat(t_TotalVent.toPrecision(3))-parseFloat(TotalVent.toPrecision(3));

		document.getElementById("total_cantComp3").innerHTML=parseFloat(t_cantComp.toPrecision(3))-parseFloat(cantComp.toPrecision(3));
		document.getElementById("total_precio3").innerHTML=0;
		document.getElementById("total_totalComp3").innerHTML=parseFloat(t_totalComp.toPrecision(3))-parseFloat(totalComp.toPrecision(3));
		document.getElementById("total_cantVent3").innerHTML=parseFloat(t_cantVent.toPrecision(3))-parseFloat(cantVent);
		document.getElementById("total_total3").innerHTML=0;
		document.getElementById("total_totalVent3").innerHTML=parseFloat(t_TotalVent.toPrecision(3))-parseFloat(TotalVent.toPrecision(3));
	}else{
		alert('Accion Invalida');
	}
}



function format(input)
{
	var num = input.value.replace(/\,/g,'');
	if(!isNaN(num)){
		input.value = num;
	}
	else{ alert('Solo se permiten numeros');
		input.value = input.value.replace(/[^\d\.]*/g,'');
	}
}

