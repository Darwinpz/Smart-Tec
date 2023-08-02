var data_pisos
var data_sensor

$(document).ready(function () {
    var table = $('#table_sensores').DataTable({
        "ajax": {
            "url": "/principal/ver_sensores",
            "method": "post"
        },
        "columns": [
            {"data":"_id"},
            { "data": "piso.nombre" },
            { "data": "seccion" },
            { "data": "plaza" },
            { "data": "nombre" },
            { "data": "estado" },
            { "data": null }
        ],
        "createdRow": function (row, data, index) {
            if(data.estado == "OCUPADO"){
                $(row).addClass("text-danger fw-bold")
            }
            if(data.estado == "DISPONIBLE"){
                $(row).addClass("text-success fw-bold")
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
                "defaultContent": '<a type="button" class="btn btn-primary btn-editar-sensores" ><i class="fas fa-edit"></i></a> <a type="button" class="btn btn-danger btn-eliminar-sensores"><i class="fas fa-trash"></i></a>',
            }
        ],
        "pagingType": "full_numbers", //con esto salen los botones de primero anterior siguiente ultimo y los numeros de pagina
        "pageLength": 30, //para que se filtren por 30
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json" //Para que salga en español
        },
        "lengthMenu": [30, 35, 40, 45, 50]
    });


    $('#table_sensores tbody').on('click', '.btn-eliminar-sensores', function () {
        
        var data = table.row($(this).parents('tr')).data();

        const response = confirm('¿Estas seguro de eliminar el sensor: ' + data.nombre + '?');

        if (response) {

            $.ajax({

                url: '/principal/del_sensores',
                type: 'POST',
                data: { id:data._id, nombre: data.nombre}

            }).done(function () {

                $('#table_sensores').DataTable().ajax.reload();                

            }).fail(function (e) {
                alert("Error: "+ e.responseJSON.message);
            });

        }

    });

    $('#table_sensores tbody').on('click', '.btn-editar-sensores', function () {
        var data = table.row($(this).parents('tr')).data();
       
        $('#sensorModal').modal("show");

        let form = document.getElementById("form_sensor");
    
        document.getElementById("sensorModalLabel").innerHTML = "<b>Editar sensor</b>"

        document.getElementById("save-sensor").style = "display:none"
        document.getElementById("edit-sensor").style = "display:visible"

        document.getElementById("s_nombre").value = data.nombre  

        document.getElementById("s_codigo").value = data._id
    
        data_sensor = data

        form.setAttribute("action","/principal/edit_sensor")
        
    });

    setInterval( function () {
        table.ajax.reload();    
    }, 1000 );

});



$('#sensorModal').on('show.bs.modal', function (event) {

    let form = document.getElementById("form_sensor");
    let mensaje = document.getElementById("mensaje_sensor");

    mensaje.innerText = ""

    document.getElementById("sensorModalLabel").innerHTML = "<b>Agregar sensor</b>"

    document.getElementById("save-sensor").style = "display:visible"
    document.getElementById("edit-sensor").style = "display:none"
    
    form.reset();

    var output = '<option disabled selected value="">Selecciona</option>';
    $("#s_cmb_piso").html(output);
    $("#s_cmb_seccion").html(output);
    $("#s_cmb_plaza").html(output);

    $.ajax({

        url: '/principal/ver_pisos',
        type: 'POST',

        success: function (response) {

            var output = '<option disabled selected value="">Selecciona</option>';

            response = JSON.parse(response)

            response.data.forEach(piso => {

                output += '<option value=' + piso._id + '>' + piso.nombre + '</option>';

            });


            data_pisos = response.data

            $("#s_cmb_piso").html(output);

            if (data_sensor) {
                
                $("#s_cmb_piso").val(data_sensor.piso._id).change()
                
            }

            output = "";

        }

    });

    data_sensor = null

    form.setAttribute("action","/principal/save_sensores")

});


$("#s_cmb_piso").on("change", function (e) {

    var id_piso = document.getElementById("s_cmb_piso").value
    
    let piso = data_pisos.find(o => o._id === id_piso);

    var output = '<option disabled selected value="">Selecciona</option>';

    piso.items.forEach(seccion => {

        output += '<option value=' + seccion.seccion + '>' + seccion.seccion + '</option>';

    });

    $("#s_cmb_seccion").html(output);

    if (data_sensor) {
                
        $("#s_cmb_seccion").val(data_sensor.seccion).change()
    }


});


$("#s_cmb_seccion").on("change", function (e) {

    var id_piso = document.getElementById("s_cmb_piso").value
    var id_seccion = document.getElementById("s_cmb_seccion").value
    
    let piso = data_pisos.find(o => o._id === id_piso);

    let seccion = piso.items.find(o=> o.seccion === id_seccion)

    var output = '<option disabled selected value="">Selecciona</option>';

    sensores = $('#table_sensores').DataTable().rows().data().toArray();

    arr_plazas = []

    sensores.forEach(sensor => {
        
        if(sensor.piso._id == id_piso && sensor.seccion == id_seccion){
           arr_plazas.push(parseInt(sensor.plaza))
        }

    });

    for (let i = 1; i <= seccion.plaza; i++) {

        output += '<option value=' + i + '>' + i + '</option>';
    
    }

    $("#s_cmb_plaza").html(output);

    if (data_sensor) {
                
        $("#s_cmb_plaza").val( data_sensor.plaza).change()
    
    }else{

        const selectElement = document.getElementById("s_cmb_plaza");

        for (let i = selectElement.options.length - 1; i >= 0; i--) {
            if (arr_plazas.includes(i)) {
              selectElement.remove(i);
            }
        }

    }

});

$('#form_sensor').submit(function (e) {

    e.preventDefault();

    var form = $('#form_sensor')[0];

    let mensaje = document.getElementById("mensaje_sensor");

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
    
        if(e.message != "sensor Actualizado Correctamente"){

            form.reset();
            $('#sensorModal').modal("hide");

        }

        $('#table_sensores').DataTable().ajax.reload();

    }).fail(function(e){
        
        mensaje.innerText = e.responseJSON.message;
        mensaje.style="color:red;";

    });


});
