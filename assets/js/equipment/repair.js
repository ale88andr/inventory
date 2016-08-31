// revise form selector
var repairControl = $('#repair-control');
var repairControlText = repairControl.text();

repairControl.on('click', function(event){
    event.preventDefault();
    var block = $('#repair-block');

    if (block.hasClass('hidden')) {
        repairControl.text('Свернуть форму');
        block.show('fast').removeClass('hidden');
    } else {
        repairControl.text(repairControlText);
        block.hide('fast').addClass('hidden');
    }
});
