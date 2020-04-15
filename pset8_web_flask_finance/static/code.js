function validatePassword(form) {
    // Shortcut variables
    password = form.password.value;
    confirmation = form.confirmation.value;

    // The password confirmation should match the password.
    if (password != confirmation) {
        alert ("\nPasswords do not match")
        return false;
    }
    else {
        return true;
    }
}

function increaseBy(increment) {
    // Shortcut variables
    quantity = document.querySelector("#quantity");
    value = Number(increment);

    // Value 0 means that the user has clicked "Reset"
    if (value === 0) {
        quantity.value = "";
    }
    else {
        if (quantity.value) {
            // Increase the existing value.
            quantity.value = Number(quantity.value) + value;
        }
        else {
            // Sets the value for the first time or after a reset.
            quantity.value = value;
        }
    }
}

function confirmTransaction(transaction) {
    // Shortcut variables.
    symbol = document.querySelector("#symbol").value;
    quantity = document.querySelector("#quantity").value;

    // Asks the user confirmation for the transaction
    if (transaction === 'buy' || transaction === 'sell')
    {
        message = "Are you sure you want to " + transaction + " " + quantity + " stocks of " + symbol + "?";
        return confirm(message);
    }
}