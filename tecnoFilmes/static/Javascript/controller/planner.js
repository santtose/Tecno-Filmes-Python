//Paginação Sugestão
var HZperPage = 10,//number of results per page
HZwrapper = 'paginationTable',//wrapper class
HZlines   = 'tableItem',//items class
HZpaginationId ='pagination-container',//id of pagination container
HZpaginationArrowsClass = 'paginacaoCursor',//set the class of pagi
HZpaginationColorDefault =  '#60BBAC',//default color for the pagination numbers
HZpaginationColorActive = '#049278', //color when page is clicked
HZpaginationCustomClass = 'customPagination'; //custom class for styling the pagination (css)
function paginacao(){
    function paginationShow(){
        if($("#" + HZpaginationId).children().length > 10){
   
           var a = $(".activePagination").attr("data-valor");
   
           if(a >= 4){
               var i = parseInt(a) - 3, o = parseInt(a) + 2;
               $(".paginacaoValor").hide(),
               $(".paginacaoValor").slice(i,o).show()
           }else 
               $(".paginacaoValor").hide(),
               $(".paginacaoValor").slice(0,5).show()
   
       }}
       paginationShow(),$("#beforePagination").hide(),$("." + HZlines).hide();
   
       for(var tamanhotabela=$("." + HZwrapper).children().length,porPagina = HZperPage,paginas = Math.ceil(tamanhotabela/porPagina),i = 1; i <= paginas;)
   
       $("#"+HZpaginationId).append("<p class='paginacaoValor " + HZpaginationCustomClass + "' data-valor=" + i + ">" + i + "</p>"),
           i++,$(".paginacaoValor").hide(),$(".paginacaoValor").slice(0,5).show();
   
       $(".paginacaoValor:eq(0)").css("background","" + HZpaginationColorActive).addClass("activePagination");
      
       var exibir = $("." + HZlines).slice(0,porPagina).show();
   
       $(".paginacaoValor").on("click",function(){
           
           $(".paginacaoValor").css("background","" + HZpaginationColorDefault).removeClass("activePagination"),
           $(this).css("background","" + HZpaginationColorActive).addClass("activePagination");
   
           var a = $(this).attr("data-valor"),
               i = a * porPagina,
               o = i - porPagina;
   
           $("." + HZlines).hide(),
               exibir = $("." + HZlines).slice(o,i).show(),
               "1" === a ? $("#beforePagination").hide(): $("#beforePagination").show(),
               a === "" + $(".paginacaoValor:last").attr("data-valor")?$("#afterPagination").hide(): $("#afterPagination").show(),
               paginationShow()
       }),
       $(".paginacaoValor").last().after($("#afterPagination")),
       $("#beforePagination").on("click",function(){
   
           var a = $(".activePagination").attr("data-valor"),
           i = parseInt(a) - 1;
           $("[data-valor=" + i + "]").click(),
           paginationShow()
   
       }),
       $("#afterPagination").on("click",function(){
   
           var a = $(".activePagination").attr("data-valor"),
           i = parseInt(a) + 1;
           $("[data-valor=" + i + "]").click(),
           paginationShow()
   
       }),
           $(".paginacaoValor").css("float","left"),
           $("." + HZpaginationArrowsClass).css("float","left");
   
}

