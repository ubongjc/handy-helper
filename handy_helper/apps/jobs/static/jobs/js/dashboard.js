$(document).ready(function(){
    $('.add').on("click", function(){
        data = {'job_id': $(this).data("job")};
        $.post("user/jobs/add/", data, function(response){
            $('#placeholder').html(response);
        });
        return false;
    });

    $('#logout').on("click", function(){
        $('#logoutModal').modal('toggle');
        return false;
    });
    $('#logoutModal').on('shown.bs.modal', function(event){
        $('#yes').on('click', function(){
            $('#yes').attr("href", $('#logout').attr("href"));
        });
        $('#close, #no').on("click", function(){
            $('#logoutModal').modal('hide');
        });
    });

    $('.removeModal').appendTo("body") 
    $('.remove').on("click", function(){
        $('.removeModal').modal('toggle');
        return false;
    });
    $('.removeModal').on('shown.bs.modal', function(event){
        $('.remove_yes').on('click', function(){;
            data = {'job_id': $(this).data("id")};
            $.post("jobs/remove/", data, function(response){
                $('#placeholder').html(response);
                $('.removeModal').modal('hide');
            });
            return false;
        });
        $('.remove_close, .remove_no').on("click", function(){
            $('.removeModal').modal('hide');
            return false;
        });
    });

    $('.done').on("click", function(){
        data = {'job_id': $(this).data("job")};
        $.post("jobs/remove/", data, function(response){
            $('#placeholder').html(response);
        });
        return false;
    });

    $('.give_up').on("click", function(){
        data = {'job_id': $(this).data("job")};
        $.post("jobs/giveup/", data, function(response){
            $('#placeholder').html(response);
        });
        return false;
    });
});