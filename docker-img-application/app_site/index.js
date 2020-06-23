/* 5g MEC Related */
var _updateResult = function(data) {
	$( "#result" ).text(
		data
	)
}

var _get_query = function(endpoint) {
	$.get(endpoint).done(_updateResult);
}

var services = function() {
	_get_query("services");
}

var transports = function() {
	_get_query("transports");
}

var service_subscribe = function() {
	_get_query("services/subscribe");
}

var service_unsubscribe = function() {
	_get_query("services/unsubscribe");
}

var dns_rules = function() {
	_get_query("dns_rules");
}

var dns_rule_activate = function() {
	_get_query("dns_rules/ACTIVE");
}

var dns_rule_deactivate = function() {
	_get_query("dns_rules/INACTIVE");
}

var notifications = function() {
	_get_query("notifications")
}

var notification_subscribe = function() {
	_get_query("notifications/subscribe")
}

var notification_unsubscribe = function() {
	_get_query("notifications/unsubscribe")
}

var notify_ready = function() {
	_get_query("notifications/notify_ready")
}

var timings_caps = function() {
	_get_query("timings/timing_caps")
}

var timings_current_time = function() {
	_get_query("timings/current_time")
}

var start_ptp = function() {
	_get_query("timings/_start_ptp")
}

var ptp_status = function() {
	_get_query("timings/_ptp_status")
}

var ptp_time = function() {
	_get_query("timings/_ptp_time")
}

var traffic_rules = function() {
	_get_query("dns_rules");
}

var traffic_rule_activate = function() {
	_get_query("traffic_rules/ACTIVE");
}

var traffic_rule_deactivate = function() {
	_get_query("traffic_rules/INACTIVE");
}

var application_interaction = function() {
	_get_query("_contactapplication")
}

setInterval(function() {
	$.get("_get_application_notice").done( function(data) {
		console.log(data)
		if (data === 'True') {
			$( "#service_ready_led" ).css(
				"background-color",
				"green"
			)
		}
	});
}, 1000)

var activeMenu = 'services'

/* UI related */
var activate_menu = function(menu) {
	$( `#${activeMenu}` ).removeClass('d-block')
	$( `#${activeMenu}` ).addClass('d-none')
	$( `#nav${activeMenu}` ).removeClass('active')
	$( `#${menu}` ).removeClass('d-none')
	$( `#${menu}` ).addClass('d-block')
	$( `#nav${menu}` ).addClass('active')

	activeMenu = menu
}
