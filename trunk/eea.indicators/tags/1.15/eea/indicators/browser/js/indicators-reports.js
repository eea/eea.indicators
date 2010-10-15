$(document).ready(function () {
    $(".fix_btn").click(function(){
        var parent = $(this).parent();

        if ($(this).attr('value') == '-') {
            $(this).attr('value', '+');
            $('.target', parent).remove();
            return false;
        }

        $(this).attr('value', '-');
        var url = $(this).parent().find('a').attr('href');
        $(parent).append("<div class='target' style='padding:0 1em 1em 1em; " + 
                         "margin:0 1em 1em 0; border:1px solid #666'>Loading...</div>");
        $('.target', parent).load(url);
        return false;
    });
});

