function change_kupu_styles(){
    $(".kupu-table").remove();
    $('.kupu-image').remove();
    $(".kupu-tb-styles option[value='h2|']").remove();
    $(".kupu-tb-styles option[value='h3|']").remove();
}

$(document).ready(function () {
    on_load_dom();
    $(window).ajaxStart(function(){
            $('body').append("<div class='specification-loading'></div>");
            var dim = get_dimmensions();
            var scr = get_scrollXY();
            $('.specification-loading').css({
                'top':dim.height/2-50 + scr.y + 'px',
                'left':dim.width/2-50 + scr.x + 'px'
                });
            return false;
        });
    $(window).ajaxComplete(function(){
            $('.specification-loading').remove();
            return false;
        }
    );
});

function on_load_dom(){
    setTimeout('change_kupu_styles()', '2000');
    set_actives();
    set_creators();
    set_deleters();
    set_editors();
    set_sortables();
    // activates the active fields
    $(".active_field").make_editable();
}

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
}

function set_sortables() {
    $('.sortable_spec').sortable({
            'handle':'.handler',
            'items':'.list-item',
            placeholder: 'ui-state-highlight'
            });	
}

function set_editors(){
    $('a.schemata_edit').click(function(){
            var link = $(this).attr('href');
            var title = $(this).text();
            var region = $(this).parents(".active_region")[0];
            var options = {
            'width':800,
            'height':600
            }
            var active_region = region.id; //the region that will be reloaded

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

                schemata_ajaxify($("#dialog-inner"), active_region);

                }, options);
            return false;
            });
}

function set_creators(){
    $('a.object_creator').click(function(){
            var link = $(this).attr('href');
            var region = $(this).parents(".active_region")[0];
            $.ajax({
                url: link,
                type:'GET',
                // timeout: 2000,
                error: function() {
                    alert("Failed to update!");
                },
                success: function(r) { 
                    reload_region($(region));
                    return false;
                }
                });
            return false;
            });
}

function set_deleters(){
    $('a.object_delete').click(function(){
            var link = $(this).attr('href');
            var region = $(this).parents(".active_region")[0];
            $.ajax({
                url: link,
                type:'GET',
                // timeout: 2000,
                error: function() {
                    alert("Failed to update!");
                },
                success: function(r) { 
                    reload_region($(region));
                    return false;
                }
                });
            return false;
            });
}

(function($) {
 $.fn.make_editable = function() {

 return this.each(function() {
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
         var region_id = null;

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

    $.ajax({
        url: update_handler,
        type:'GET',
        // timeout: 2000,
        error: function() {
            alert("Failed to update!");
        },
        success: function(r) { 
            var id = $(el).attr('id');
            $(el).replaceWith(r);
            on_load_dom();
            var new_el = $("#"+id);
            $(new_el).effect('highlight');
            // $(new_el).animate({backgroundColor:'#e1e1e1'}, 1000)
            //         .animate({backgroundColor:'transparent'}, 1500);
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
    $("form", el).submit(
            function(e){
            //if we find a kupu frame inside this form, we assume our field is a richtext field
            if ($('.kupu-editor-iframe', el).length > 0) {
                var textarea = $('textarea[name=' + fieldname + ']', el)[0];
                window.active_kupu.saveDataToField(textarea.form, textarea);
            }

            var data = ($(":input[name=" + fieldname + "]", this).serialize() + 
                "&form_submit=Save&form.submitted=1&specific_field=" + fieldname
                );

            $.ajax({
                "data": data,
                url: this.action,
                type:'POST',
                // timeout: 2000,
                error: function() {
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

function schemata_ajaxify(el, active_region){

    set_actives();

    $("form", el).submit(
            function(e){
            var form = this;

            var inputs = [];
            $(".widgets-list .widget-name").each(function(){
                inputs.push($(this).text());
                });

// problem: we can't read the content of kupu fields because we can't get a reference to them
// solution to problem: when we initialize a kupu editor with KupuEditor(iframe), it shouldn't reload
// the frame, so we can then get a reference to the kupu editor

            var data = "";
            $(inputs).each(function(i, v){
                var sep = ""
                var field = $(":input[name=" + v + "]", form);
                (i == 0) ? sep = "" : sep = "&";
                data += sep + field.serialize();
                });
            data += "&_active_region=" + active_region;
            data += "&form_submit=Save&form.submitted=1";

            $.ajax({
                "data": data,
                url: this.action,
                type:'POST',
                // timeout: 2000,
                error: function() {
                    alert("Failed to submit");
                },
                success: function(r) { 
                    $(el).html(r);
                    schemata_ajaxify(el, active_region);
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

function close_dialog(region){
    reload_region($("#"+region));
    $("#dialog-inner").dialog("destroy");
}

function get_dimmensions() {
  var myWidth = 0, myHeight = 0;
  if( typeof( window.innerWidth ) == 'number' ) {
    //Non-IE
    myWidth = window.innerWidth;
    myHeight = window.innerHeight;
  } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
    //IE 6+ in 'standards compliant mode'
    myWidth = document.documentElement.clientWidth;
    myHeight = document.documentElement.clientHeight;
  } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
    //IE 4 compatible
    myWidth = document.body.clientWidth;
    myHeight = document.body.clientHeight;
  }
  return {'width':myWidth, 'height':myHeight}
}
function get_scrollXY() {
  var scrOfX = 0, scrOfY = 0;
  if( typeof( window.pageYOffset ) == 'number' ) {
    //Netscape compliant
    scrOfY = window.pageYOffset;
    scrOfX = window.pageXOffset;
  } else if( document.body && ( document.body.scrollLeft || document.body.scrollTop ) ) {
    //DOM compliant
    scrOfY = document.body.scrollTop;
    scrOfX = document.body.scrollLeft;
  } else if( document.documentElement && ( document.documentElement.scrollLeft || document.documentElement.scrollTop ) ) {
    //IE6 standards compliant mode
    scrOfY = document.documentElement.scrollTop;
    scrOfX = document.documentElement.scrollLeft;
  }
  return {x: scrOfX, y:scrOfY };
}
