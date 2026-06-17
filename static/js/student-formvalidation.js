function getStudentValidationOptions() {
    return {
        rules: {
            first_name: {
                required: true,
                minlength: 3
            },
            last_name: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            mobile: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
            dob: {
                required: true
            },
            gender: {
                required: true
            },
            address: {
                required: true
            },
            city: {
                required: true
            },
            department: {
                required: true
            },
            skills: {
                required: true
            }
        },
        messages: {
            first_name: {
                required: "First name is required",
                minlength: "First name minimum 3 characters"
            },
            last_name: {
                required: "Last name is required"
            },
            email: {
                required: "Email is required",
                email: "Enter a valid email address"
            },
            mobile: {
                required: "Mobile is required",
                digits: "Only digits allowed",
                minlength: "Mobile must be 10 digits",
                maxlength: "Mobile must be 10 digits"
            },
            dob: {
                required: "Date of birth is required"
            },
            gender: {
                required: "Gender is required"
            },
            address: {
                required: "Address is required"
            },
            city: {
                required: "City is required"
            },
            department: {
                required: "Department is required"
            },
            skills: {
                required: "Select at least one skill"
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

function initStudentFormValidation(selector) {
    var form = $(selector);

    if (form.length && !form.data("validator")) {
        form.validate(getStudentValidationOptions());
    }
}

$(document).ready(function() {
    initStudentFormValidation("#studentForm");
    initStudentFormValidation("#editStudentForm");
});
