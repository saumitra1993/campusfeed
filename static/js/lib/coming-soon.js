 $('#counter').countdown('2015/12/15 12:00:00').on('update.countdown',function(event){var $this = $(this).html(event.strftime('' + '<div class="counter-container"><div class="counter-box first"><div class="number">%-D</div><span>Day%!d<span></div>' + '<div class="counter-box"><div class="number">%H</div><span>Hours</span></div>' + '<div class="counter-box"><div class="number">%M</div><span>Minutes</span></div>' + '<div class="counter-box last"><div class="number">%S</div><span>Seconds</span></div></div>'))});
            

$(document).ready(function () {
    $("#submitbutton").click(function()
    {
        var error = true;
        if(!(/(.+)@(.+){2,}\.(.+){2,}/.test($("#email").val())))
        {
            $("#email").addClass("not-valid");
            error = false ;
        } else { $("#email").removeClass("not-valid"); }
        
        if(error)
        {
            $.ajax
            ({
                type: "POST",
                url: "notifyme.php",
                data: $("form#notifyMe").serialize(),
                success: function(result) {
                    $("#email").val('');
                        $("#successmsg").show();
                        $("#successmsg").html(result); 
                }
            });
        }
    });

    });