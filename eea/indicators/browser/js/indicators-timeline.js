$(document).ready(function () {
    $(".not-ready-anchor").each(function(){
        var url = $(this).parent().find('a:last-child').attr('href') + '/portlet_readiness_live';
        $(this).qtip({content: {
            'url':url,
            'text':'Loading...'
        }});
    });
});

