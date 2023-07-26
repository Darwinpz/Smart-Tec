$(document).ready(function () {
    var table = $('#table_histories').DataTable({
        "ajax": {
            "url": "/principal/ver_histories",
            "method": "post"
        },
        "columns": [
            {"data":"_id"},
            {"data":"tipo"},
            {"data":"mensaje"},
            { "data": "cedula"},
            { "data": "rol"},
            {"data":"fecha_accion"},
            { "data": null }
        ],
        "createdRow": function (row, data, index) {
            if (data.tipo == "CORRECTO") {
                $(row).addClass("text-success fw-bold")
            }else{
                $(row).addClass("text-danger fw-bold")
            }

        },
        "columnDefs": [
            {
                target: 0,
                visible: false,
                searchable: false,
            },
            {
                "targets": -1,
                "data": null,
                "defaultContent": '<a type="button" class="btn btn-primary btn-ver-histories" ><i class="fas fa-eye"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });

    $('#table_histories tbody').on('click', '.btn-ver-histories', function () {
        var data = table.row($(this).parents('tr')).data();
       
        $('#historyModal').modal("show");
        
    });


});


$('#historyModal').on('show.bs.modal', function (event) {

    
    form.reset();

});
