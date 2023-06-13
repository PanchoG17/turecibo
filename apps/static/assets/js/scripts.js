$(document).ready(()=>{

    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
    let username = $('#username').val()

    $('.btn-visualizar').click(function(){
        let id_recibo = this.value
        let periodo = $(this).parent().parent().find('.periodo').html().toUpperCase().trim();
        let anio = $(this).parent().parent().find('.anio').html().toUpperCase().trim();

        $.post( '/generate_pdf', { id_recibo : id_recibo , csrfmiddlewaretoken : csrftoken }
        )
        .done(function( data ) {
            window.location.href = `/view_pdf/${data.id}/${username}-${periodo}_${anio}`;
        })
        .fail(function() {
            alert( "server error" );
        })
    })

    $('.btn-descargar').click(function(){
        let id_recibo = this.value
        let periodo = $(this).parent().parent().find('.periodo').html().toUpperCase().trim();
        let anio = $(this).parent().parent().find('.anio').html().toUpperCase().trim();

        $.post( '/generate_pdf', { id_recibo : id_recibo , csrfmiddlewaretoken : csrftoken }
        )
        .done(function( data ) {
            window.location.href = `/download_pdf/${data.id}/${periodo}_${anio}`
        })
        .fail(function() {
            alert( "server error" );
        })
    })

    $('.btn-nomade').click(function(){

        let service = this.value
        $('#msg').empty().append("<div class='spinner-border text-primary' role='status'><span class='sr-only'>Loading...</span></div>")

        $.post( '/generate_nomade_pdf', { service : service , csrfmiddlewaretoken : csrftoken }
        )
        .done(function( data ) {
            if(data['msg'] == 'success'){
                $('#msg').empty()
                window.location.href = `/view_nomade_pdf/${username}_${service}`;
            }
            else{
                $('#msg').empty().append(data['msg'])
            }
        })
        .fail(function( data) {
            alert( "server error" );
        })
    })

    $('table tbody').on('click', '.btn-mail', function (){

        var parent = $(this).closest("tr").prev()
        if ($(parent).hasClass('parent')){
            var id_recibo = this.value
            var periodo = $(parent).find('.periodo').html().toUpperCase().trim();
            var escalafon = $(parent).find('.escalafon').html().toUpperCase().trim();
            var anio = $(parent).find('.anio').html().toUpperCase().trim();
        }
        else{
            var id_recibo = this.value
            var periodo = $(this).parent().parent().find('.periodo').html().toUpperCase().trim();
            var escalafon = $(this).parent().parent().find('.escalafon').html().toUpperCase().trim();
            var anio = $(this).parent().parent().find('.anio').html().toUpperCase().trim();
        }

        $('#msg').empty().append("<div class='spinner-border text-primary' role='status'><span class='sr-only'>Loading...</span></div>")
        $.post( '/enviar_mail', {
            csrfmiddlewaretoken : csrftoken,
            id_recibo : id_recibo,
            escalafon : escalafon,
            periodo : periodo,
            anio : anio
        })
        .done(function( data ) {
            $('#msg').empty().append(data['msg'])
        })
        .fail(function() {
            alert( "server error" );
        })

    } );

    $('table tbody').on('click', '.btn-banco', function (){

        var parent = $(this).closest("tr").prev()
        if ($(parent).hasClass('parent')){
            var id_recibo = this.value
            var periodo = $(parent).find('.periodo').html().toUpperCase().trim();
            var escalafon = $(parent).find('.escalafon').html().toUpperCase().trim();
            var anio = $(parent).find('.anio').html().toUpperCase().trim();
        }
        else{
            var id_recibo = this.value
            var periodo = $(this).parent().parent().find('.periodo').html().toUpperCase().trim();
            var escalafon = $(this).parent().parent().find('.escalafon').html().toUpperCase().trim();
            var anio = $(this).parent().parent().find('.anio').html().toUpperCase().trim();
        }

        $('#msg').empty().append("<div class='spinner-border text-primary' role='status'><span class='sr-only'>Loading...</span></div>")
        $.post( '/enviar_mail_banco', {
            csrfmiddlewaretoken : csrftoken,
            id_recibo : id_recibo,
            escalafon : escalafon,
            periodo : periodo,
            anio : anio
        })
        .done(function( data ) {
            $('#msg').empty().append(data['msg'])
        })
        .fail(function() {
            alert( "server error" );
        })

    } );

});