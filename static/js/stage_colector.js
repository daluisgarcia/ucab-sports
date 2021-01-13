$(document).ready(function(){
    const stage_selector_id = 'id_stagetournament_set-0-id_fase';
    const stage_input_id = 'id_stagetournament_set-0-jerarquia';
    const forms_num_id = 'id_stagetournament_set-TOTAL_FORMS';

    let selectorCont = 0;
    let inputCont = 0;

    /*Function to change the id number*/
    function changeIdNumber(idName, obj) {
        return idName.replace('0', (++obj.cont).toString());
    }

    /*Add a new input to the form*/
    $("#addBtn").click(function(){
        let div = document.createElement('div');

        let selector = $(`#${stage_selector_id}`).clone();
        let input = $(`#${stage_input_id}`).clone();

        let obj = {'cont': selectorCont};
        let str = changeIdNumber(stage_selector_id, obj);
        selectorCont = obj.cont;
        selector.attr('id', str);
        selector.attr('name', str.slice(3, str.length));
        selector.appendTo(div);

        obj = {'cont': inputCont};
        str = changeIdNumber(stage_input_id, obj);
        inputCont = obj.cont;
        input.attr("id", str);
        input.attr('name', str.slice(3, str.length));
        input.appendTo(div);

        form_num = $(`#${forms_num_id}`);
        form_num.val(parseInt(form_num.val()) + 1);

        $('#form-card').append(div);
    });

});