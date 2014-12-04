function refreshlist(){
    var url = "remain";
    $.ajax({
         url: url,
         dataType: 'json',
         success: function( data ) {
            $("#AC_P").text(data[0]);
            $("#daypower").text(data[1]);
            $("#allpower").text(data[2]/1000.0);
         },
         error: function( data ) {
            $("#AC_P").text(0);
            $("#daypower").text(0);
            $("#allpower").text(0);
        }
    });
}
   
function loaddaydata(datas)
{
    var d1 = [];
    var d2 = datas;
    var d4 =[];
    for (var i = 0; i < 24; i += 1) {
        d1.push([i, d2[i]]);
        if(Math.round((i+1)%2) ==0 ){d4.push([i,i]);}      
    }

    $.plot("#placeholder", [{
            data: d1,
            color: "#5482FF"
        }],{
            series: {
                bars: {
                    show: true
                }
            },
            bars: {
               // align: "center",
                barWidth: 0.95,
                show: true,
                showNumbers: true,
            },
            yaxis:{min:0},
            xaxis: {ticks:d4}
        });  
}

function loadmonthdata(datas)
{
    var d1 = [];
    var d2 = datas;
    var d4 =[];
    for (var i = 0; i < datas.length; i += 1) {
        d1.push([i, d2[i]]);
        if(Math.round((i+1)%4) ==0 ){d4.push([i,i]);}      
    }

    $.plot("#placeholder", [{
            data: d1,
            color: "#5482FF"
        }],{
            series: {
                bars: {
                    show: true
                }
            },
            bars: {
               // align: "center",
                barWidth: 0.95,
                show: true,
                showNumbers: true,
            },
            yaxis:{min:0},
            xaxis: {ticks:d4}
        });  
}

function reloaddaychart(num){
    var daydataurl = "reDayPower";
    $.ajax({
        url: daydataurl,
        type: "GET",
        dataType:"json",
        data:{    
            sinum:num,
            day:$("#inputday").val()
         },
        success:function(data){
            loaddaydata(data);
        },
        error : function() {    
        }  
    });
}

function reloadmonthchart(num){
    var monthdataurl = "reMonthPower";
    $.ajax({
        url: monthdataurl,
        type: "GET",
        dataType:"json",
        data:{    
            sinum:num,
            day:$("#inputday").val()
         },
        success:function(data){
            loadmonthdata(data);
        },
        error : function() {    
        }  
    });
}

function ThisDay()
{
    var now = new Date();      
    var year = now.getFullYear();       //年
    var month = now.getMonth() + 1;     //月
    var day = now.getDate();            //日

    var clock = year + "-";       
    if(month < 10)
        clock += "0";      
    clock += month + "-";       
    if(day < 10)
        clock += "0";          
    clock += day;
    $("#inputday").val(clock);
}

function reloadchart(num)
{
    if($("#mselect").val()==1){
        reloaddaychart(num);
    }else{
        reloadmonthchart(num);
    }
}