// revise form selector
var form = $('#revise-form');

var fh = new FormHelper('revise-form');

// Bind create dept even
form.on('submit', function(event){
    event.preventDefault();
    fh.clean();
    submitReviseForm();
});

$(document).on('click', '.delete', function(){
    var item = $(this).attr('data-item');
    if (confirm('Удалить оборудование из ревизии?')) {
        $('tr#equipment-' + item).remove();
    }
});

function loadReviseCsvData(data) {
    var reviseDiv = $('#revise-data-list'); // Empty div loads with django template

    $(document.createElement('h3')).addClass('text-success').text('Данные загруженные из файла ревизии:').appendTo(reviseDiv);

    var reviseForm = $(document.createElement('form')).attr({'method': 'post', 'action': '/equipments/revise/update/'});
    var reviseTable = $(document.createElement('table')).addClass('table table-hover table-striped');

    reviseTable.html("<thead><tr>" +
        "<th>Модель</th>" +
        "<th>Инвентарный номер</th>" +
        "<th>Серийный номер</th>" +
        "<th>Дата ревизии</th>" +
        "<th>Удалить:</th>" +
        "</tr></thead>");

    $.each(data, function (key, item){
        var row = $(document.createElement('tr')).attr({'id': 'equipment-' + key});

        // model tab
        $(document.createElement('td')).html('<b>' + item.model + '</b>').appendTo(row);

        var invNum = item.inventory_number == 'None' ? 'Не имеет' : item.inventory_number;

        // inventory number tab
        $(document.createElement('td')).addClass('text-primary').text(invNum).appendTo(row);

        var serialNum = item.serial_number == 'None' ? 'Не имеет' : item.serial_number;

        // serial number tab
        $(document.createElement('td')).text(serialNum).appendTo(row);

        // revised date tab
        $(document.createElement('td')).text(item.revised_at).appendTo(row);

        // delete equipment tab
        $(document.createElement('td'))
            .html('<a href="#" class="delete" data-item="' + key + '"><i class="fa fa-trash fa-fw"></i></a>')
            .appendTo(row);

        // hidden equipment field
        $(document.createElement('input'))
            .attr({
                'type': 'hidden',
                'name': 'data',
                'value': [item.inventory_number, item.serial_number, item.revised_at].join(';')
            })
            .appendTo(row);

        row.appendTo(reviseTable);
    });

    reviseTable.appendTo(reviseForm);

    $('input[name="csrfmiddlewaretoken"]').appendTo(reviseForm);

    $(document.createElement('input'))
        .attr({'type': 'submit', 'value': 'Применить ревизию'})
        .addClass('btn btn-lg btn-warning')
        .appendTo(reviseForm);

    $(document.createElement('a'))
        .attr({'href': '/equipments/revise'})
        .text('Сброс данных')
        .addClass('btn btn-lg btn-default')
        .appendTo(reviseForm);

    reviseForm.appendTo(reviseDiv);
}

function submitReviseForm() {
    var formData = new FormData();
    formData.append('file', $('#id_file')[0].files[0]);

    $.ajax({
        url : "",
        type : "POST",
        data : formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType

        // handle a successful response
        success : function(json) {
            form.slideUp(200); // Hide revise form on success
            loadReviseCsvData(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            var errors = $.parseJSON(xhr.responseText);
            fh.errorMessage('Ошибка отправки данных формы!');
            fh.showErrors(errors.errors);
            console.log(errors);
        }
    });
}
