$("#put_in").change(function () {
    if ($(this).val() == "yes") {
        $('#PutInAlbum').show();
    } else {
        $('#PutInAlbum').hide();
    }

});
$("#put_in").trigger("change");