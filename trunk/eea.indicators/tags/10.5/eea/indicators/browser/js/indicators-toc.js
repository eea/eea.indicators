function figuresNumber() {
    var figures = jQuery(".figure-title");
    var count = 1;

    jQuery.each(figures, function(i, figure) {
        var figure_title = figure.innerHTML;
        figure.innerHTML = 'Fig. ' + count + ': ' + figure_title;
        count += 1;
    });
}

jQuery(document).ready(function () {
    figuresNumber();
});
