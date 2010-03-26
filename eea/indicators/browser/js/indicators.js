function change_kupu_styles(){
	$(".kupu-table").remove();
	$('.kupu-image').remove();
	$(".kupu-tb-styles option[value='h2|']").remove();
	$(".kupu-tb-styles option[value='h3|']").remove();
}
$(document).ready(function () {
		setTimeout('change_kupu_styles()', '2000');
		});

function dialog_edit(url, title, callback){
	var target = $('#dialog_edit_target');
	$(target).append("<div id='dialog-inner'></div>");
	$("#dialog-inner").dialog({modal:true, width:700, minWidth:700, 'title':title});
	// width:700, height:450, minHeight:450, minWidth:700, 
	$("#dialog-inner").load(url, callback);
	change_kupu_styles();
}

window.kupu_id = null;

(function($) {
 $.fn.make_editable = function(link, title) {

 return this.each(function() {
	 $('a', this).click(function(e){
		 var title = $(this).text();
		 var link = $(this).attr('href');
		 dialog_edit(link, title, function(text, status, xhr){
			 $('.kupu-editor-iframe').parent().parent().parent().parent().each(function(){
				 window.kupu_id = $(this).attr('id');
				 // TODO: this is a temporary hack to make kupu work properly
				 // the problem is probably that not all the DOM is loaded when the kupu editor
				 // is initiated and so it freezes the editor
				 // A proper fix would be to see if it's possible to delay the kupu load when it is 
				 // loaded through AJAX
				 // This fix has two problems: it uses a global variable (window.kupu_id) - but 
				 // this is easily fixable; it loads a frame (emptypage.html) that might not be completely
				 // loaded in the timeout interval, and when that happens it throws an error
				 setTimeout('initPloneKupu(window.kupu_id)', 500);
				 });
			 });
		 return false;
		 });
	 });
 };
 })(jQuery);

// 
