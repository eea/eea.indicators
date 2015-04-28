jQuery(document).ready(function($){
    if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)){
        var ieversion=RegExp.$1;
        if (ieversion<9){
            return;
        }
    }
    var resizeButton = "<a class='standardButton googlechart-inline-resize'>Resize chart</a>";

    jQuery.each(jQuery(".embedded-daviz-visualization .standardButton"), function(){
        if ((jQuery(this).closest("dd").find("div.figure-chart-live").length > 0) &&
            (jQuery(this).closest("dd").find("div.isChart").length > 0)) {
            jQuery(this).after(resizeButton);
        }
    });

    jQuery("a.googlechart-inline-resize").click(function(){
        var chartToResize;
        jQuery.each(jQuery(this).closest(".embedded-daviz-visualization").find(".googlechart_dashboard"), function(idx, chart){
            if (jQuery(chart).is(":visible")){
                chartToResize = jQuery(chart);
            }
        });
        chartToResize.EEAChartResizer();
    });
});
