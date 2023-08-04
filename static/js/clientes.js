
$(document).ready(function () {
    var table = $('#table_clientes').DataTable({
        "ajax": {
            "url": "/principal/ver_clientes",
            "method": "post",
        },
        "columns": [
            { "data": "_id" },
            { "data": "cedula" },
            { "data": "nombres" },
            { "data": "correo" },
            { "data": "placa" },
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
                "defaultContent": '<a type="button" class="btn btn-primary btn-editar-clientes" ><i class="fas fa-edit"></i></a> <a type="button" class="btn btn-danger btn-eliminar-clientes"><i class="fas fa-trash"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });

    $('#table_clientes tbody').on('click', '.btn-eliminar-clientes', function () {

        var data = table.row($(this).parents('tr')).data();

        const response = confirm('¿Estas seguro de eliminar el cliente: ' + data.nombres + '?');

        if (response) {

            $.ajax({

                url: '/principal/del_clientes',
                type: 'POST',
                data: { cedula: data.cedula }

            }).done(function () {

                $('#table_clientes').DataTable().ajax.reload();

            }).fail(function (e) {
                alert("Error: " + e.responseJSON.message);
            });

        }

    });

    $('#table_clientes tbody').on('click', '.btn-editar-clientes', function () {
        var data = table.row($(this).parents('tr')).data();

        $('#clienteModal').modal("show");

        let form = document.getElementById("form_cliente");

        document.getElementById("clienteModalLabel").innerHTML = "<b>Editar Cliente</b>"

        document.getElementById("save-cliente").style = "display:none"
        document.getElementById("edit-cliente").style = "display:visible"

        document.getElementById("cli_ciudadano").value = data.nombres
        document.getElementById("cli_clave").value = data.clave
        document.getElementById("cli_rep_clave").value = data.clave
        document.getElementById("cli_correo").value = data.correo
        document.getElementById("cli_placa").value = data.placa
        document.getElementById("cli_buscar").value = data.cedula

        document.getElementById("cli_cedula").value = data.cedula

        form.setAttribute("action", "/principal/edit_cliente")

    });

});


$("#cli_buscar").on("input", function (e) {

    cedula = $(this).val()

    let mensaje = document.getElementById("cli_mensaje_buscador");

    if (cedula != "" && cedula.length == 10) {
        
        mensaje.innerHTML = '<i class="fa fa-spinner fa-spin" style="color:gray"></i>'

        $.ajax({

            url: '/padron/buscar',
            type: 'POST',
            data: { s_buscar: cedula }

        }).done(function (response){
            
            response = JSON.parse(response)

            document.getElementById("cli_cedula").value = response.cedula
            document.getElementById("cli_ciudadano").value = response.nombre

            mensaje.innerText = "Encontrado";
            mensaje.style = "color:green;";


        }).fail(function (e){

            mensaje.innerText = "No se encuentra el Cliente";
            mensaje.style = "color:red;";

        });

    }else{

        document.getElementById("cli_cedula").value = ""
        document.getElementById("cli_ciudadano").value = ""

        mensaje.innerText = "";

    }

})


$('#clienteModal').on('show.bs.modal', function (event) {

    let form = document.getElementById("form_cliente");
    let mensaje = document.getElementById("mensaje_cliente");

    mensaje.innerText = ""

    document.getElementById("clienteModalLabel").innerHTML = "<b>Agregar cliente</b>"

    document.getElementById("save-cliente").style = "display:visible"
    document.getElementById("edit-cliente").style = "display:none"

    form.reset();

    form.setAttribute("action", "/principal/save_clientes")

});



$('#form_cliente').submit(function (e) {

    e.preventDefault();

    var form = $('#form_cliente')[0];

    let mensaje = document.getElementById("mensaje_cliente");

    mensaje.innerHTML = '<i class="fa fa-spinner fa-spin" style="color:gray"></i>'

    $.ajax({

        url: form.getAttribute("action"),
        type: 'POST',
        data: new FormData(form),
        processData: false,
        contentType: false,
        cache: false

    }).done(function (e) {

        mensaje.innerText = e.message;
        mensaje.style = "color:green;";

        if(e.message != "Cliente Actualizado Correctamente"){

            form.reset();
            $('#clienteModal').modal("hide");

        }
        
        $('#table_clientes').DataTable().ajax.reload();

    }).fail(function (e) {

        mensaje.innerText = e.responseJSON.message;
        mensaje.style = "color:red;";

    });


});



$('.btn_ver_clave').click(function (e) {

    e.preventDefault();

    let $this = $(this);

    var padre = $this.prev('input');
    var hijo = $this[0].getElementsByTagName("i")[0];

    switch (padre.attr("type")) {

        case "text":

            padre.attr("type", "password");
            hijo.classList.add("fa-eye-slash");
            hijo.classList.remove("fa-eye")
            break

        case "password":
            padre.attr("type", "text");
            hijo.classList.add("fa-eye");
            hijo.classList.remove("fa-eye-slash")
            break;
    }

});