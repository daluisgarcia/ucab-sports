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
        selector.appendTo(divIn);
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

        form_num = $(`#${forms_num_id}`);
        form_num.val(parseInt(form_num.val()) + 1);

        let li = document.createElement('li');
        li.classList.add('list-group-item');
        li.append(div);

        $('#form-list').append(li);
    });



});