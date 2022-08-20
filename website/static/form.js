$("#user_type").change(function () {
    if ($(this).val() == "listener") {
        $('#listenerDiv').show();
    } else {
        $('#listenerDiv').hide();
    }

});
$("#user_type").trigger("change");

$("#user_type").change(function () {
    if ($(this).val() == "listener") {
        $('#listenerDiv').show();
    } else {
        $('#listenerDiv').hide();
    }

});
$("#user_type").trigger("change");


$("#is_premium").change(function () {
    if ($(this).val() == "no") {
        $('#noPremiumDiv').show();
    } else {
        $('#noPremiumDiv').hide();
    }
    if ($(this).val() == "yes") {
        $('#PremiumDiv').show();
    } else {
        $('#PremiumDiv').hide();
    }
});
$("#is_premium").trigger("change");