


$(document).ready(function () {
    let global_max_row = parseInt($("#peak_num").attr('value'));
    console.log(global_max_row)

    let top_item_height = $("#top-item").outerHeight();
    $("#blank").css("height", top_item_height);
    $("#top-item").addClass("fixed-top");

    $("body").on('blur', ".peak-td", function () {
        let id = $(this).attr('id');
        $("#input-"+id).attr('value', $(this).text());
        let add_row = true;
        for(let i = 1; i < global_max_row; i++){
            if($("#a"+i).text() == '' || $("#b"+i).text() == '' || $("#c"+i).text() == ''){
                add_row = false;
                break
            }
        }
        if(add_row){
            let num = parseInt(id.substring(1))+1;
            $("#tr"+num).css('display', '');
            global_max_row++;
            $("#peak_num").attr('value', global_max_row);
        }
    });

    $(".navbar").click(function () {
        window.location.href = 'https://www.ly0505.top/'
    })


});