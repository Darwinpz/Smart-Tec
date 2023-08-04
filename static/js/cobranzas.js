
$(document).ready(function () {
    var table = $('#table_cobranzas').DataTable({
        "ajax": {
            "url": "/principal/ver_cobranzas",
            "method": "post"
        },
        "columns": [
            {"data":"_id"},
            { "data": "placa" },
            { "data": "ingreso" },
            { "data": "salida" },
            { "data": "total" },
            { "data": null }
        ],
        "columnDefs": [
            {
                target: 0,
                visible: false,
                searchable: false,
            },
            {
                "targets": -1,
                "data": null,
                "defaultContent": '<a type="button" class="btn btn-primary btn-ver-cobranzas" ><i class="fas fa-eye"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });


    $('#table_cobranzas tbody').on('click', '.btn-editar-cobranzas', function () {
        var data = table.row($(this).parents('tr')).data();
       
        $('#pisoModal').modal("show");

        let form = document.getElementById("form_piso");
    
        document.getElementById("pisoModalLabel").innerHTML = "<b>Editar piso</b>"

        document.getElementById("save-piso").style = "display:none"
        document.getElementById("edit-piso").style = "display:visible"

        document.getElementById("p_nombre").value = data.nombre  

        document.getElementById("p_codigo").value = data._id

        form.setAttribute("action","/principal/edit_piso")
        
    });


});



$('#pisoModal').on('show.bs.modal', function (event) {

    let form = document.getElementById("form_piso");
    let mensaje = document.getElementById("mensaje_piso");

    mensaje.innerText = ""

    document.getElementById("pisoModalLabel").innerHTML = "<b>Agregar piso</b>"

    document.getElementById("save-piso").style = "display:visible"
    document.getElementById("edit-piso").style = "display:none"

    form.setAttribute("action","/principal/save_cobranzas")
 
    form.reset();

});


