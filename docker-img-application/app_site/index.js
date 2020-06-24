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
	_get_query("traffic_rules");
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

var get_configuration = function() {
	$.get("_configuration").done( function (data_s) {
		data = JSON.parse(data_s)
		console.log("%o", data)
		Object.keys(data).forEach((key) => {
			if (typeof(data[key]) === 'string') {
				$( `#${key}` ).val(
					data[key]
				)
			} else {
				$( `#${key}` ).val(
					JSON.stringify(data[key], null, 4)
				)
			}
		})
	})
}

var put_configuration = function() {
	data = {};
	[ "mec_base", "target_service", "other_application_uri", "app_instance_id" ].forEach((k) => {
		data[k] = $( `#${k}` ).val()
	})

	text_area_keys = ["service_data"];
	// Text areas input
	text_area_keys.forEach((key) => {
		data[key] = JSON.parse($( `#${key}` ).val())
	})

	// success feedback?
	$.ajax({
		url:'_configuration',
		type:'POST',
		data: JSON.stringify(data),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
	})
}


setInterval(function() {
	$.get("_get_application_notice").done( function(data) {
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
