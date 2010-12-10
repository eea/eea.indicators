function change_kupu_styles(){
  // customize the Kupu editor to IMS standards
  $(".kupu-table").remove();
  $('.kupu-image').remove();
  $(".kupu-tb-styles option[value='h2|']").remove();
  $(".kupu-tb-styles option[value='h3|']").remove();
}

function get_kupu_editor(editorId) {
  // initializes a kupu editor and returns it.
  // This is needed to make up for the lack of proper API:
  // we can't get the kupu editor back from just the iframe or whatever
  // The content here is taken from initPloneKupu()

  var prefix = '#'+editorId+' ';

  var iframe = getFromSelector(prefix+'iframe.kupu-editor-iframe');
  var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
  // var form = textarea.form;

  // first we create a logger
  var l = new DummyLogger();

  // now some config values
  var conf = loadDictFromXML(document, prefix+'xml.kupuconfig');

  // the we create the document, hand it over the id of the iframe
  var doc = new KupuDocument(iframe);

  // now we can create the controller
  var kupu = (window.kupu = new KupuEditor(doc, conf, l));
  return kupu;
}


function save_kupu_values(el) {
  // saves each value from a kupu editor into its associated textarea

  $('.kupu-editor-iframe', el).parent().parent().parent().parent().each(function(){
    var id        = $(this).attr('id');
    var thiskupu  = get_kupu_editor(id);
    var fieldname = id.substr("kupu-editor-".length);
    var textarea  = $('#' + id + ' textarea[name=' + fieldname + ']')[0];
    var result    = thiskupu.getRichText(textarea.form, textarea);
    result = result.replace(/^\s+/g, "");  // for some reasons what kupu saves has a space in front

    if (result != textarea.defaultValue) {
      textarea.value = result;
    }
  });
}

function block_ui(){
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
}

function unblock_ui(){
  jQuery('.specification-overlay').remove();
  jQuery('.specification-loading').remove();
}

function set_sortables() {
  // make certain DOM elements sortable with jquery UI sortable

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
}

