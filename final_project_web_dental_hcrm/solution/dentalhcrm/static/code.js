function isInt(value) {
    return !isNaN(value) &&
        parseInt(Number(value)) == value &&
        !isNaN(parseInt(value, 10));
}

var MIN_AGE = 0;
var MAX_AGE = 120;

function calc_patient_year_of_birth() {
    var year_of_birth = document.getElementById("patient_year_of_birth");
    var age = document.getElementById("patient_age");

    if (!isInt(age.value)) {
        alert("Invalid age");
        age.select();
        return 1;
    }

    if (age.value < MIN_AGE || age.value > MAX_AGE) {
        alert("Age out of boundaries");
        age.select();
        return 2;
    }

    var current_year = new Date().getFullYear();
    year_of_birth.value = current_year - age.value;
    return 0;
}

function calc_patient_age() {
    var age = document.getElementById("patient_age")
    var year_of_birth = document.getElementById("patient_year_of_birth");

    if (!isInt(year_of_birth.value)) {
        alert("Invalid year of birth");
        year_of_birth.select();
        return 1;
    }

    var current_year = new Date().getFullYear();

    if (year_of_birth.value < current_year - MAX_AGE || year_of_birth.value > current_year) {
        alert("Invalid year of birth");
        year_of_birth.select()
        return 2;
    }

    age.value = current_year - year_of_birth.value;
    return 0;
}

function ConfirmDelete() {
    var deleteButton = document.getElementById('delete_button');

    var choice = confirm(deleteButton.getAttribute('data-confirm'));

    if (choice) {
        window.location.href = deleteButton.getAttribute('href');
    }
    
}


