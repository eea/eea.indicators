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

    jQuery(".googlechart-inline-resize").click(function(){
        var chartToResize;
        var chart = jQuery(this).closest("dd").find(".googlechart_dashboard");
	if (jQuery(chart).is(":visible")){
		chartToResize = jQuery(chart);
	}
        if (chartToResize) {
            chartToResize.EEAChartResizer();
        }
    });
});
