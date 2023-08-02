
$(document).ready(function () {
    var table = $('#table_pisos').DataTable({
        "ajax": {
            "url": "/principal/ver_pisos",
            "method": "post"
        },
        "columns": [
            {"data":"_id"},
            { "data": "nombre" },
            { "data": "count_seccion" },
            { "data": "count_plaza" },
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
                "defaultContent": '<a type="button" class="btn btn-primary btn-editar-pisos" ><i class="fas fa-edit"></i></a> <a type="button" class="btn btn-danger btn-eliminar-pisos"><i class="fas fa-trash"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });


    $('#table_pisos tbody').on('click', '.btn-eliminar-pisos', function () {
        
        var data = table.row($(this).parents('tr')).data();

        const response = confirm('¿Estas seguro de eliminar el piso: ' + data.nombre + '?');

        if (response) {

            $.ajax({

                url: '/principal/del_pisos',
                type: 'POST',
                data: { id:data._id, nombre: data.nombre}

            }).done(function () {

                $('#table_pisos').DataTable().ajax.reload();                

            }).fail(function (e) {
                alert("Error: "+ e.responseJSON.message);
            });

        }

    });

    $('#table_pisos tbody').on('click', '.btn-editar-pisos', function () {
        var data = table.row($(this).parents('tr')).data();
       
        $('#pisoModal').modal("show");

        let form = document.getElementById("form_piso");
    
        document.getElementById("pisoModalLabel").innerHTML = "<b>Editar piso</b>"

        document.getElementById("save-piso").style = "display:none"
        document.getElementById("edit-piso").style = "display:visible"

        document.getElementById("p_nombre").value = data.nombre  

        document.getElementById("p_codigo").value = data._id

        clearopcciones();

        for (var i = 0; i < data.items.length; i++) {

            crear_opciones(i, data.items[i])

        }

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

    form.setAttribute("action","/principal/save_pisos")

    clearopcciones();
    
    form.reset();

});


$('#form_piso').submit(function (e) {

    e.preventDefault();

    var form = $('#form_piso')[0];

    let mensaje = document.getElementById("mensaje_piso");

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
        mensaje.style="color:green;";
    
        if(e.message != "Piso Actualizado Correctamente"){

            form.reset();
            $('#pisoModal').modal("hide");

        }

        $('#table_pisos').DataTable().ajax.reload();

    }).fail(function(e){
        
        mensaje.innerText = e.responseJSON.message;
        mensaje.style="color:red;";

    });


});


function addopciones() {

    var count = document.getElementById("items").childElementCount

    count = count - 1;

    if (count <= 4) {

        crear_opciones(count, null)

    }

}

function clearopcciones() {

    document.querySelectorAll(".items").forEach(e => e.remove())

}

function crear_opciones(count, objeto) {

    var btn_eliminar = document.createElement("span")
    btn_eliminar.className = "btn btn-danger d-flex justify-content-center"
    btn_eliminar.innerHTML = "<i class='fas fa-trash'></i>"
    btn_eliminar.style = "border-radius:50%; position:absolute; height:25px; width:3px"
    btn_eliminar.setAttribute("onclick", "delopciones(" + count + ")");

    var row = document.createElement("div");
    row.className = "row mb-2 items"
    row.id = "piso_" + count

    var col_seccion = document.createElement("div");
    col_seccion.className = "col-lg-6 col-md-12 col-sm-12 mb-1 mt-1";

    var col_plaza = document.createElement("div");
    col_plaza.className = "col-lg-6 col-md-12 col-sm-12 mb-1 mt-1";

    var input_seccion = document.createElement("input");
    input_seccion.type = "text"
    input_seccion.maxLength = 1
    input_seccion.placeholder = "Sección"
    input_seccion.className = "form-control"
    input_seccion.name = "seccion[]"
    input_seccion.required = true;
    input_seccion.value = (objeto != null) ? objeto.seccion : ""

    var input_plaza = document.createElement("input");
    input_plaza.type = "number"
    input_plaza.placeholder = "Plaza"
    input_plaza.className = "form-control"
    input_plaza.name = "plaza[]"
    input_plaza.required = true;
    input_plaza.value = (objeto != null) ? objeto.plaza : ""

    col_seccion.appendChild(input_seccion)
    col_plaza.appendChild(input_plaza)

    row.appendChild(btn_eliminar)
    row.appendChild(col_seccion)
    row.appendChild(col_plaza)

    document.getElementById("items").appendChild(row)

}


function delopciones(id) {

    document.getElementById("piso_" + id).remove();

}