//Paginação Em Atendimento
var HZperPageAt = 10,//number of results per page
HZwrapperAt = 'paginationTableAt',//wrapper class
HZlinesAt   = 'tableItemAt',//items class
HZpaginationIdAt ='pagination-container-at',//id of pagination container
HZpaginationArrowsClassAt = 'paginacaoCursorAt',//set the class of pagi
HZpaginationColorDefaultAt =  '#60BBAC',//default color for the pagination numbers
HZpaginationColorActiveAt = '#049278', //color when page is clicked
HZpaginationCustomClassAt = 'customPaginationAt'; //custom class for styling the pagination (css)
function paginacaoAt(){
    function paginationShow(){
        if($("#" + HZpaginationId).children().length > 10){
   
           var a = $(".activePaginationAt").attr("data-valor");
   
           if(a >= 4){
               var i = parseInt(a) - 3, o = parseInt(a) + 2;
               $(".paginacaoValorAt").hide(),
               $(".paginacaoValorAt").slice(i,o).show()
           }else 
               $(".paginacaoValorAt").hide(),
               $(".paginacaoValorAt").slice(0,5).show()
   
       }}
       paginationShow(),$("#beforePaginationAt").hide(),$("." + HZlinesAt).hide();
   
       for(var tamanhotabela=$("." + HZwrapperAt).children().length,porPagina = HZperPageAt,paginas = Math.ceil(tamanhotabela/porPagina),i = 1; i <= paginas;)
   
       $("#"+HZpaginationIdAt).append("<p class='paginacaoValorAt " + HZpaginationCustomClassAt + "' data-valor=" + i + ">" + i + "</p>"),
           i++,$(".paginacaoValorAt").hide(),$(".paginacaoValorAt").slice(0,5).show();
   
       $(".paginacaoValorAt:eq(0)").css("background","" + HZpaginationColorActiveAt).addClass("activePaginationAt");
      
       var exibir = $("." + HZlinesAt).slice(0,porPagina).show();
   
       $(".paginacaoValorAt").on("click",function(){
           
           $(".paginacaoValorAt").css("background","" + HZpaginationColorDefaultAt).removeClass("activePaginationAt"),
           $(this).css("background","" + HZpaginationColorActiveAt).addClass("activePaginationAt");
   
           var a = $(this).attr("data-valor"),
               i = a * porPagina,
               o = i - porPagina;
   
           $("." + HZlinesAt).hide(),
               exibir = $("." + HZlinesAt).slice(o,i).show(),
               "1" === a ? $("#beforePaginationAt").hide(): $("#beforePaginationAt").show(),
               a === "" + $(".paginacaoValorAt:last").attr("data-valor")?$("#afterPaginationAt").hide(): $("#afterPaginationAt").show(),
               paginationShow()
       }),
       $(".paginacaoValorAt").last().after($("#afterPaginationAt")),
       $("#beforePaginationAt").on("click",function(){
   
           var a = $(".activePaginationAt").attr("data-valor"),
           i = parseInt(a) - 1;
           $("[data-valor=" + i + "]").click(),
           paginationShow()
   
       }),
       $("#afterPaginationAt").on("click",function(){
   
           var a = $(".activePaginationAt").attr("data-valor"),
           i = parseInt(a) + 1;
           $("[data-valor=" + i + "]").click(),
           paginationShow()
   
       }),
           $(".paginacaoValorAt").css("float","left"),
           $("." + HZpaginationArrowsClassAt).css("float","left");
   
}

// Filtros
var countOrng = $('.cont-orng-sugestao a p').length
var countOrngAtendimento = $('.cont-orng-atendimento a p').length

var sugestaoCont = $('.contador').attr('data-conta');
$('.contador').text('Sugestão (' + sugestaoCont + ')');

var atendimentoCont = $('.contador-b').attr('data-conta')
$('.contador-b').text('Em Atendimento (' + atendimentoCont + ')');

