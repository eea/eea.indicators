function change_kupu_styles(){
  // customize the Kupu editor to IMS standards
	$(".kupu-table").remove();
	$('.kupu-image').remove();
	$(".kupu-tb-styles option[value='h2|']").remove();
	$(".kupu-tb-styles option[value='h3|']").remove();
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

$(document).ready(function () {

		set_editors();
		set_actives();
		set_creators();
		set_deleters();
    set_edit_buttons();

		// setTimeout('change_kupu_styles()', '2000');

		on_load_dom();

    // styling tweak for relations widget edit button
    $(".eea-widget-referencebrowser").each(function(){
      var parent = $(this).parent();
      $(parent).prepend(this);
      });

});

function on_load_dom() {
	// executed whenever the regions are reloaded

	set_sortables();
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

function set_sortables() {
	// make certain DOM elements sortable with jquery UI sortable

	$('.sortable_spec').each(function(){
      var handler = $(".metadata .handler", this).text();
      $(this).sortable({
          'handle':'.handler',
          'items':'.list-item',
          placeholder: 'ui-state-highlight',
          // containment: 'parent'	// has a bug in UI, sometimes it's impossible to move #2 to #1
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
              'data':data,
              'success':function(){
                unblock_ui()
              }
            });
          }
        });
      $('.sortable_spec').disableSelection();

      });
}

function set_editors(){
	// Set handlers for Edit (full schemata) buttons

	$('a.schemata_edit').live('click', function(){
      block_ui();
			var link = $(this).attr('href');
			var title = $(this).text();
			var region = $(this).parents(".active_region")[0];
			var options = {
			'width':800,
			'height':600
			}
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

  $('.active_field a').disableSelection();
	$('.active_field a').live('click', function(){
      block_ui();
			var link = $(this).attr('href');
			var title = $(this).text();
			var region = $(this).parents(".active_region")[0];
      var field = $(this).parents('.active_field')[0];

			var active_region = region.id; //the region that will be reloaded

      var content = $('.content', field).get();
      var metadata = $('.metadata', field);
      var fieldname = $('.metadata > .fieldname', field).text();

			var options = { 'width':800, 'height':600 }
      options.height = Number($('.metadata > .height', field).text()) || options.height;
      options.width = Number($('.metadata > .width', field).text()) || options.width;

      var id_to_fill = 'active_field-' + fieldname
      $(content).attr('id', id_to_fill);
      dialog_edit(link, title, function(text, status, xhr){
				// schemata_ajaxify($("#dialog-inner"), fieldname);
        ajaxify($("#dialog-inner"), fieldname);
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
			var region = $(this).parents(".active_region")[0];
      var title = "Edit";
      var options = {
        'width':800,
        'height':600
      }
			$.ajax({
          url: link,
          type:'GET',
          // timeout: 2000,
          error: function() {
            unblock_ui();
            alert("ERROR: There was a problem communicating with the server. Please reload this page.");
          },
          success: function(r) {
            reload_region($(region));
            var info = $(r).children('.object_edit_url');
            if (info) {
              var edit_link = info.text();
              dialog_edit(edit_link, title, function(text, status, xhr){
                schemata_ajaxify($("#dialog-inner"), $(region).attr('id'));
                unblock_ui();
                },
                options
              );
            } else {
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

function reload_region(el){
  block_ui();
	var update_handler = $(".metadata .region_update_handler", el).text();
  var also_reload = $(".metadata .also_reload", el);
  if (also_reload) {
    $(also_reload).children().each(function(){
        var region = $(this).text();
        if (region) {
          reload_region($("#"+region))
        }
    });
  }

	$.ajax({
        url: update_handler,
        type:'GET',
        // timeout: 2000,
        error: function() {
          unblock_ui();
          alert("ERROR: There was a problem communicating with the server. Please reload this page.");
        },
        success: function(r) {
            var id = $(el).attr('id');
            $(el).replaceWith(r);
            on_load_dom();
            var new_el = $("#"+id);
            $(new_el).effect('highlight');
            // $(new_el).animate({backgroundColor:'#e1e1e1'}, 1000)
            //         .animate({backgroundColor:'transparent'}, 1500);
            unblock_ui();
            return false;
        }
        });

  return false;
}

function closer(fieldname, active_region){
  // reloads a region and closes the dialog based on an active field name

  //TODO: check that these 3 commented lines don't break anything;
  //they don't seem to be needed if we reload the region
	// var text = $('#value_response').html(); // 1

  if (active_region) {
    var region = $("#" + active_region).get();
  } else {
    var fieldname = "#active_field-"+fieldname;
    var region = $(fieldname).parents('.active_region').get();
  }

  // console.log("Closing & reloading region", region);
  reload_region(region);

	// $(fieldname).html(text);   // 2
	// $('#value_response').remove(); // 3

	$("#dialog-inner").dialog("close");
	return false;
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
};

function dialog_edit(url, title, callback, options){
	// Opens a modal dialog with the given title

  block_ui();
	options = options || {
		'height':null,
			'width':800,
	}
	var target = $('#dialog_edit_target');
	$("#dialog-inner").remove();     // temporary, apply real fix
	$(target).append("<div id='dialog-inner'></div>");
  window.onbeforeunload = null; // disable form unloaders
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
						var form = $("#dialog-inner form").get(0);
						var e = document.createEvent("HTMLEvents");	// TODO: replace with jquery's trigger()
						e.initEvent('submit', true, true);
						form.dispatchEvent(e);	// TODO: need to check compatibility with IE
					},
					'Cancel':function(e){
						$("#dialog-inner").dialog("close");
					}
				},
        beforeclose:function(event, ui){
            return true;
            var form = $("#dialog-inner form").get(0);
            beforeunloadtool = window.onbeforeunload && window.onbeforeunload.tool;
            save_kupu_values(form);
            var res = beforeunloadtool.isAnyFormChanged();

            beforeunloadtool.removeForms(form);
            return true;    // TODO: fix this so that the form unload alert works properly

            // if (beforeunloadtool) {
            //   save_kupu_values(form);
            //   if (beforeunloadtool.isAnyFormChanged()) {
            //      // the problem is that it falsely detects changed content;
            //     alert(window.onbeforeunload.tool.execute());
            //     return false;
            //   } else {
            //     return true;
            //   };
            // }
          }
				});

	$("#dialog-inner").load(url, callback);
	change_kupu_styles();
};


function close_dialog(region){
    reload_region($("#"+region));
    $("#dialog-inner").dialog("close");
}


function get_kupu_editor(editorId) {
	// initializes a kupu editor and returns it.
	// This is needed to make up for the lack of proper API:
	// we can't get the kupu editor back from just the iframe or whatever
	// The content here is taken from initPloneKupu()

	var prefix = '#'+editorId+' ';

	var iframe = getFromSelector(prefix+'iframe.kupu-editor-iframe');
	var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
	var form = textarea.form;

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


KupuEditor.prototype.getRichText = function(form, field) {
	// taken from saveDataToForm, because that function assumes too much
	var sourcetool = this.getTool('sourceedittool');
	if (sourcetool) {sourcetool.cancelSourceMode();};
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


function ajaxify(el, fieldname){
	// This will make a form submit and resubmit itself using AJAX
	// It also takes care of kupu mangling

	$('.kupu-editor-iframe').parent().parent().parent().parent().each(function(){
			var kupu_id = $(this).attr('id');
			setTimeout(function(){
				initPloneKupu(kupu_id);
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
};

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

// vim: set sw=2 ts=2 et:
//
