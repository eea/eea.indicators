function block_ui(){
(function($) {
  var scr_x = jQuery(window).scrollLeft();
  var scr_y = jQuery(window).scrollTop();
  var dim_x = jQuery(window).width();
  var dim_y = jQuery(window).height();

  var overlay = jQuery('<div>');
  overlay.addClass('specification-overlay');

  var loading = jQuery('<div>');
  loading.addClass('specification-loading');

  loading.css({
    'top':dim_y/2-50 + scr_y + 'px',
    'left':dim_x/2-50 + scr_x + 'px',
    'z-index':2001
  });
  overlay.css({
    'top':scr_y+'px',
    'left':scr_x+'px',
    'z-index':2000,
    'width':dim_x+'px',
    'height':dim_y+'px',
    // 'background-color':'white',
    position:'absolute'
  });

  jQuery('body').append(overlay);
  jQuery('body').append(loading);
  overlay.show();
  loading.show();
})(jQuery);
}

function unblock_ui(){
  jQuery('.specification-overlay').remove();
  jQuery('.specification-loading').remove();
}

function set_sortables() {
  // make certain DOM elements sortable with jquery UI sortable

(function($) {
  $('.sortable_spec').each(function(){
    var handler = $(".metadata .handler", this).text();
    $(this).sortable({
      'handle':'.handler',
      'items':'.list-item',
      placeholder: 'ui-state-highlight',
      // containment: 'parent'    // has a bug in UI, sometimes it's impossible to move #2 to #1
      'update':function(event, ui){
        var sortable = event.target;
        var neworder = $(sortable).sortable('toArray');
        var data = "";
        $(neworder).each(function(){
          data += "&order:list=" + this;
        });
        block_ui();
        $.ajax({
          'url':handler,
          'type':'POST',
          'cache':false,
          'data':data,
          'success':function(){
            unblock_ui();
          }
        });
      }
    });
    $('.sortable_spec').disableSelection();

  });
})(jQuery);
}

function init_tinymce(el){
  // init tinymce edit fields
  var config = {
      'theme_advanced_buttons1': "save,style,bold,italic,justifyleft,justifycenter," +
                                 "justifyright,justifyfull,bullist,numlist,definitionlist," +
                                 "outdent,indent,link,unlink,anchor,code,fullscreen",
      'theme_advanced_buttons2':"",
      'theme_advanced_buttons3':"",
      'theme_advanced_buttons4':"",
      "theme_advanced_styles":[

    { title: "Invisible grid", tag: "table", className: "invisible", type: "Tables" },
    { title: "Fancy listing", tag: "table", className: "listing", type: "Tables" },
    { title: "Fancy grid listing", tag: "table", className: "grid listing", type: "Tables" },
    { title: "Fancy vertical listing", tag: "table", className: "vertical listing", type: "Tables" },
    { title: "Literal", tag: "pre", className: "", type: "Text" },
    { title: "Discreet", tag: "span", className: "discreet", type: "Selection" },
    { title: "Pull-quote", tag: "blockquote", className: "pullquote", type: "Text" },
    { title: "Call-out", tag: "p", className: "callout", type: "Text" },
    { title: "Highlight", tag: "span", className: "visualHighlight", type: "Selection" },
    { title: "Disc", tag: "ul", className: "listTypeDisc", type: "Lists" },
    { title: "Square", tag: "ul", className: "listTypeSquare", type: "Lists" },
    { title: "Circle", tag: "ul", className: "listTypeCircle", type: "Lists" },
    { title: "Numbers", tag: "ol", className: "listTypeDecimal", type: "Lists" },
    { title: "Lower Alpha", tag: "ol", className: "listTypeLowerAlpha", type: "Lists" },                                                                                               
    { title: "Upper Alpha", tag: "ol", className: "listTypeUpperAlpha", type: "Lists" },
    { title: "Lower Roman", tag: "ol", className: "listTypeLowerRoman", type: "Lists" },
    { title: "Upper Roman", tag: "ol", className: "listTypeUpperRoman", type: "Lists" },
    { title: "Definition term", tag: "dt", className: "", type: "Lists" },
    { title: "Definition description", tag: "dd", className: "", type: "Lists" },
    { title: "Odd row", tag: "tr", className: "odd", type: "Tables" },
    { title: "Even row", tag: "tr", className: "even", type: "Tables" },
    { title: "Heading cell", tag: "th", className: "", type: "Tables" },
    { title: "Page break (print only)", tag: "div", className: "pageBreak", type: "Print" },
    { title: "Clear floats", tag: "div", className: "visualClear", type: "Text" },
    { title: "(remove style)", tag: "", className: "", type: "Selection" }
        ],

  };
  window.initTinyMCE(document, config);
  return ;      //plone43
}


