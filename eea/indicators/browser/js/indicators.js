function change_kupu_styles(){
	$(".kupu-table").remove();
	$('.kupu-image').remove();
	$(".kupu-tb-styles option[value='h2|']").remove();
	$(".kupu-tb-styles option[value='h3|']").remove();
}
$(document).ready(function () {
		setTimeout('change_kupu_styles()', '2000');
		});

function dialog_edit(url, title){
	var target = $('#dialog_edit_target');
	$(target).append("<div id='dialog-inner'></div>");
	$("#dialog-inner").dialog({modal:true, width:700, minWidth:700, 'title':title});
	// width:700, height:450, minHeight:450, minWidth:700, 
	$("#dialog-inner").load(url);
	change_kupu_styles();
}

(function($) {
 $.fn.make_editable = function(link, title) {
 return this.each(function() {
	 $('a', this).click(function(e){
		 var title = $(this).text();
		 var link = $(this).attr('href');
		 dialog_edit(link, title);
		 return false;
		 });
	 });
 };
 })(jQuery);

