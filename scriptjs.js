var texto = "";
	$("#view-as-wrapper article").each(function(){
		texto += $(this).find(".anunciante span").html() + ";";
		var elements = $(this).find("h2").html().split("\n");
		texto += elements[1].trim().substring(8, elements[1].trim().length - 9) + ";";
		texto += elements[2].trim() + ";";
		//texto += $(this).find("h2").html().trim() + ";";
		texto += $(this).find(".preco strong").html() + ";";
		if ($(this).find(".unstyled li").length > 0)
			texto += $(this).find(".icone-area").html().split("<")[0];
		texto = texto.substring(0,texto.length - 1);
		texto += "\n";
	});
	return texto;
