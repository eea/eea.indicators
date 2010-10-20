function ajaxize(target, url) {
    $(target).load(url, function(){
        $(".report form", target).submit(
            function(){
                var btn = $('input[type=');
                var formurl = $(this).attr('action');
                var report = $(this).parents('.report').get(0);
                var data = $(this).serialize();

                $(target).load(formurl, data, function(){ 
                    ajaxize(target, url);
                });
            
                return false;
            }
        );
    });
}


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

        ajaxize($('.target', parent).get(0), url);
        return false;
    });

});

