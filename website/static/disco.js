$("#put_in").change(function () {
    if ($(this).val() == "yes") {
        $('#PutInAlbum').show();
    } else {
        $('#PutInAlbum').hide();
    }

});
$("#put_in").trigger("change");

$("#put_in").change(function () {
    if ($(this).val() == "no") {
        $('#add_song_').show();
    } else {
        $('#add_song_').hide();
    }

});
$("#put_in").trigger("change");