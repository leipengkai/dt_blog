$(document).ready(function() {
	document.session = $('#session').val();
	
	setTimeout(requestInventory, 100);
	
	$('#add-button').click(function(event) {
		jQuery.ajax({
			url: '//localhost:8000/cart',
			type: 'POST',
			data: {
				session: document.session,
				action: 'add'
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
			},
			success: function(data, status, xhr) {
				$('#add-to-cart').hide();
				$('#remove-from-cart').show();
				$(event.target).removeAttr('disabled');
			}
		});
	});
	
	$('#remove-button').click(function(event) {
		jQuery.ajax({
			url: '//localhost:8000/cart',
			type: 'POST',
			data: {
				session: document.session,
				action: 'remove'
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
			},
			success: function(data, status, xhr) {
				$('#remove-from-cart').hide();
				$('#add-to-cart').show();
				$(event.target).removeAttr('disabled');
			}
		});
	});
});

function requestInventory() {
	var host = 'ws://localhost:8000/cart/status?session=' + document.session;
	
	var websocket = new WebSocket(host);
    websocket.send('oiRRFw8XxXgLi4oiSiGgHTkr1pbY')
//    	C --> S
	websocket.onopen = function (evt) { };
	websocket.onmessage = function(evt) {  // S --> C
		$('#count').html($.parseJSON(evt.data)['inventoryCount']); // 我们必须手工解析服务器送来的JSON对象
	};
	websocket.onerror = function (evt) { };
}