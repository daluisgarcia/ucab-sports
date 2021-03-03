$(document).ready(function(){
    const stage_selector_id = 'id_stagetournament_set-0-id_fase';
    const stage_participante_equipo_id = 'id_stagetournament_set-0-participantes_por_equipo';
    const stage_equipo_partido_id = 'id_stagetournament_set-0-equipos_por_partido';
    const stage_num_grupos_id = 'id_stagetournament_set-0-num_grupos';
    const stage_equipos_grupo_id = 'id_stagetournament_set-0-equipos_por_grupo';
    const forms_num_id = 'id_stagetournament_set-TOTAL_FORMS';

    let selectorCont = 0;
    let input1Cont = 0;
    let input2Cont = 0;
    let input3Cont = 0;
    let input4Cont = 0;

    /*Function to change the id number*/
    function changeIdNumber(idName, obj) {
        return idName.replace('0', (++obj.cont).toString());
    }

    function updateIds(numberDeleted) {
        let str = '';
        while (numberDeleted < input4Cont) {
            let selectorAux = document.getElementById(`${changeIdNumber(stage_selector_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(stage_selector_id, {'cont': numberDeleted - 1});
            selectorAux.id = str;
            selectorAux.name = str.slice(3, str.length);
            let input1Aux = document.getElementById(`${changeIdNumber(stage_participante_equipo_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(stage_participante_equipo_id, {'cont': numberDeleted - 1});
            input1Aux.id = str;
            input1Aux.name = str.slice(3, str.length);
            let input2Aux = document.getElementById(`${changeIdNumber(stage_equipo_partido_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(stage_equipo_partido_id, {'cont': numberDeleted - 1});
            input2Aux.id = str;
            input2Aux.name = str.slice(3, str.length);
            let input3Aux = document.getElementById(`${changeIdNumber(stage_num_grupos_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(stage_num_grupos_id, {'cont': numberDeleted - 1});
            input3Aux.id = str;
            input3Aux.name = str.slice(3, str.length);
            let input4Aux = document.getElementById(`${changeIdNumber(stage_equipos_grupo_id, {'cont': numberDeleted})}`);
            str = changeIdNumber(stage_equipos_grupo_id, {'cont': numberDeleted - 1});
            input4Aux.id = str;
            input4Aux.name = str.slice(3, str.length);
            numberDeleted++;
        }
        selectorCont--;
        input1Cont--;
        input2Cont--;
        input3Cont--;
        input4Cont--;
        form_num = $(`#${forms_num_id}`);
        form_num.val(parseInt(form_num.val()) - 1);
    }

    /*Add a new input to the form*/
    $("#addBtn").click(function(){
        let div = document.createElement('div');
        div.classList.add('row');

        let selector = $(`#${stage_selector_id}`).clone();
        let input1 = $(`#${stage_participante_equipo_id}`).clone();
        let input2 = $(`#${stage_equipo_partido_id}`).clone();
        let input3 = $(`#${stage_num_grupos_id}`).clone();
        let input4 = $(`#${stage_equipos_grupo_id}`).clone();

        let obj = {'cont': selectorCont};
        let str = changeIdNumber(stage_selector_id, obj);
        selectorCont = obj.cont;
        selector.attr('id', str);
        selector.attr('name', str.slice(3, str.length));
        let divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'mb-3');
        let label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Fase';
        divIn.append(label);
        let span = document.createElement('span');
        span.classList.add('stage_select');
        selector.appendTo(span);
        divIn.append(span);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        obj = {'cont': input1Cont};
        str = changeIdNumber(stage_participante_equipo_id, obj);
        input1Cont = obj.cont;
        input1.attr("id", str);
        input1.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'ml-lg-2', 'ml-xl-2', 'mr-lg-3', 'mr-xl-3', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Participantes por equipo';
        divIn.append(label);
        input1.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        obj = {'cont': input2Cont};
        str = changeIdNumber(stage_equipo_partido_id, obj);
        input2Cont = obj.cont;
        input2.attr("id", str);
        input2.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'ml-lg-3', 'ml-xl-3', 'mr-lg-3', 'mr-xl-3', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Equipos por partido';
        divIn.append(label);
        input2.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);
        
        obj = {'cont': input3Cont};
        str = changeIdNumber(stage_num_grupos_id, obj);
        input3Cont = obj.cont;
        input3.attr("id", str);
        input3.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'ml-lg-3', 'ml-xl-3', 'mr-lg-3', 'mr-xl-3', 'mb-3');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Número de grupos';
        divIn.append(label);
        input3.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);
        
        obj = {'cont': input4Cont};
        str = changeIdNumber(stage_equipos_grupo_id, obj);
        input4Cont = obj.cont;
        input4.attr("id", str);
        input4.attr('name', str.slice(3, str.length));
        divIn = document.createElement('div');
        divIn.classList.add('col', 'col-sm', 'col-md', 'col-lg-2', 'col-xl-2', 'text-left', 'ml-lg-3', 'ml-xl-3', 'mr-lg-2', 'mr-xl-2');
        label = document.createElement('h6');
        label.classList.add('d-md-none');
        label.innerText = 'Equipos por grupo';
        divIn.append(label);
        input4.appendTo(divIn);
        div.append(divIn);

        divIn = document.createElement('div');  // Separation block
        divIn.classList.add('w-100', 'd-block', 'd-sm-none');
        div.append(divIn);

        btn = document.createElement('button')
        btn.classList.add('btn', 'btn-danger', 'deleteRow')
        btn.type = 'button'
        btn.innerText = 'X'
        btn.id = input4Cont;
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

        $('#form-list').append(li);
    });

    $("#form").submit(function (e) {
        let stagesAdded = [];

        let stages = $(".stage_select").get();
        let promise = new Promise((resolve, reject) => {
            stages.forEach(function (stage){
                let num = stage.children[0].value;
                if (!stagesAdded.includes(num)) {
                    stagesAdded.push(num);
                } else {
                    reject();
                }
            });
            resolve();
        });

        promise.then(value => {
            return true;
        }).catch(err => {
            e.preventDefault();
            alert('No se pueden agregar dos veces la misma fase al torneo');
        });
    });

});