function ajaxify(el, fieldname){
  // This will make a form submit and resubmit itself using AJAX

(function($) {
  init_tinymce(el);

  $("form", el).submit(
    function(e){
      block_ui();
      /* tinyMCE.triggerSave(); */
      var form = this;
      var data = ($(form).serialize() + "&form_submit=Save&form.submitted=1");

      $.ajax({
        "data": data,
        url: this.action,
        type:'POST',
        cache:false,
        // timeout: 2000,
        error: function() {
          unblock_ui();
          alert("Failed to submit");
        },
        success: function(r) {
          $(el).html(r);
          ajaxify(el);
          unblock_ui();
          return false;
        }
      });
      return false;
    });
})(jQuery);
}

function set_relation_widgets() {
  // activates the relation widgets

(function($) {
  $(".indicators_relations_widget").each(function(){
    var fieldname = $(".metadata .fieldName", this).text();
    var realfieldname = $(".metadata .realFieldName", this).text();
    var widget_dom_id = $(".metadata .widget_dom_id", this).text();
    if (!widget_dom_id) {
      return false;
    }

    var popup = new EEAReferenceBrowser.Widget(fieldname);
    try {
      $('#' + widget_dom_id).get(0)._widget = popup;
      $(popup.events).bind(popup.events.SAVED, function(evt){
        ajaxify($('#'+widget_dom_id), realfieldname);
        $('#' + widget_dom_id + ' form').trigger('submit');
      });
    } catch (e) {
      // for some reasons this behaves as if the DOM is not fully loaded.
      // Probably the calling script should be made smarter
    }

  });
})(jQuery);
}

function bootstrap_select_widgets() {
(function($) {
  $(".dummy-org-selector").each(function(i,v){
    var widget = new MultiSelectAutocompleteWidget($(v));
  });
})(jQuery);
}

function set_generic_ajax_forms(){
(function($) {
  $(".generic_ajax_forms form").submit(function(e){
    var form = this;
    var data = $(":input", form).serialize();
    var url = $(this).attr('action');

    block_ui();

    $.ajax({
      'url':url,
      type:'POST',
      'data':data,
      cache:false,
      error:function(){
        unblock_ui();
        alert("ERROR: There was a problem communicating with the server. Please reload this page.");
      },
      success:function(r){
        unblock_ui();
        $(form).html(r);
      }
    });
    return false;
  });
})(jQuery);
}

function bootstrap_relations_widgets(){
  // bootstraps reference widgets for the assessment aggedit
(function($) {
  $('.eea-widget-referencebrowser').each(
    function(){
      // If it has a metadata then it's a widget from assessmentpart.
      // At this moment it's the only one that has that.

      if (!$(".metadata", this).length) { return false; }

      var widget = this;
      var active_field = $(widget).parents('.active_field').get(0);

      var fieldname = $(".metadata .fieldname", this).text();
      var domid = $(".metadata .domid", this).text();    //$(this).attr('id');
      var popup = new EEAReferenceBrowser.Widget(domid, {'fieldname':fieldname});
      $('#' + domid).get(0)._widget = popup;
      var region = $(this).parents('.active_region'); // TODO: is this needed? doesn't look like

      try {
        $(popup.events).bind(popup.events.SAVED, function(evt){
          ajaxify(active_field, domid);
          $(widget).parents('form').trigger('submit');
        });
      } catch (e) {
        // for some reasons this behaves as if the DOM is not fully loaded.
        // Probably the calling script should be made smarter
      }
    }
  );
})(jQuery);
}

function on_load_dom() {
  // executed whenever the regions are reloaded
  set_sortables();
  set_relation_widgets();
  bootstrap_relations_widgets();
  bootstrap_select_widgets();
  set_readiness_accordion();  // for portlet_readiness
  set_generic_ajax_forms();

}