function ajaxify(el, fieldname){
  // This will make a form submit and resubmit itself using AJAX
  // It also takes care of kupu mangling

  $('.kupu-editor-iframe').parent().parent().parent().parent().each(function(){
    var kupu_id = $(this).attr('id');
    setTimeout(function(){
      initPloneKupu(kupu_id);
      $("#kupu-bold-button").trigger('click');
      $("#kupu-bold-button").trigger('click');
    }, 1000);
  });

  $("form", el).submit(
    function(e){
      block_ui();
      var form = this;
      save_kupu_values(form);
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
}

function set_relation_widgets() {
  // activates the relation widgets

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
}

function bootstrap_select_widgets() {
  $(".dummy-org-selector").each(function(i,v){
    var widget = new MultiSelectAutocompleteWidget($(v));
  });
}

function set_generic_ajax_forms(){
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
}

function bootstrap_relations_widgets(){
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
      var region = $(this).parents('.active_region');

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
}

function set_actives(){
  // adds effects for active fields; this should be executed whenever the DOM is reloaded

  // make the Cancel link from dialogs close the form
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
}

function schemata_ajaxify(el, active_region){

  set_actives();

  // TODO: this is a _temporary_ hack to make kupu work properly
  // the problem is probably that not all the DOM is loaded when the kupu editor
  // is initiated and so it freezes the editor
  // A proper fix would be to see if it's possible to delay the kupu load when it is
  // loaded through AJAX
  // This fix has one problem: it loads a frame (emptypage.html) that might not be completely
  // loaded in the timeout interval, and when that happens it throws an error

  $('.kupu-editor-iframe').parent().parent().parent().parent().each(function(){
    var kupu_id = $(this).attr('id');
    setTimeout(function(){
      initPloneKupu(kupu_id);
      $("#kupu-bold-button").trigger('click');
      $("#kupu-bold-button").trigger('click');
      // $("#kupu-bold-button").trigger('click');
    }, 1000);
  });

  $("form", el).submit(
    function(e){
      block_ui();
      var form = this;

      var inputs = [];
      $(".widgets-list .widget-name").each(function(){
        inputs.push($(this).text());
      });

      save_kupu_values(form);

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
}

function set_inout(el){
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
}

function dialog_edit(url, title, callback, options){
  // Opens a modal dialog with the given title

  block_ui();
  options = options || {
    'height':null,
    'width':800
  };
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
      $("#dialog-inner label").trigger('click');
      set_inout($("#archetypes-fieldname-themes"));
      callback();
    }
  });
  change_kupu_styles();
}

function set_editors(){
  // Set handlers for Edit (full schemata) buttons

  $('a.schemata_edit').live('click', function(){
    block_ui();
    var link = $(this).attr('href');
    var title = $(this).attr('title');
    var region = $(this).parents(".active_region")[0];

    // rewrite this to take advantage of metadata
    var options = {
      'width':800,
      'height':600
    };
    var active_region = region.id; //the region that will be reloaded

    dialog_edit(link, title, function(text, status, xhr){
      schemata_ajaxify($("#dialog-inner"), active_region);
      unblock_ui();
    },
  options);

  return false;
});
}

function set_edit_buttons() {
  // activate single active fields

  $('.active_field .control a').disableSelection();
  $('.active_field .control a').live('click', function(){

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

    var options = { 'width':800, 'height':600 };
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
}

function set_creators(){
  // Set handlers for Create buttons

  $('a.object_creator').live('click', function(){
    block_ui();
    var link = $(this).attr('href');
    var is_direct_edit = $(this).hasClass('direct_edit');
    var region = $(this).parents(".active_region")[0];
    var title = "Edit";
    var options = {
      'width':800,
      'height':600
    };
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
}

function set_deleters(){
  // Set handlers for Delete buttons

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
}


function closer(fieldname, active_region, url){
  // reloads a region and closes the dialog based on an active field name

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
}

function close_dialog(region){
  reload_region($("#"+region));
  $("#dialog-inner").dialog("close");
}


KupuEditor.prototype.getRichText = function(form, field) {
  // taken from saveDataToForm, because that function assumes too much
  var sourcetool = this.getTool('sourceedittool');
  if (sourcetool) {
    sourcetool.cancelSourceMode();
  }
  var transform = this._filterContent(this.getInnerDocument().documentElement);

  var contents = this.getXMLBody(transform);
  if (/^<body[^>]*>(<\/?(p|br)[^>]*>|\&nbsp;|\s)*<\/body>$/.test(contents)) {
    contents = ''; /* Ignore nearly empty contents */
  }
  var base = this._getBase(transform);
  contents = this._fixupSingletons(contents);
  contents = this.makeLinksRelative(contents, base).replace(/<\/?body[^>]*>/g, "");

  return contents;
};


function open_relations_widget(widget_dom_id, selected_tab){
  var widget = $("#"+widget_dom_id).get(0)._widget;
  window._selected_tab = selected_tab;// will be read by the relations widget and set as selected tab

  $("#" + widget_dom_id + " :input").trigger('click');
  return false;
}
function preselect_relations_tab(region_id, selected_tab){
  $("#" + region_id + " .searchButton").click(function(){
    window._selected_tab = selected_tab;// will be read by the relations widget and set as selected tab
    return true;
  });
}

$(document).ready(function () {

  set_editors();
  set_actives();
  set_creators();
  set_deleters();
  set_edit_buttons();

  on_load_dom();

});

// this.contentWindow.focus();//this should solve the problem that requires pressing the bold button

KupuZoomTool.prototype.commandfunc = function(button, editor) {
  // we rewrite the KupuZoomTool because we want to scroll the page
  /* Toggle zoom state */
  var zoom = button.pressed;
  this.zoomed = zoom;

  var zoomClass = 'kupu-fulleditor-zoomed';
  var iframe = editor.getDocument().getEditable();

  var body = document.body;
  var html = document.getElementsByTagName('html')[0];
  var doc = editor.getInnerDocument();

  if (zoom) {
    this.scrolled = jQuery(window).scrollTop();
    html.style.overflow = 'hidden';
    window.scrollTo(0, 0);
    editor.setClass(zoomClass);
    body.className += ' '+zoomClass;
    doc.body.className += ' '+zoomClass;
    this.onresize();
  } else {
    html.style.overflow = '';
    var fulleditor = iframe.parentNode;
    fulleditor.style.width = '';
    body.className = body.className.replace(/ *kupu-fulleditor-zoomed/, '');
    doc.body.className = doc.body.className.replace(/ *kupu-fulleditor-zoomed/, '');
    editor.clearClass(zoomClass);

    iframe.style.width = '';
    iframe.style.height = '';

    var sourcetool = editor.getTool('sourceedittool');
    var sourceArea = sourcetool?sourcetool.getSourceArea():null;
    if (sourceArea) {
      sourceArea.style.width = '';
      sourceArea.style.height = '';
    }
    var scrolled = this.scrolled;
    setTimeout(function(){
      window.scrollTo(0, scrolled);
    }, 200);    // TODO: this fix is a hack. Try to replace it.
  }
  // Mozilla needs this. Yes, really!
  doc.designMode=doc.designMode;

  window.scrollTo(0, iframe.offsetTop);
  editor.focusDocument();
};

function toggle_creator_option(el){
  var a = $(el).parent().parent().children('a.object_creator').get(0);
  var href = $(a).attr('href');
  if (!a.original_href) {
    a.original_href = href;
  }
  $(a).attr('href', a.original_href + "&create_in_latest_spec=" + $(el).attr('value'));
}

// vim: set sw=2 ts=2 softtabstop=2 et:
