function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}




// achive
function action(something){
    $.ajax({
	type: 'POST',
	url: '/achive/action',
	async: true,
	data: ({action : something, count:1, _xsrf : getCookie("_xsrf")}),
	dataType: "json"
    });
    achive_refresh();
}

function achive_refresh(){
    $.ajax({
	type: 'GET',
	url: '/achive/myachive',
	async:true,
	success: function(data){
	    $('#myachive').html(JSON.stringify(data))
	},
	dataType: "json"
    });
}


// feed
function post_to_wb(txt){
	$.ajax({
	  type: 'POST',
	  url: '/share/wb',
	  data: ({content : txt, _xsrf : getCookie("_xsrf")}),
	  success: function(data){
	    alert(data);
	  },
	  dataType: "json"
	});
}
function delete_feed(feedid){
	$.ajax({
	  type: 'POST',
	  url: '/feed/delete',
	  data: ({feedid : feedid, _xsrf : getCookie("_xsrf")}),
	  success: function(msg){
		$('#feed_'+feedid.toString().replace('.', '')).hide('normal');
	  },
	  dataType: "json"
	});
}


//task
function giveup_task(tid){
    $.ajax({
	type: 'POST',
	data: ({tid:tid, _xsrf : getCookie("_xsrf")}),
	url: '/task/giveup',
        async:true,
    });
}
function finish_task(tid){
    $.ajax({
	type: 'POST',
	url: '/task/finish',
	data: ({tid:tid, _xsrf : getCookie("_xsrf")}),
	async:true,
    });
}
function accept_task(tid){
    $.ajax({
        type: 'POST',
	data: ({tid:tid,  _xsrf : getCookie("_xsrf")}),
        url: '/task/accept',
        async:true,
    });
}

//mashup
function get_data(div_name, url){
    $.ajax({
        type: 'get',
        url: url,
        async: false,
        dataType: "json",
        success : function(data){
            switch (div_name)
            {
            case "contentArea":
                $("#contentArea").append("<h2>my feed story</h2><br>"+JSON.stringify(data));
                break;
            case "leftCol":
                $("#leftCol").append("<div id='profile'><h2>my profile</h2><br>"+JSON.stringify(data)+'</div>');
                break;
            case "rightCol":
                $("#rightCol").append("<h2>my follower</h2><br>"+JSON.stringify(data));
                break;
            }
        },
    });
}

// profile action
function profile_action(something){
    $.ajax({
        type: 'POST',
        url: '/profile/action',
        async: true,
        data: ({action : something, count:$('#action_count').val() , _xsrf : getCookie("_xsrf")}),
        dataType: "json"
    });
}


//msg
function read_msg(from, time){
    $.ajax({
	type: 'POST',
	url : '/msg/read',
	async: true,
	data :({msgtime:time, fromid:from, _xsrf:getCookie("_xsrf")}),
    });
    $('#'+from+"_"+time+"_content").show();
}

function delete_msg(from, time)
{
    $.ajax({
        type: 'POST',
        url : '/msg/delete',
        async: true,
        data :({msgtime:time, fromid:from, _xsrf:getCookie("_xsrf")}),
    });
    $('#'+from+"_"+time).hide();
}

//trade
function buy(itemid){
    $.ajax({
	type:'POST',
	url: '/trade/store/buy',
	data: ({itemid:itemid, _xsrf: getCookie("_xsrf")}),
	dataType: "html",
	success : function(data){alert(data)},
	error: function(data){alert(data.responseText)},
    });
}