function reload_region(el){
(function($) {
  block_ui();
  var update_handler = $(".metadata .region_update_handler", el).text();
  var also_reload = $(".metadata .also_reload", el);
  if (also_reload) {
    $(also_reload).children().each(function(){
      var region = $(this).text();
      if (region) {
        reload_region($("#"+region));
      }
    });
  }

  $.ajax({
    url: update_handler,
    type:'GET',
    cache:false,
    // timeout: 2000,
    error: function() {
      unblock_ui();
      alert("ERROR: There was a problem communicating with the server. Please reload this page.");
    },
    success: function(r) {
      var id = $(el).attr('id');
      $(el).replaceWith(r);
      var new_el = $("#"+id);
      $(new_el).effect('highlight');
      on_load_dom();
      unblock_ui();
      return false;
    }
  });

  return false;
})(jQuery);
}

function set_actives(){
  // adds effects for active fields; this should be executed whenever the DOM is reloaded

  // make the Cancel link from dialogs close the form
(function($) {
  $("#dialog-inner .cancel-btn").live('click', function(e){
    $("#dialog-inner").dialog("close");
    return false;
  });

  // make the controls appear on the active fields, on hover
  $(".active_field").live('mouseover', function(e){
    $(this).addClass("active_field_hovered");
    return false;
  });
  $(".active_field").live('mouseout', function(e){
    $(this).removeClass("active_field_hovered");
    return false;
  });


})(jQuery);
}

function schemata_ajaxify(el, active_region){

(function($) {
  set_actives();
  init_tinymce(el);

  //set the tags widget
  var widgets = $('.ArchetypesKeywordWidget');
  if(widgets.length){
    widgets.eeatags();
  }

  $("form", el).submit(
    function(e){
      block_ui();
      /* tinyMCE.triggerSave(); */
      var form = this;

      var inputs = [];
      $(".widgets-list .widget-name").each(function(){
        inputs.push($(this).text());
      });

      var data = "";
      data = $(form).serialize();
      data += "&_active_region=" + active_region;
      data += "&form_submit=Save&form.submitted=1";

      $.ajax({
        "data": data,
        url: this.action,
        type:'POST',
        cache:false,
        // timeout: 2000,
        error: function() {
          unblock_ui();
          alert("Failed to submit");
        },
        success: function(r) {
          $(el).html(r);
          schemata_ajaxify(el, active_region);
          unblock_ui();
          return false;
        }
      });
      return false;
    });
})(jQuery);
}

function set_inout(el){
(function($) {
  if (!el.length) { return false; }
  var divs = $("div div", el);
  var last_div = divs.get(divs.length-1);
  $("<div style='float:left; padding-top:18px'><input type='button' value='&uarr;' class='context up-btn'/><br/><input value='&darr;' type='button' class='context down-btn'/></div>").insertBefore($(last_div));
  var select = $("select", divs.get(1)).get(0);

  var up_btn = $(".up-btn", el);
  var down_btn = $(".down-btn", el);
  $(up_btn).click(function(){
    var ix = select.selectedIndex;
    if (ix === 0) {
      return false;
    }

    var opt = $(select).children().get(ix);
    var arr = [];
    for (i=0; i<select.options.length; i++) {
      arr.push(select.options[i]);
    }

    // move position above to the selected position
    arr[ix] = select.options[ix-1];
    arr[ix-1] = opt;

    var len = select.options.length;
    select.options.length = 0;

    for (i=0; i<len; i++) {
      select.options[i] = arr[i];
    }
  });

  $(down_btn).click(function(){
    var ix = select.selectedIndex;
    if (ix === select.options.length-1) {
      return false;
    }

    var opt = $(select).children().get(ix);
    var arr = [];
    for (i=0; i<select.options.length; i++) {
      arr.push(select.options[i]);
    }

    // move position below the selected position
    arr[ix] = select.options[ix+1];
    arr[ix+1] = opt;

    var len = select.options.length;
    select.options.length = 0;

    for (i=0; i<len; i++) {
      select.options[i] = arr[i];
    }
  });
})(jQuery);
}

