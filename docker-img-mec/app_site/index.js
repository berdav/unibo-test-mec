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
	_get_query("service/subscribe");
}

var service_unsubscribe = function() {
	_get_query("service/unsubscribe");
}

var dns_rules = function() {
	_get_query("dns_rules");
}

var dns_rule_activate = function() {
	_get_query("dns_rule/ACTIVE");
}

var dns_rule_deactivate = function() {
	_get_query("dns_rule/INACTIVE");
}
