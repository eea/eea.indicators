jQuery(document).ready(function ($) {
    $(".not-ready-anchor").each(function(){
        var url = $(this).parent().find('a:first-child').next('a').attr('href') + '/portlet_readiness_live';
        $(this).qtip({content: {
            'url':url,
            'text':'Loading, please wait...'
        }});
    });
});

