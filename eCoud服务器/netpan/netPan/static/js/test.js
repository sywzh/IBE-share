$(document).ready(function(){
            getWord();
        });
function getWord(){
    $('#submitbtn').click(function(){
        var a = $('#testName').val();
        var b = $('#testWord').val();
        $.ajax({
            type:"post",
            url:"",
            data:{
                a:a,
                b:b
            },
            dataType:'json',
            contentType:"application/x-www-form-urlencoded;charset=UTF-8",
            success:function(data){
                alert(data.message);
            },
            
        });
    });
}
