$(document).ready(function(){

    //ADD INGREDIENT
    var type_ing = $("#id_type_ingredient").val();
    $('#title-ingredient-information-form').hide();
    $('#div_id_ebc_min').hide();
    $('#div_id_ebc_max').hide();
    $('#div_id_attenuation_min').hide();
    $('#div_id_attenuation_max').hide();
    $('#div_id_acide_alpha').hide();

    //ADD INGREDIENT TO BRASSIN
    $('#div_id_temps_infusion').hide();

    if (type_ing == 'malt'){$('#div_id_ebc_min').show();$('#div_id_ebc_max').show();}
    if (type_ing == 'levure'){$('#div_id_attenuation_min').show();$('#div_id_attenuation_max').show();}
    if (type_ing == 'houblon'){$('#div_id_acide_alpha').show();}
    if (type_ing == 'autre'){$('#title-ingredient-information-form').hide();}
 
  //FILTER ON BRASSIN TABLE
  $("#Brassin-table-filter").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Brassin-table tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  //FILTER ON INGREDIENT TABLE
  $("#Ingredient-table-filter").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Ingredient-table tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  //FILTER ON ACHAT TABLE
  $("#Achat-table-filter").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Achat-table tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

    //FILTER ON VENTE TABLE
  $("#Vente-table-filter").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Vente-table tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  //INGREDIENT ADD FORM
  $("#id_type_ingredient").on('change', function() {
    var type_ing = $(this).val().toLowerCase();
    $('#title-ingredient-information-form').show();
    $('#div_id_ebc_min').hide();
    $('#div_id_ebc_max').hide();
    $('#div_id_attenuation_min').hide();
    $('#div_id_attenuation_max').hide();
    $('#div_id_acide_alpha').hide();

    if (type_ing == 'malt'){$('#div_id_ebc_min').show();$('#div_id_ebc_max').show();}
    if (type_ing == 'levure'){$('#div_id_attenuation_min').show();$('#div_id_attenuation_max').show();}
    if (type_ing == 'houblon'){$('#div_id_acide_alpha').show();}
    if (type_ing == 'autre'){$('#title-ingredient-information-form').hide();}
   });

  //INGREDIENT ADD FORM
  $("#id_ingredient").on('change', function() {
    var ing = $(this);
    $('#div_id_temps_infusion').hide();
    $('#id_quantite').prop("disabled", false);
    var text = $("option:selected",ing).text(); 
    if (text.match(/Levure.*/)) {$('#id_quantite').val(1);$('#id_quantite').prop("disabled", true);}
    if (text.match(/Houblon.*/)){$('#div_id_temps_infusion').show();}
   });

  //CALCULS RECETTE
  $("#volume_empatage_desire").on("keyup", function() {
    var v_empatage = $(this).val();
    var table=$("#table_ing_recette");
    var rowLength = $("#table_ing_recette tr").length;
    var taux_empatage =$("#taux_empatage").val();
    var masse_tot = taux_empatage*v_empatage
    //pour chaque ligne du tableau ingredients
    for (var i=1; i<rowLength; i+=1)
    {
      //calculer les quantités

      var percent = $('table tr:nth-child('+i+') td:nth-child(3)').text().substring(1, 3);
      var quantite = masse_tot*parseFloat(percent)/100 ;

      //écriture
      $('table tr:nth-child('+i+') td:nth-child(4)').text(quantite);
        
      //var ID_INGREDIENT=dataRow[1]; 
      //var TYPE=dataRow[0]; 
      
      //color case si pas assez de stock
      //var dataRow = table.DataTable().row(i).data();
      //$.ajax({url:"Recette_Ingredient_Get_Stock.php",method:"POST",data:{ID_INGREDIENT:ID_INGREDIENT,TYPE:TYPE},
      //  success:function(dataStock){if (table.find("tr:eq("+(i+1)+")").find("td:eq(3)").html()>dataStock[0]){table.find("tr:eq("+i+")").find("td:eq(3)").style.color="red"}}});
    }

  });

});

 function calc_quantites_ingredients(volume_empatage)
 {
  

  //pour chaque ligne du tableau ingredients
  for (var i=0; i<rowLength; i+=1)
  {
    //calculer les quantités
    var percent = table.rows[i].cells[2].innerHTML;
    var quantite = masse_tot*percent/100 ;

    //écriture
    table.find("tr:eq("+(i+1)+")").find("td:eq(3)").html(quantite); 
      
    //var ID_INGREDIENT=dataRow[1]; 
    //var TYPE=dataRow[0]; 
    
    //color case si pas assez de stock
    //var dataRow = table.DataTable().row(i).data();
    //$.ajax({url:"Recette_Ingredient_Get_Stock.php",method:"POST",data:{ID_INGREDIENT:ID_INGREDIENT,TYPE:TYPE},
    //  success:function(dataStock){if (table.find("tr:eq("+(i+1)+")").find("td:eq(3)").html()>dataStock[0]){table.find("tr:eq("+i+")").find("td:eq(3)").style.color="red"}}});
  }
  return;
 } 


//UPDATE °P / SG FORM
function calc_SG(str,input_name) 
{
  var id_input_to_update = input_name.substring(0,input_name.length-2);
  if (str.length > 0 && !isNaN(str)) 
    console.log('\"#' + id_input_to_update + '\"');
  { 
    $('#' + id_input_to_update).val(Math.round(conversion_P_D(str)*1000)/1000);
    return;
  } 
}

function conversion_P_D(P)
{
  var D = 1+P/(258.6-0.88*P);
  return D ;
}