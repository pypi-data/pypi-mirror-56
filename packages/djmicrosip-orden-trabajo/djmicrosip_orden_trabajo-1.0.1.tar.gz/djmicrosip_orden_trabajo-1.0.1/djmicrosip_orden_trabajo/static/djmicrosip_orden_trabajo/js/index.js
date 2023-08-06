$(document).ready(function(){
	$( ".progress-item" ).each(function() {
		var width=$(this).attr("data-width");
		console.log(width)
	
		$(this).css("width",width);
		if(width=="25%")
		{$(this).css("background-color","#dc3545");}
		else if(width=="50%")
		{$(this).css("background-color","#ff9007");}
		else if(width=="75%")
		{$(this).css("background-color","#ffc107");}
		else
		{$(this).css("background-color","#28a745");}

	});
	$( "[name*='vendedor']" ).each(function() {
		$(this).addClass("hidden");
		var number=$(this).parent().attr("id");
		$(this).addClass("pedido"+number);
	});
	$("#menu").hide();
});
$('#id_llamada').change(function() {
	$('.form').submit();
});
$( ".asignar" ).click(function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  console.log($(".pedido"+number).attr('id'))
  $(".pedido"+number).removeClass("hidden");
  $(".btncancel"+number).removeClass("hidden");
  $(".vendedor_asign").addClass("hidden");

 
});
$( ".cancelar" ).click(function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  $(".pedido"+number).addClass("hidden");
  $(".asign"+number).removeClass("hidden");
  $(".btn"+number).addClass("hidden");
  $(".vendedor_asign"+number).removeClass("hidden");
 
});
$( ".guardar" ).click(function() {
	var id_crm=$(this).attr("id");
	var id_cliente=$(".pedido"+id_crm).val();

	console.log(id_crm,id_cliente);
	
 	if(id_crm && id_vendedor)
	{
		$.ajax({
		url: '/pedidos/vendedor_asignar/',
		type: 'get',
		data: {
			'id_vendedor': id_cliente,
			'id_crm':id_crm,
		},
		success: function (data) {
				if(data.mensaje=="Guardado")
				{location.reload();}
				else
				{alert(data.mensaje)}				
			}
		});
	}
 
});
function progreso_(id_crm,progreso)
{
		if(progreso=="0")
	{
		$(this).addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .change_state").html('Inicio <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
	}	
	else if(progreso=="25")
	{
		$(this).addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .change_state").html('Finalizado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ccc");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Recibido');
	}
	else if(progreso=="50")
	{
		$(this).addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .change_state").html('Aviso a cliente <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Inicio');
	}
	else if(progreso=="75")
	{
		$(this).addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#28a745");
		$("#change_state"+id_crm+" .change_state").html('Entregado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Finalizado');
	}
	else{
		$(this).addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Aviso a cliente');
	}
}
$( ".progress" ).on("touchstart",function(){
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);
});

$( ".progress" ).dblclick(function() {
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);


	//alert(id_crm)

});

$( ".change_state" ).click(function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/change_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{location.reload();}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$( ".return_state" ).click(function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/return_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{location.reload();}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$("[name*='vendedor']").on("change",function(){
	var valor=$(this).val();
	var number=$(this).parent().attr("id");
	if(valor != '')
	{	
		$(".btn"+number).removeClass("hidden");
	}
	else
	{$(".btn"+number).addClass("hidden");}
});
$( ".more" ).click(function() {
	var id_doc=$(this).attr("id");
	if($(this).hasClass("glyphicon-triangle-right"))
	{
		$(this).removeClass("glyphicon-triangle-right");
		$(this).addClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).removeClass("hidden");
		$('.det'+id_doc+' #contenido').empty();


		$.ajax({
		url: '/pedidos/get_detalles/',
		type: 'get',
		data: {
			'id_doc': id_doc,
		},
		success: function (data) {
				
				for (var i = 0; i <= data.length-1; i++) {
					console.log(data[i]);
					var html='<div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].unidades+'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].articulo +'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].notas+'</div></div>'
					console.log(html)
					$('.det'+id_doc+' #contenido').append(html);
				}
			}
		});
	}
	else
	{
		$(this).addClass("glyphicon-triangle-right");
		$(this).removeClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).addClass("hidden");
	}
});
$( ".det_progreso" ).click(function() {
	var id_crm=$(this).attr("id");
	$("#tiempo_espera").html('');
	$("#tiempo_fin").html('');
	$("#tiempo_aviso").html('');
	$("#tiempo_entrega").html('');
	if (id_crm)
	{
		$.ajax({
		url: '/pedidos/get_tiempos/',
		type: 'get',
		data: {
			'id_crm': id_crm,
		},
		success: function (data) {

					if(data)
					{	
						if(data.tiempo_espera)
						{$("#tiempo_espera").html(data.tiempo_espera);}
						if(data.tiempo_fin)
						{$("#tiempo_fin").html(data.tiempo_fin);}
						if(data.tiempo_aviso)
						{$("#tiempo_aviso").html(data.tiempo_aviso);}
						if(data.tiempo_entrega)	
						{$("#tiempo_entrega").html(data.tiempo_entrega);}
					}
			}
		});
	}

});