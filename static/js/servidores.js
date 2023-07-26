var data_serv

$(document).ready(function () {
    var table = $('#table_servidores').DataTable({
        "ajax": {
            "url": "/principal/ver_servidores",
            "method": "post",
            "data": { s_validar: "" },
        },
        "columns": [
            { "data": "_id" },
            { "data": "cedula" },
            {"data":"nombres"},
            { "data": "estado" },
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
                "defaultContent": '<a type="button" class="btn btn-primary btn-editar-servidores" ><i class="fas fa-edit"></i></a> <a type="button" class="btn btn-danger btn-eliminar-servidores"><i class="fas fa-trash"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });

    $('#table_servidores tbody').on('click', '.btn-eliminar-servidores', function () {

        var data = table.row($(this).parents('tr')).data();

        const response = confirm('¿Estas seguro de eliminar el servidor: ' + data.nombres + '?');

        if (response) {

            $.ajax({

                url: '/principal/del_servidores',
                type: 'POST',
                data: { cedula: data.cedula }

            }).done(function () {

                $('#table_servidores').DataTable().ajax.reload();

            }).fail(function (e) {
                alert("Error: " + e.responseJSON.message);
            });

        }

    });


    $('#table_servidores tbody').on('click', '.btn-editar-servidores', function () {
        var data = table.row($(this).parents('tr')).data();
        
        $('#servidorModal').modal("show");

        let form = document.getElementById("form_servidor");

        document.getElementById("servidorModalLabel").innerHTML = "<b>Editar Servidor</b>"

        document.getElementById("save-servidor").style = "display:none"
        document.getElementById("edit-servidor").style = "display:visible"

        document.getElementById("s_cedula").value = data.cedula
        document.getElementById("s_ciudadano").value = data.nombres
        document.getElementById("s_cmb_estado").value = data.estado
        document.getElementById("s_correo").value = data.correo

        if(data.url_foto != ""){

            document.getElementById("img_servidor").src = "/servidores/"+data.url_foto

            var btn_borrar = document.createElement("span")
            btn_borrar.className = "btn btn-danger d-flex justify-content-center mt-2"
            btn_borrar.innerText = "Eliminar Foto"
            btn_borrar.id = "btn-borrar-foto-servidor"
            document.getElementById("foto-servidor").appendChild(btn_borrar)
            
            $('#btn-borrar-foto-servidor').on('click', function () {

                const response = confirm('¿Estas seguro de eliminar la Imagen?');

                if (response) {

                    $.ajax({

                        url: '/del_foto',
                        type: 'POST',
                        data: { id: data._id, tipo:"servidores" }

                    }).done(function () {

                        document.getElementById("img_servidor").src = "/img/perfil.png"
                        document.getElementById("btn-borrar-foto-servidor").remove()
                        data_serv.url_foto = ""

                    }).fail(function (e) {
                        alert("Error: " + e.responseJSON.message);
                    });

                }

            })

        }else{
            document.getElementById("img_servidor").src = "/img/perfil.png"
            
            if(document.getElementById("btn-borrar-foto-servidor") != undefined){

                document.getElementById("btn-borrar-foto-servidor").remove()

            }

        }


        data_serv = data

        document.getElementById("s_div_buscar").style = "display:none";

        form.setAttribute("action", "/principal/edit_servidor")


    });

});


$('#servidorModal').on('show.bs.modal', function (event) {


    let form = document.getElementById("form_servidor");
    let mensaje = document.getElementById("mensaje_servidor");
    let mensaje_buscador = document.getElementById("mensaje_buscador");
    
    document.getElementById("img_servidor").src = "/img/perfil.png"

    document.getElementById("save-servidor").style = "display:visible"
    document.getElementById("edit-servidor").style = "display:none"

    document.getElementById("s_div_buscar").style = "display:visible";

    mensaje.innerText = ""
    mensaje_buscador.innerText = ""

    document.getElementById("servidorModalLabel").innerHTML = "<b>Agregar Servidor</b>"

    if(document.getElementById("btn-borrar-foto-servidor") != undefined){

        document.getElementById("btn-borrar-foto-servidor").remove()

    }

    form.reset();


    data_serv = null
        
    
    form.setAttribute("action", "/principal/save_servidores")

});

$("#s_buscar").on("input", function (e) {

    cedula = $(this).val()

    let mensaje = document.getElementById("mensaje_buscador");

    if (cedula != "" && cedula.length == 10) {
        
        mensaje.innerHTML = '<i class="fa fa-spinner fa-spin" style="color:gray"></i>'

        $.ajax({

            url: '/padron/buscar',
            type: 'POST',
            data: { s_buscar: cedula }

        }).done(function (response){
            
            response = JSON.parse(response)

            document.getElementById("s_cedula").value = response.cedula
            document.getElementById("s_ciudadano").value = response.nombre

            mensaje.innerText = "Encontrado";
            mensaje.style = "color:green;";


        }).fail(function (e){

            mensaje.innerText = "No se encuentra el ciudadano";
            mensaje.style = "color:red;";

        });

    }else{

        document.getElementById("s_cedula").value = ""
        document.getElementById("s_ciudadano").value = ""

        mensaje.innerText = "";

    }

})

$('#form_servidor').submit(function (e) {

    e.preventDefault();

    var form = $('#form_servidor')[0];

    let mensaje = document.getElementById("mensaje_servidor");

    let mensaje_buscador = document.getElementById("mensaje_buscador");

    mensaje.innerHTML = '<i class="fa fa-spinner fa-spin" style="color:gray"></i>'

    $.ajax({

        url: form.getAttribute("action"),
        type: 'POST',
        data: new FormData(form),
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,

    }).done(function (e) {

        mensaje.innerText = e.message;
        mensaje.style = "color:green;";

        if(e.message != "Servidor Actualizado Correctamente"){

            form.reset();
            document.getElementById("img_servidor").src = "/img/perfil.png"
            mensaje_buscador.innerText = "";
            $('#servidorModal').modal("hide");

        }

        $('#table_servidores').DataTable().ajax.reload();

    }).fail(function (e) {

        mensaje.innerText = e.responseJSON.message;
        mensaje.style = "color:red;";

    });

});
