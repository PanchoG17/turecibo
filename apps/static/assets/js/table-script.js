$(document).ready( function () {

    let user = $("#user").val();
    let dni = $("#dni").val();

    try{
        $('#recibos-completo').DataTable({
            responsive: true,
            info: false,
            autoWidth: false,
            pagingType: "full",
            order: [[4, 'desc'],[6, 'desc']],
            dom:
            '<"text-center pt-3 my-3"<"card border-primary mb-3"<"card-header"><"card-body"<"recibos-header" lf >>>><"#msg.text-center"><t><"d-flex pb-2 justify-content-center"p>',
            columnDefs: [
                { targets: '_all', orderable: false, className:"p-1" },
                { targets: [4,6], visible: false },
                { targets: [8,9,10,11], "width" : "25px", className:"custom-icons"},
                { targets: [2,7,10,11], className:"desktop" },
                { targets: [3], "width" : "80px",className:"anio" },
                { targets: [0], "width" : "30px", className:"not-desktop dtr-control" },
                { targets: [1], className:"min-tablet border-custom escalafon" },
                { targets: [3,5], className:"all" },
                { targets: [5], className:"periodo"},
                { targets: [8,9], className:"min-mobile-l" },
                { targets: [7], "render": function ( data, type, row, meta ) {
                    data = data.replace(',','.')
                    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'ARS' }).format(parseFloat(data))
                }
                }
            ],
            language: {
                search:         "Buscar:",
                lengthMenu:     "Mostrar recibos _MENU_",
                zeroRecords:    "No hay coincidencias",
                searchPlaceholder: "Escribe algo...",
                paginate: {
                    first:      '<i class="fa-solid fa-angles-left"></i>',
                    previous:   '<i class="fa-solid fa-angle-left"></i>',
                    next:       '<i class="fa-solid fa-angle-right"></i>',
                    last:       '<i class="fa-solid fa-angles-right"></i>',
                }
            },
            initComplete: function(settings, json) {
                $('.card-header').append(`<p><strong>Agente:</strong> ${user}</p>`)
                $('.card-header').append(`<strong>DNI:</strong> ${dni}`)
                $('#spin').hide();
                $('#menu-footer').show();
                $('.table-js').show();
            }
        });
    }
    catch(err){
        $('#spin').hide();
        $('#menu-footer').show();
        $('.table-js').show();
    }

    try{
        $('#recibos-home').DataTable({
            responsive: true,
            paging: false,
            info: false,
            searching: false,
            autoWidth: false,
            order: [[4, 'desc'],[6, 'desc']],
            columnDefs: [
                { targets: '_all', orderable: false, className:"p-0" },
                { targets: [4,6], visible: false },
                { targets: [8,9,10,11], "width" : "25px", className:"custom-icons"},
                { targets: [2,7,10,11], className:"desktop" },
                { targets: [3], "width" : "80px",className:"anio" },
                { targets: [0], "width" : "30px", className:"not-desktop dtr-control p-1" },
                { targets: [1], className:"min-tablet border-custom escalafon" },
                { targets: [3,5], className:"all" },
                { targets: [5], className:"periodo", "width":"120px" },
                { targets: [8,9], className:"min-mobile-l" },
                { targets: [7], "render": function ( data, type, row, meta ) {
                    data = data.replace(',','.')
                    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'ARS' }).format(parseFloat(data))
                }
                }
            ],
            initComplete: function(settings, json) {
                $('#spin').hide();
                $('.table-js').show();
                $('#menu-footer').show();
            }
        });
    }
    catch(err){
        $('#spin').hide();
        $('#menu-footer').show();
        $('.table-js').show();
    }

} );