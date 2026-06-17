function getDepartmentValidationOptions() {
    return {
        rules: {
            name: {
                required: true,
                minlength: 3
            },
            code: {
                required: true,
                minlength: 2,
                maxlength: 10
            },
            description: {
                required: true,
                minlength: 5
            }
        },
        messages: {
            name: {
                required: "Department name is required",
                minlength: "Minimum 3 characters required"
            },
            code: {
                required: "Department code is required",
                minlength: "Minimum 2 characters required",
                maxlength: "Maximum 10 characters allowed"
            },
            description: {
                required: "Description is required",
                minlength: "Minimum 5 characters required"
            }
        },
        errorClass: "text-danger",
        validClass: "is-valid",
        highlight: function(element) {
            $(element).addClass("is-invalid");
        },
        unhighlight: function(element) {
            $(element).removeClass("is-invalid");
        },
        errorPlacement: function(error, element) {
            element.closest(".mb-3, .form-group")
                   .find("div.text-danger")
                   .empty()
                   .append(error);
        }
    };
}

function initDepartmentFormValidation(selector) {
    var form = $(selector);

    if (form.length && !form.data("validator")) {
        form.validate(getDepartmentValidationOptions());
    }
}

$(document).ready(function() {
    initDepartmentFormValidation("#departmentForm");
    initDepartmentFormValidation("#editDepartmentForm");
});
