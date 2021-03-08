$(document).ready(function(){
    const person_cedula_id = 'id_form-0-cedula';
    const person_nombre_id = 'id_form-0-nombre';
    const person_apellido_id = 'id_form-0-apellido';
    const person_correo_id = 'id_form-0-correo';
    const person_username_id = 'id_form-0-nickname';
    const person_rol_id = 'id_form-0-rol';
    const forms_num_id = 'id_form-TOTAL_FORMS';

    let input_validation = document.getElementById(`${changeIdNumber(person_cedula_id, {'cont': 1})}`);

    let cedulaCont = input_validation ? 1 : 0;
    let nombreCont = input_validation ? 1 : 0;
    let apellidoCont = input_validation ? 1 : 0;
    let correoCont = input_validation ? 1 : 0;
    let usernameCont = input_validation ? 1 : 0;
    let rolCont = input_validation ? 1 : 0;

    /*Function to change the id number*/
    function changeIdNumber(idName, obj) {
        return idName.replace('0', (++obj.cont).toString());
    }

    function updateIds(numberDeleted) {
        let str = '';
        while (numberDeleted < usernameCont) {
            let cedulaAux = document.getElementById(`${changeIdNumber(person_cedula_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_cedula_id, {'cont': numberDeleted - 1});
            cedulaAux.id = str;
            cedulaAux.name = str.slice(3, str.length);
            let nombreAux = document.getElementById(`${changeIdNumber(person_nombre_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_nombre_id, {'cont': numberDeleted - 1});
            nombreAux.id = str;
            nombreAux.name = str.slice(3, str.length);
            let apellidoAux = document.getElementById(`${changeIdNumber(person_apellido_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_apellido_id, {'cont': numberDeleted - 1});
            apellidoAux.id = str;
            apellidoAux.name = str.slice(3, str.length);
            let correoAux = document.getElementById(`${changeIdNumber(person_correo_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_correo_id, {'cont': numberDeleted - 1});
            correoAux.id = str;
            correoAux.name = str.slice(3, str.length);
            let usernameAux = document.getElementById(`${changeIdNumber(person_username_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_username_id, {'cont': numberDeleted - 1});
            usernameAux.id = str;
            usernameAux.name = str.slice(3, str.length);
            let rolAux = document.getElementById(`${changeIdNumber(person_rol_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(person_rol_id, {'cont': numberDeleted - 1});
            rolAux.id = str;
            rolAux.name = str.slice(3, str.length);
            numberDeleted++;
        }
        cedulaCont--;
        nombreCont--;
        apellidoCont--;
        correoCont--;
        usernameCont--;
        rolCont--;
        form_num = $(`#${forms_num_id}`);
        form_num.val(parseInt(form_num.val()) - 1);
    }

    /*Add a new input to the form*/
    $("#addBtn").click(function(){
        let num_max_part = $('#num_max_part').val();

        if (parseInt(num_max_part) === cedulaCont+1){
            alert('No se pueden agregar mas participantes');
            return false;
        }


        let div = document.createElement('div');
        div.classList.add('row');

        let inputCedula = $(`#${person_cedula_id}`).clone();
        let inputNombre = $(`#${person_nombre_id}`).clone();
        let inputApellido = $(`#${person_apellido_id}`).clone();
        let inputCorreo = $(`#${person_correo_id}`).clone();
        let inputUsername = $(`#${person_username_id}`).clone();
        let inputRol = $(`#${person_rol_id}`).clone();

        let obj = {'cont': cedulaCont};
        let str = changeIdNumber(person_cedula_id, obj);
        cedulaCont = obj.cont;
        inputCedula.attr('id', str);
        inputCedula.attr('name', str.slice(3, str.length));
        let divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        let label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Cedula';
        divIn.append(label);
        let span = document.createElement('span');
        span.classList.add('stage_select');
        inputCedula.appendTo(span);
        divIn.append(span);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        obj = {'cont': nombreCont};
        str = changeIdNumber(person_nombre_id, obj);
        nombreCont = obj.cont;
        inputNombre.attr("id", str);
        inputNombre.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Nombre';
        divIn.append(label);
        inputNombre.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        obj = {'cont': apellidoCont};
        str = changeIdNumber(person_apellido_id, obj);
        apellidoCont = obj.cont;
        inputApellido.attr("id", str);
        inputApellido.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Apellido';
        divIn.append(label);
        inputApellido.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);
        
        obj = {'cont': correoCont};
        str = changeIdNumber(person_correo_id, obj);
        correoCont = obj.cont;
        inputCorreo.attr("id", str);
        inputCorreo.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Correo';
        divIn.append(label);
        inputCorreo.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);
        
        obj = {'cont': usernameCont};
        str = changeIdNumber(person_username_id, obj);
        usernameCont = obj.cont;
        inputUsername.attr("id", str);
        inputUsername.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Username';
        divIn.append(label);
        inputUsername.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        obj = {'cont': rolCont};
        str = changeIdNumber(person_rol_id, obj);
        rolCont = obj.cont;
        inputRol.attr("id", str);
        inputRol.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Rol';
        divIn.append(label);
        inputRol.appendTo(divIn);
        div.append(divIn);

        btn = document.createElement('button')
        btn.classList.add('btn', 'btn-danger', 'deleteRow')
        btn.type = 'button'
        btn.innerText = 'X'
        btn.id = rolCont;
        btn.addEventListener("click", function () {
            id = this.id
            updateIds(parseInt(id))
            object = this.parentElement.parentElement.parentElement
            object.remove()
        });
        divIn = document.createElement('div');
        divIn.classList.add('col');
        divIn.append(btn)
        div.append(divIn);

        form_num = $(`#${forms_num_id}`);
        form_num.val(parseInt(form_num.val()) + 1);

        let li = document.createElement('li');
        li.classList.add('list-group-item');
        li.append(div);

        $('#person_list').append(li);
    });

    // $("#form").submit(function (e) {
    //     let stagesAdded = [];
    //
    //     let stages = $(".stage_select").get();
    //     let promise = new Promise((resolve, reject) => {
    //         stages.forEach(function (stage){
    //             let num = stage.children[0].value;
    //             if (!stagesAdded.includes(num)) {
    //                 stagesAdded.push(num);
    //             } else {
    //                 reject();
    //             }
    //         });
    //         resolve();
    //     });
    //
    //     promise.then(value => {
    //         return true;
    //     }).catch(err => {
    //         e.preventDefault();
    //         alert('No se pueden agregar dos veces la misma fase al torneo');
    //     });
    // });

});