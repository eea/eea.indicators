function figuresNumber() {
    var figures = jQuery(".figure-title");
    var count = 1;

    jQuery.each(figures, function(i, figure) {
        var figure_title = figure.innerHTML;
        figure.innerHTML = 'Fig. ' + count + ': ' + figure_title;
        count += 1;
    });
}

function clearToc(toc) {
    toc.find(".portletItem").empty();
}

function showMetadata(metadata) {
    var $document_toc = jQuery('#document-toc');
    var $metadata = jQuery(metadata),
        $metaddata_info_switchable = jQuery(".metadata-info-switchable");
    if ($metadata.hasClass('metadata-switch-show')) {
        $metaddata_info_switchable.find("h2").toggleClass('notoc');
        $metaddata_info_switchable.fadeIn("slow", function() {
            $metadata.removeClass('metadata-switch-show')
            .addClass('metadata-switch-hide')
            .html('Switch to short indicator view');
        });
        clearToc($document_toc);
        build_toc($document_toc);
    }
    else
        if ($metadata.hasClass('metadata-switch-hide')) {
            $metaddata_info_switchable.find("h2").toggleClass('notoc');
            $metaddata_info_switchable.fadeOut("slow", function() {
                $metadata.removeClass('metadata-switch-hide')
                .addClass('metadata-switch-show')
                .html('Switch to full indicator view');
            });
            clearToc($document_toc);
            build_toc($document_toc);
        }
}

function setMetadataSwitchBtn() {
    var $metadata_switch = jQuery(".metadata-switch");
    $metadata_switch.click(function () { showMetadata(this); });
}

jQuery(document).ready(function () {
    figuresNumber();
    setMetadataSwitchBtn();
});
