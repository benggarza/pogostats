// JQuery listeners for the form.html template
// Requirements: JQuery, Awesomplete

console.log("Creating event listeners");

// API call to collect pokemon names
$(document).ready( function () {
    console.log("Sending an api request for pokemon_id!"); ////
    $.ajax({
        url: '/api/pokedex/pokemon_id',
        type: "GET",
        data: {'pokemon_id': 'None'},
        success: function(data) {
            console.log("Data!:"); ////
            console.log(data); ////
            // Awesomplete doesn't take jquery elements
            new Awesomplete(document.getElementById('pokemon_id'), {list: data['data']});
        },
        failure: function(data) {
            console.log("Request failed");
            console.log(data);
        }
    });

    // Create levels awesomplete values
    levels=[]
    for (let i = 1.0; i <= 50.0; i+=0.5){
        levels.push(i);
    }
    new Awesomplete(document.getElementById('level'), {list: levels});

    for (let i = 0; i <= 15; i++){
        $('#atk_iv').append($(document.createElement('option')).prop({
            value: i,
            text: i
        }));
        $('#def_iv').append($(document.createElement('option')).prop({
            value: i,
            text: i
        }));
        $('#sta_iv').append($(document.createElement('option')).prop({
            value: i,
            text: i
        }));
    }
} );

$('#pokemon_id').on('awesomplete-selectcomplete', function () {
    var pokemon_id = $('#pokemon_id').val();
    console.log('pokemon_id changed, value is now ', $('#pokemon_id').val()); ////

    if (pokemon_id !== undefined) {
        console.log("Sending an api request for fast_move_id!"); ////
        $.ajax({
            url: '/api/pokedex/fast_move_id',
            type: "GET",
            data: {'pokemon_id': pokemon_id},
            success: function(data) {
                console.log("Data!:"); ////
                console.log(data); ////
                for (let val of data['data']) {
                    $('#fast_move').append($(document.createElement('option')).prop({
                        value: val[1],
                        text: val[0].charAt(0) + val[0].slice(1).toLowerCase().replace('_', ' ')
                    }));
                }
            },
            failure: function(data) {
                console.log("Request failed");
                console.log(data);
            }
        });

        console.log("Sending an api request for first_charged_move_id!"); ////
        $.ajax({
            url: '/api/pokedex/first_charged_move_id',
            type: "GET",
            data: {'pokemon_id': pokemon_id},
            success: function(data) {
                console.log("Data!:"); ////
                console.log(data); ////
                for (let val of data['data']) {
                    $('#first_charged_move').append($(document.createElement('option')).prop({
                        value: val[1],
                        text: val[0].charAt(0) + val[0].slice(1).toLowerCase().replace('_', ' ')
                    }));
                    $('#second_charged_move').append($(document.createElement('option')).prop({
                        value: val[1],
                        text: val[0].charAt(0) + val[0].slice(1).toLowerCase().replace('_', ' ')
                    }));
                }
            },
            failure: function(data) {
                console.log("Request failed");
                console.log(data);
            }
        });
        var fieldIds = ['#level','#atk_iv', '#def_iv', '#sta_iv', '#fast_move', '#first_charged_move', '#second_charged_move'];
        for (var field of fieldIds){
            $(field).prop('disabled', false);
        }

        trySubmit();
    }
} );
$('#level').on('awesomplete-selectcomplete', trySubmit);
$('#atk_iv').on('change', trySubmit);
$('#def_iv').on('change', trySubmit);
$('#sta_iv').on('change', trySubmit);
$('#fast_move').on('change', trySubmit);
$('#first_charged_move').on('change', trySubmit);
$('#second_charged_move').on('change', trySubmit);


function trySubmit(){
    let fieldIds = ['#pokemon_id','#level','#atk_iv', '#def_iv', '#sta_iv', '#fast_move', '#first_charged_move', '#second_charged_move'];
    let submitReady = true;
    for (let field of fieldIds){
        console.log(field, $(field).val());
        if ($(field).val() == null || $(field).val() == ""){
            submitReady = false;
            $('#submit-btn').prop('disabled', false);
            break;
        }
    }
    if (submitReady){
        $('#submit-btn').prop('disabled', false);
    }
}