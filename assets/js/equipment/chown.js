// chown form selector
var chownControl = $('#chown-control');
var repairControlText = chownControl.text();

chownControl.on('click', function(event){
    event.preventDefault();
    var block = $('#chown-block');

    if (block.hasClass('hidden')) {
        chownControl.text('Свернуть форму');
        block.show('fast').removeClass('hidden');
    } else {
        chownControl.text(repairControlText);
        block.hide('fast').addClass('hidden');
    }
});
