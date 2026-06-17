function getSkillValidationOptions() {
    return {
        rules: {
            name: {
                required: true,
                minlength: 2
            },
            description: {
                required: true,
                minlength: 10
            }
        },
        messages: {
            name: {
                required: "Skill name is required",
                minlength: "Minimum 2 characters required"
            },
            description: {
                required: "Description is required",
                minlength: "Minimum 10 characters required"
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

function initSkillFormValidation(selector) {
    var form = $(selector);

    if (form.length && !form.data("validator")) {
        form.validate(getSkillValidationOptions());
    }
}

$(document).ready(function() {
    initSkillFormValidation("#skillForm");
    initSkillFormValidation("#editSkillForm");
});
