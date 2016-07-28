function FormHelper(formId) {

    this.formId = formId || '';

    this.showMessage = function(text, type) {
        var message = text || '';
        var message_type = type || 'success';
        var html_code = "<div id='js-message' class='row'><div class='col-lg-4 text-center col-lg-offset-4'><br><div class='alert alert-dismissible alert-" + message_type + "'><button type='button' class='close' data-dismiss='alert'>×</button><strong>" + message + "</strong><br></div></div></div>";
        $(html_code).insertBefore(".row").hide().slideDown(200);
    };

    this.showErrors = function(hash) {
        $.each(hash, function(key, error) {
            var field = $(":input[name='" + key + "']");
            field.parent().addClass('has-error');
            $("#error-" + key).text(error.toString());
        })
    };

    this.errorMessage = function(message) {
        this.showMessage(message, 'danger');
    };

    this.successMessage = function(message) {
        this.showMessage(message);
    };

    this.clean = function() {
        $("#js-message").remove();

        var formForClean = $("form#" + this.formId + " :input");

        $.each(formForClean, function() {
            var field = $(this);

            if(field.parent().hasClass('has-error')) {
                field.parent().removeClass('has-error');
                field.next().text('');
            }
        })
    };
}
