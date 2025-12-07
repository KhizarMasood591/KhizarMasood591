$(document).ready(
    function(){
        $(".rate-name-field select").change(
            function(){
                var selectedValue = $(this).val();
                if (selectedValue == "Discounted"){
                    $(".discount-pct").show();
                }
                else{
                    $(".discount-pct").hide();
                };
            }
        )
    }
);
$(document).ready(
function(){
        $(".discount-pct").hide()
    }
);
$(document).ready(
    function(){
        $(".room-night-field input").change(
            function(){
                var inputValue = $(this).val();
                console.log(inputValue);
                if (inputValue <= 0){
                    $(".generate-letter").prop("disabled",true);
                }
                else{
                    $(".generate-letter").prop("disabled",false);
                }
            }
        );
    }
);
$(document).ready(
    function(){
        $('.property-names').change(
            function (){
                const roomNights = $(".nights").val();
                const dateString_checkIn =  $(".arrival-date").val();
                if (dateString_checkIn != "" && roomNights != ""){
                    const checkIn = new Date(dateString_checkIn);
                    const dateString_arrv = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkIn);
                    const checkOut = checkIn;
                    checkOut.setDate(checkOut.getDate() + Number(roomNights));
                    const dateString_dep = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkOut);
                    const property = $('.property-names').val();
                    $.get(
                    "https://khizar591.pythonanywhere.com/get_rates?hotel="+property+"&checkin="+dateString_arrv+"&checkout="+dateString_dep,
                    function (response){
                        $('.rate-field').empty();
                        console.log(response);
                        for (var i= 0; i < response["rates"].length;i++){
                            $('.rate-field').append('<option>'+ response["rates"][i] + '</option>');
                        };
                    }
                    );
                }

            }
        )
    }
);
$(document).ready(
    function(){
        $('.arrival-date').change(
            function (){
                const roomNights = $(".nights").val();
                const dateString_checkIn =  $(".arrival-date").val();
                if (dateString_checkIn != "" && roomNights != ""){
                    const checkIn = new Date(dateString_checkIn);
                    const dateString_arrv = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkIn);
                    const checkOut = checkIn;
                    checkOut.setDate(checkOut.getDate() + Number(roomNights));
                    const dateString_dep = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkOut);
                    const property = $('.property-names').val();
                    $.get(
                    "https://khizar591.pythonanywhere.com/get_rates?hotel="+property+"&checkin="+dateString_arrv+"&checkout="+dateString_dep,
                    function (response){
                        $('.rate-field').empty();
                        console.log(response);
                        for (var i= 0; i < response["rates"].length;i++){
                            $('.rate-field').append('<option>'+ response["rates"][i] + '</option>');
                        };
                    }
                    );
                    const depDate = document.querySelector(".check-out-field input");
                    depDate.placeholder = checkOut.toLocaleDateString('en-US');
                }

            }
        )
    }
);
$(document).ready(
    function(){
        $('.nights').change(
            function (){
                const roomNights = $(".nights").val();
                const dateString_checkIn =  $(".arrival-date").val();
                if (dateString_checkIn != "" && roomNights != ""){
                    const checkIn = new Date(dateString_checkIn);
                    const dateString_arrv = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkIn);
                    const checkOut = checkIn;
                    checkOut.setDate(checkOut.getDate() + Number(roomNights));
                    const dateString_dep = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkOut);
                    const property = $('.property-names').val();
                    const adults = $('.adult-count input').val();
                    $.get(
                    "https://khizar591.pythonanywhere.com/get_rates?hotel="+property+"&checkin="+dateString_arrv+"&checkout="+dateString_dep+"&adults="+adults,
                    function (response){
                        $('.rate-field').empty();
                        console.log(response);
                        for (var i= 0; i < response["rates"].length;i++){
                            $('.rate-field').append('<option>'+ response["rates"][i] + '</option>');
                        };
                    }
                    );
                    const depDate = document.querySelector(".check-out-field input");
                    depDate.placeholder = checkOut.toLocaleDateString('en-US');
                }

            }
        )
    }
);
$(document).ready(
    function(){
        $('.property-names').change(
            function(){
                if($('.property-names').val() != 'TBH'){
                    $(".adult-count").hide();
                }
                else{
                    $(".adult-count").show();
                };
            }
            )
    }
    );
$(document).ready(
    function(){
        $(".adult-count").hide();
    }
    );
$(document).ready(
    function(){
        $('.adult-count input').change(
            function (){
                const roomNights = $(".nights").val();
                const dateString_checkIn =  $(".arrival-date").val();
                if (dateString_checkIn != "" && roomNights != ""){
                    const checkIn = new Date(dateString_checkIn);
                    const dateString_arrv = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkIn);
                    const checkOut = checkIn;
                    checkOut.setDate(checkOut.getDate() + Number(roomNights));
                    const dateString_dep = new Intl.DateTimeFormat('en-US',{dateStyle:'short'}).format(checkOut);
                    const property = $('.property-names').val();
                    const adults = $('.adult-count input').val();
                    $.get(
                    "https://khizar591.pythonanywhere.com/get_rates?hotel="+property+"&checkin="+dateString_arrv+"&checkout="+dateString_dep+"&adults="+adults,
                    function (response){
                        $('.rate-field').empty();
                        console.log(response);
                        for (var i= 0; i < response["rates"].length;i++){
                            $('.rate-field').append('<option>'+ response["rates"][i] + '</option>');
                        };
                    }
                    );
                }

            }
        )
    }
);