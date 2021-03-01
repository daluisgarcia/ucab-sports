$(document).ready(function(){
    const stage_selector_id = 'select';
    const stage_participante_equipo_id = 'part';
    const stage_equipo_partido_id = 'part-match';
    const stage_num_grupos_id = 'num-groups';
    const stage_equipos_grupo_id = 'team-group';

    let selectorCont = 0;
    let input1Cont = 0;
    let input2Cont = 0;
    let input3Cont = 0;
    let input4Cont = 0;

    /*Add a new input to the form*/
    $("#addBtn").click(function(){
        let div = document.createElement('div');
        div.classList.add('row');

        let selector = $(`#${stage_selector_id}`).clone();
        let input1 = $(`#${stage_participante_equipo_id}`).clone();
        let input2 = $(`#${stage_equipo_partido_id}`).clone();
        let input3 = $(`#${stage_num_grupos_id}`).clone();
        let input4 = $(`#${stage_equipos_grupo_id}`).clone();

        let str = `stage-select-${(++selectorCont).toString()}NN`;
        selector.attr('name', str);
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

        str = `stage-part-${(++input1Cont).toString()}NN`;
        input1.attr('name', str);
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

        str = `stage-part-match-${(++input2Cont).toString()}NN`;
        input2.attr('name', str);
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

        str = `stage-num-groups-${(++input3Cont).toString()}NN`;
        input3.attr('name', str);
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

        str = `stage-team-group-${(++input4Cont).toString()}NN`;
        input4.attr('name', str);
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
        btn.addEventListener("click", function() {
            let numObject = $('#stageTournNum');
            let num = parseInt(numObject.text());
            if ( num > 1 ) {
                object = this.parentElement.parentElement.parentElement
                object.remove();
                numObject.text( num - 1 );
            }else {
                alert('No puedes borrar todas las fases');
            }
        });
        divIn = document.createElement('div');
        divIn.classList.add('col');
        divIn.append(btn)
        div.append(divIn);

        divIn = $('#stageTournNum'); //Rows counter
        let num = parseInt(divIn.text());
        divIn.text( num + 1 )

        let li = document.createElement('li');
        li.classList.add('list-group-item', 'col-12');
        li.id = 'NN'
        li.append(div);

        $('#form-list').append(li);
    });

    $(".deleteRow").click(function() {
        let numObject = $('#stageTournNum');
        let num = parseInt(numObject.text());
        if ( num > 1 ) {
            object = this.parentElement.parentElement.parentElement;
            $.get(object.id, function(data, status){
                if (status !== 'success') {
                    alert('Hay un problema tratando de eliminar la fase, recargue la pagina he intentelo de nuevo')
                } else {
                    object.remove();
                    numObject.text( num - 1 );
                }
            })
        }else {
            alert('No puedes borrar todas las fases');
        }
    });
});