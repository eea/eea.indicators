jQuery(document).ready(function($){
    var resizeButton = "<a class='standardButton googlechart-inline-resize'>Resize chart</div>";

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
