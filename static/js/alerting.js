function success_alert(text){
    swal({
        title: "Success!",
        text: text,
        icon: "success",
        timer: 1500,
        buttons: false,
    });
}

function error_alert(text){
    swal({
        title: "Error!",
        text: text,
        icon: "error",
        timer: 1500,
        buttons: false,
    });
}