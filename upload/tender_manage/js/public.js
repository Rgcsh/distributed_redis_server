//本地使用
serverUrl = '//127.0.0.1:5000/'
serverUrl_user = serverUrl + 'user/'
serverUrl_fund_info = serverUrl + 'fund_info/'
serverUrl_order = serverUrl + 'order/'
serverUrl_weburl = serverUrl+ 'upload/tender_manage/'

//	弹窗消失
function hide_popover(name, get_text) {
	$(name).parent().find("label").text(get_text)
	$(name).removeAttr('disabled')
}

//屏蔽点击事件
function disabled_click(name) {
	$(name).attr({
		'disabled': 'disabled'
	})
}

function login_cookies_set(get_data) {
	console.log(get_data.result)
	var token = get_data.result['token']
	var email = get_data.result['email']
	var user_id = get_data.result['id']
	expire_time = {
		expires: 1
	}
	$.cookie('token', token, expire_time);
	$.cookie('email', email, expire_time);
	$.cookie('user_id', user_id, expire_time);
}

function cookies_remove() {
	$.cookie('token', null);
	$.cookie('email', null);
	$.cookie('user_id', null);
	$.cookie('role_type', null);
	$.cookie('username', null);
	$.cookie('user_department', null);
	$.cookie('user_no', null);
}
//api接口出错事件
//function api_error(name){
//	disabled_click()
//	
//}
