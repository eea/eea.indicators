function change_kupu_styles(){
		$(".kupu-tb-styles option[value='h2|']").remove();
		$(".kupu-tb-styles option[value='h3|']").remove();
}
$(document).ready(function () {
		$(".kupu-table").remove();
		$('.kupu-image').remove();
		setTimeout('change_kupu_styles()', '2000');
});

