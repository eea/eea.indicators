var DavizChartSelection = function(btn){
        this.btn = $(btn);
        this.popup = $("<div>");
        //this.popup.addClass('xxx');
        this.btn.after(this.popup);
        this.popup.html('<p><label>Select chart</label></p>');

        var select = this.btn.parent().find('select')
        var form = select.parents('form');
        console.log(form);
        select.detach();
        this.popup.append(select);

        this.popup.dialog({
            modal:true,
            buttons:{
                'OK':function(){
                    form.append(select);
                    $(this).dialog('close');
                }, 
                'Cancel':function(){
                    form.append(select);
                    $(this).dialog('close');
                }
            }
        });

};

// DavizChartSelection.prototype = { }