$('#at-dia').click(function(){

    if($(this).attr('src') == '../../static/icons/atvdia.png')
        $(this).attr('src', '../../static/icons/atvdiaclick.png')
    else
        $(this).attr('src','../../static/icons/atvdia.png')

    $('.borda').toggle()

    if($(this).attr('src') == '../../static/icons/atvdiaclick.png' && countOrng < 10){
        $('.esconde').hide()
    }else{
        $('.esconde').show()
    }

    if($('.esconde').css('display') == 'none'){
        $('.borda').hide()
    }

    if($('.esconde').css('display') == 'block'){
        paginacao()
    }

    if($('#pro-dias').attr('src') == ('../../static/icons/pro5diasclick.png')){
        $('.borda_orng').hide()
    }

    if($('#at-dia').attr('src') == ('../../static/icons/atvdiaclick.png') && countOrngAtendimento < 10){
        $('.escondeAt').hide()
    }


    $('.borda').each(function(){
        if ($(this).css('display') == 'none' && $('.borda_orng').css('display') == 'block') {

            let result = (sugestaoCont - sugestaoCont) + countOrng
            $('.contador').text('Sugestão (' + result + ')')

        }else if($(this).css('display') == 'none' && $('.borda_orng').css('display') == 'none'){

            let result = (sugestaoCont - sugestaoCont)
            $('.contador').text('Sugestão (' + result + ')')

        }else if($(this).css('display') == 'block' && $('.borda_orng').css('display') == 'none'){

            let result = (sugestaoCont - countOrng)
            $('.contador').text('Sugestão (' + result + ')')

        }else{
            $('.contador').text('Sugestão (' + sugestaoCont + ')')
        }
    })

    $('.borda').each(function(){
        if ($(this).css('display') == 'none' && $('.borda_orng').css('display') == 'block'){

            let result = (atendimentoCont - atendimentoCont) + countOrngAtendimento
            $('.contador-b').text('Em Atendimento (' + result + ')')

        }else if($(this).css('display') == 'none' && $('.borda_orng').css('display') == 'none'){

            let result = (atendimentoCont - atendimentoCont)
            $('.contador-b').text('Em Atendimento (' + result + ')')

        }else if($(this).css('display') == 'block' && $('.borda_orng').css('display') == 'none'){

            let result = (atendimentoCont - countOrngAtendimento)
            $('.contador-b').text('Em Atendimento (' + result + ')')

        }else{
            $('.contador-b').text('Em Atendimento (' + atendimentoCont + ')')
        }
    })

});

if(atendimentoCont < 10 && countOrngAtendimento < 10){
    $('.escondeAt').hide()
}else{
    $('.escondeAt').show()
}

$('#pro-dias').click(function(){
    if($(this).attr('src') == '../../static/icons/pro5dias.png')
        $(this).attr('src', '../../static/icons/pro5diasclick.png')
    else
        $(this).attr('src','../../static/icons/pro5dias.png')

    $('.borda_orng').toggle()

    if(atendimentoCont > 10){
        if($(this).attr('src') == '../../static/icons/pro5diasclick.png' && atendimentoCont < 10){
            $('.escondeAt').hide()
        }else{
            $('.escondeAt').show()
        }

        if($('.escondeAt').css('display') == 'none'){
            $('.borda_orng').hide()
        }
    
        if($('.escondeAt').css('display') == 'block'){
            paginacaoAt()
        }
    
        if($('#at-dia').attr('src') == ('../../static/icons/atvdiaclick.png')){
            $('.borda').hide()
        }

    }    

    $('.borda_orng').each(function(){
        if ($(this).css('display') == 'none' && $('.borda').css('display') == 'block'){

            let result = (sugestaoCont - countOrng)
            $('.contador').text('Sugestão (' + result + ')')

        }else if($(this).css('display') == 'none' && $('.borda').css('display') == 'none'){

            let result = (countOrng - countOrng)
            $('.contador').text('Sugestão (' + result + ')')

        }else if($(this).css('display') == 'block' && $('.borda').css('display') == 'none'){

            let result = countOrng
            $('.contador').text('Sugestão (' + result + ')')

        }else{
            $('.contador').text('Sugestão (' + sugestaoCont + ')')
        }
    })

    $('.borda_orng').each(function(){
        if ($(this).css('display') == 'none' && $('.borda').css('display') == 'block'){

            let result = (atendimentoCont - countOrngAtendimento)
            $('.contador-b').text('Em Atendimento (' + result + ')')

        }else if($(this).css('display') == 'none' && $('.borda').css('display') == 'none'){

            let result = (countOrngAtendimento - countOrngAtendimento)
            $('.contador-b').text('Em Atendimento (' + result + ')')

        }else if($(this).css('display') == 'block' && $('.borda').css('display') == 'none'){

            let result = (countOrngAtendimento)
            $('.contador-b').text('Em Atendimento (' + result + ')')
            
        }else{
            $('.contador-b').text('Em Atendimento (' + atendimentoCont + ')')
        }
    })

});

$('#em-prod').click(function(){
    if($(this).attr('src') == '../../static/icons/emprod.png')
        $(this).attr('src', '../../static/icons/emprodclick.png')
    else
        $(this).attr('src','../../static/icons/emprod.png')

    $('.hide-prod').toggle()
});


paginacao()
paginacaoAt()