function dialog_edit(url, title, callback, options){
  // Opens a modal dialog with the given title

(function($) {
  block_ui();
  var height = $(window).height() - 40;
  var width = $(window).width() - 40;
  options = $.extend({
    'height':height,
    'width':width
  }, options);
  var target = $('#dialog_edit_target');
  $("#dialog-inner").remove();     // temporary, apply real fix
  $(target).append("<div id='dialog-inner'></div>");
  window.onbeforeunload = null; // this disables the form unloaders
  $("#dialog-inner").dialog({
    modal:true,
    width:options.width,
    minWidth:options.width,
    height:options.height,
    minHeight:options.height,
    'title':title,
    closeOnEscape:true,
    buttons: {
      'Save':function(e){
        var button = e.target;
        $("#dialog-inner form").trigger('submit');
      },
      'Cancel':function(e){
        $("#dialog-inner").dialog("close");
      }
    },
    beforeclose:function(event, ui){
      return true;
    }
  });

  $.ajax({
    'url':url,
    'type':'GET',
    'cache':false,
    'success': function(r){
      $("#dialog-inner").html(r);

      // this is a workaround for the following bug:
      // after editing with Kupu in one of the popup dialogs,
      // it is not possible to click inside the text inputs anymore
      // surprisingly, clicking on their label activates the fields
      // this happens only in Internet Explorer
      //
      $("#dialog-inner div.ArchetypesRichWidget > label").each(function(){ 
          var label = this; 
          if ($(label).parents('.ArchetypesRichWidget').length) { 
            $(label).trigger('click'); 
          } 
      }); 
      set_inout($("#archetypes-fieldname-themes"));
      callback();
    }
  });
})(jQuery);
}

function set_editors(){
  // Set handlers for Edit (full schemata) buttons

(function($) {
  $('a.schemata_edit').live('click', function(){
    block_ui();
    var link = $(this).attr('href');
    var title = $(this).attr('title');
    var region = $(this).parents(".active_region")[0];

    // rewrite this to take advantage of metadata
    var options = {};
    //var options = {
      //'width':800,
      //'height':600
    //};
    var active_region = region.id; //the region that will be reloaded

    dialog_edit(link, title, function(text, status, xhr){
      schemata_ajaxify($("#dialog-inner"), active_region);
      unblock_ui();
    }, options);

  return false;
});
})(jQuery);
}

function set_edit_buttons() {
  // activate single active fields

(function($) {
  $('.active_field .control a').disableSelection();
  $('.active_field .control a').live('click', function(){

    // check if the control belongs in a disabled region
    var is_disabled = $(this).parents('.active_region').hasClass('disabled');
    if (is_disabled) {return false;}

    // check if this handler is not disabled through metadata
    var meta_disable = $(this).parents('.active_field').children('.metadata .disable_handler').length;

    if (meta_disable){
      return true;
    }

    block_ui();
    var link = $(this).attr('href');
    var region = $(this).parents(".active_region")[0];
    var field = $(this).parents('.active_field')[0];

    var active_region = region.id; //the region that will be reloaded

    var content = $('.content', field).get();
    var metadata = $('.metadata', field);
    var fieldname = $('.metadata > .fieldname', field).text();
    var title = $('.metadata > .dialog_title', field).text();

    var options = {}; //'width':800, 'height':600 };
    options.height = Number($('.metadata > .height', field).text()) || options.height;
    options.width = Number($('.metadata > .width', field).text()) || options.width;

    var id_to_fill = 'active_field-' + fieldname;
    $(content).attr('id', id_to_fill);
    dialog_edit(link, title, function(text, status, xhr){
      // schemata_ajaxify($("#dialog-inner"), fieldname);
      ajaxify($("#dialog-inner"), fieldname);
      bootstrap_select_widgets();
      unblock_ui();
    }, options);
    return false;
  });
})(jQuery);
}

function set_creators(){
  // Set handlers for Create buttons

(function($) {
  $('a.object_creator').live('click', function(){
    block_ui();
    var link = $(this).attr('href');
    var is_direct_edit = $(this).hasClass('direct_edit');
    var region = $(this).parents(".active_region")[0];
    var title = "Edit";
    var options = {};

    $.ajax({
      url: link,
      type:'GET',
      cache:false,
      // timeout: 2000,
      error: function() {
        unblock_ui();
        alert("ERROR: There was a problem communicating with the server. Please reload this page.");
      },
      success: function(r) {

        // In case there's an error, show it in a dialog and abort
        var error = $(r).children('.error');
        if (error) {
          $(error).dialog({
            buttons: {
              "Ok": function() {
                $(this).dialog("close");
                unblock_ui();
                return false;
              }
            }
          });
        }

        is_direct_edit = $(r).children('direct_edit').length || is_direct_edit;
        var info = $(r).children('.object_edit_url');
        if (info) {
          var edit_link = info.text();
          if (is_direct_edit) {
            document.location = edit_link;
            // unblock_ui();
            return false;
          } else {
            reload_region($(region));
            dialog_edit(edit_link, title, function(text, status, xhr){
              schemata_ajaxify($("#dialog-inner"), $(region).attr('id'));
              unblock_ui();
            },
            options
          );
          }
        } else {
          reload_region($(region));
          unblock_ui();
        }
        return false;
      }
    });

    return false;
  });
})(jQuery);
}

