var DavizChartSelection = function (btnel) {
        var btn = $(btnel);
        var divparent = btn.parent().parent();
        var metadata = divparent.find('.metadata');
        var popup = $("<div>");

        btn.after(popup);
        popup.html('<p><label>Select chart</label></p>');

        var select = divparent.find('select');
        var cloned_select = select.clone();
        popup.append(cloned_select);

        var uid = metadata.find('.daviz_uid').text();
        var url = metadata.find('.url').text();

        var chart_titles = $(divparent).find('.chart-titles');

        popup.dialog({
            modal:true,
            buttons:{
                'OK':function(){
                    select.replaceWith(cloned_select);
                    chart_titles.find('span').remove();
                    $(cloned_select).find('option:selected').each(function(){
                        var span = $("<span>");
                        span.addClass("chart-title");
                        span.text($(this).text());
                        chart_titles.append(span);
                    });
                    var b = this;
                    $.ajax({
                        type:'POST',
                        url:url, 
                        data:{ 
                            'chart':cloned_select.serialize(),
                            'daviz_uid':uid
                        },
                        error:function(){
                            alert("Could not save data on server");
                        },
                        success:function(){
                            $(b).dialog('close');
                        }
                    });
                }, 
                'Cancel':function(){
                    // select.replaceWith(cloned_select);
                    $(this).dialog('close');
                }
            }
        });

};
