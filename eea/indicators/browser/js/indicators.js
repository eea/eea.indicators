function change_kupu_styles(){
    $(".kupu-table").remove();
    $('.kupu-image').remove();
    $(".kupu-tb-styles option[value='h2|']").remove();
    $(".kupu-tb-styles option[value='h3|']").remove();
}

$(document).ready(function () {
        // this should be integrated somehow into the kupu API
        setTimeout('change_kupu_styles()', '2000');
        set_actives();
        set_creators();
});

function set_actives(){
    $("#dialog-inner .cancel-btn").click(function(e){
            $("#dialog-inner").dialog("destroy");
            return false;
            });     // make the Cancel link from dialogs close the form

    // make the controls appear on the active fields, on hover
    $(".active_field").mouseover(function(e){
            $(this).addClass("active_field_hovered");   
            return false;
            });
    $(".active_field").mouseout(function(e){
            $(this).removeClass("active_field_hovered");    
            return false;
            });

    // activates the active fields
    $(".active_field").make_editable();
}

function set_creators(){
    $('a.object_creator').click(function(){
            var link = $(this).attr('href');
            var region = $(this).parents(".active_region")[0];
            console.log("Clicking ", link, region);
            $.ajax({
                url: link,
                type:'GET',
                // timeout: 2000,
                error: function() {
                    alert("Failed to update!");
                },
                success: function(r) { 
                    console.log("Reloading region", region);
                    reload_region($(region));
                    // $(region).replaceWith(r);
                    set_actives();
                    set_creators();
                    return false;
                }
                });
            return false;
            });
}

(function($) {
 $.fn.make_editable = function() {

 return this.each(function() {
     // console.log("Making editable ", this);
     var content = $('.content', this).get();

     var metadata = $('.metadata', this);
     var fieldname = $('.metadata > .fieldname', this).text();

     var width = Number($('.metadata > .width', this).text()) || 700;
     var height = Number($('.metadata > .height', this).text()) || null;

     var id_to_fill = 'active_field-' + fieldname
     $(content).attr('id', id_to_fill);

     $('.control a', this).click(function(e){
         var title = $(this).text();
         var link = $(this).attr('href');
         var options = {
            'width':width,
            'height':height
         }

         dialog_edit(link, title, function(text, status, xhr){

             // TODO: this is a _temporary_ hack to make kupu work properly
             // the problem is probably that not all the DOM is loaded when the kupu editor
             // is initiated and so it freezes the editor
             // A proper fix would be to see if it's possible to delay the kupu load when it is 
             // loaded through AJAX
             // This fix has two problems: it uses a global variable (window.kupu_id) - but 
             // this is easily fixable; it loads a frame (emptypage.html) that might not be completely
             // loaded in the timeout interval, and when that happens it throws an error

             $('.kupu-editor-iframe').parent().parent().parent().parent().each(function(){
                 //there should be one active kupu
                 window.kupu_id = $(this).attr('id');
                 setTimeout('initialize_kupu()', 500);
                 });

             ajaxify($("#dialog-inner"), fieldname);

             }, options);
         return false;
     });
 });
 };
})(jQuery);

function reload_region(el){
    var update_handler = $(".metadata .region_update_handler", el).text();
    // console.log(el, update_handler);

    $.ajax({
        url: update_handler,
        type:'GET',
        // timeout: 2000,
        error: function() {
            // console.log("Failed to update");
            alert("Failed to update!");
        },
        success: function(r) { 
            $(el).replaceWith(r);
            // console.log("active fields", $('.active_field'));
            // $(".active_field").make_editable();
            set_actives();

        return false;
        }
        });

return false;
}

function closer(fieldname){
    var text = $('#value_response').html();
    var fieldname = "#active_field-"+fieldname + " > *";
    var region = $(fieldname).parents('.active_region').get();
    reload_region(region);

    $(fieldname).html(text);
    $('#value_response').remove();
    $("#dialog-inner").dialog("destroy");

    return false;
}

function ajaxify(el, fieldname){
    // console.log("ajaxifying");

    $("form", el).submit(
            function(e){
            //if we find a kupu frame inside this form, we assume our field is a richtext field
            if ($('.kupu-editor-iframe', el).length > 0) {
                console.log("We have kupu");
                var textarea = $('textarea[name=' + fieldname + ']', el)[0];
                window.active_kupu.saveDataToField(textarea.form, textarea);
            }
            
            var data = ($(":input[name=" + fieldname + "]", this).serialize() + 
                "&form_submit=Save&form.submitted=1&specific_field=" + fieldname
                );
            // console.log("submiting to (action, data)", this.action, data);

            $.ajax({
                "data": data,
                url: this.action,
                type:'POST',
                // timeout: 2000,
                error: function() {
                    // console.log("Failed to submit");
                    alert("Failed to submit");
                },
                success: function(r) { 
                    $(el).html(r);
                    ajaxify(el);
                    return false;
                }
            });
            return false;
            });
};

function dialog_edit(url, title, callback, options){
    options = options || {
        'height':null,
        'width':700,
    }
    var target = $('#dialog_edit_target');
    $("#dialog-inner").remove();     // temporary, apply real fix
    $(target).append("<div id='dialog-inner'></div>");
    $("#dialog-inner").dialog({
        modal:true, 
        width:options.width, 
        minWidth:options.width, 
        height:options.height,
        minHeight:options.height,
        'title':title,
        closeOnEscape:true
        });
    $("#dialog-inner").load(url, callback);
    change_kupu_styles();
};

window.kupu_id = null;
window.active_kupu = null;

function initialize_kupu(){
    window.active_kupu = initPloneKupu(window.kupu_id);
}