function set_disablers(){
  // first, we look if there are any active_regions that are "disabler"
  if (jQuery('.active_region .disabler').length) {

    // next, we disable all active_regions that are not a disabler
    jQuery('.active_region').each(function(){
        var node = this;
        jQuery(node).removeClass('disabled');
        if (!jQuery('.metadata > .disabler', node).length) {
          jQuery(node).addClass('disabled');
        }
    });
  }
}

function set_deleters(){
  // Set handlers for Delete buttons

(function($) {
  $('a.object_delete').live('click', function(){
    block_ui();
    var link = $(this).attr('href');
    var region = $(this).parents(".active_region")[0];

    $.ajax({
      url: link,
      type:'GET',
      cache:false,
      // timeout: 2000,
      error: function() {
        unblock_ui();
        alert("ERROR: There was a problem communicating with the server. Please reload this page.");
      },
      success: function(r) {
        reload_region($(region));
        return false;
      }
    });
    return false;
  });
})(jQuery);
}


function closer(fieldname, active_region, url){
  // reloads a region and closes the dialog based on an active field name

(function($) {
  var field = "#active_field-"+fieldname;
  var region = null;
  if (active_region) {
    region = $("#" + active_region).get();
  } else {
    region = $(field).parents('.active_region').get();
  }

  // we check if the field wants to reload the entire page
  var parent = $(field).parent();
  var reload_page = $('.reload_page', parent);
  if (reload_page.length) {
    $("#dialog-inner").dialog("close");
    document.location = url;
    return false;
  }

  reload_region(region);

  $("#dialog-inner").dialog("close");
  return false;
})(jQuery);
}

function close_dialog(info) {                                                                                                                                        
    var popups = [];
    jq(".indicators_relations_widget").each(function(){ 
        var fieldname = $(".metadata .fieldName", this).text();
        var realfieldname = $(".metadata .realFieldName", this).text();
        var widget_dom_id = $(".metadata .widget_dom_id", this).text();
        if (!widget_dom_id) {
          return false;
        }
        var popup = jq('#' + widget_dom_id).get(0)._widget; 
        popups.push(popup);
    });


   if (info.search('http://') !== -1) {                                                                                                                              
       jq("#dialog-inner").dialog("close");                                                                                                                          
       if (typeof(window.popup) !== "undefined") {
           jq(window.popup.events).trigger('EEA-REFERENCEBROWSER-BASKET-ADD', {url:info});                                                                               
       } else {
        if (!popups.length) {
            alert("could not get eea.reference popup");
        } else {
            jq(popups).each(function(){
                jq(this.events).trigger('EEA-REFERENCEBROWSER-BASKET-ADD', {url:info});
            });
        }
       }
   } else {                                                                                                                                                          
       // compatibility with eea.indicators                                                                                                                          
       reload_region($("#"+info));                                                                                                                                 
       jq("#dialog-inner").dialog("close");                                                                                                                          
   }                                                                                                                                                                 
}

function open_relations_widget(widget_dom_id, selected_tab){
(function($) {
  var widget = $("#"+widget_dom_id).get(0)._widget;
  window._selected_tab = selected_tab;// will be read by the relations widget and set as selected tab

  $("#" + widget_dom_id + " :input").trigger('click');
  return false;
})(jQuery);
return false;
}

function preselect_relations_tab(region_id, selected_tab){
(function($) {
  $("#" + region_id + " .searchButton").click(function(){
    window._selected_tab = selected_tab;// will be read by the relations widget and set as selected tab
    return true;
  });
})(jQuery);
}

jQuery(document).ready(function ($) {

  set_editors();
  set_actives();
  set_creators();
  set_deleters();
  set_edit_buttons();
  set_disablers();

  on_load_dom();

});

// this.contentWindow.focus();//this should solve the problem that requires pressing the bold button

function toggle_creator_option(el){
(function($) {
  var a = $(el).parent().parent().children('a.object_creator').get(0);
  var href = $(a).attr('href');
  if (!a.original_href) {
    a.original_href = href;
  }
  $(a).attr('href', a.original_href + "&create_in_latest_spec=" + $(el).attr('value'));
})(jQuery);
}
// vim: set sw=2 ts=2 softtabstop=2 et:
