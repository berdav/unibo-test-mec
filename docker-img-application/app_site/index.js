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
