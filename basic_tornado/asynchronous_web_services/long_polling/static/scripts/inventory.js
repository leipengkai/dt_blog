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
//requestInventory函数在页面完成加载后经过一个短暂的延迟再进行调用。在函数主体中，我们通过到/cart/status的HTTP GET请求初始化一个长轮询。
//延迟允许在浏览器完成渲染页面时使加载进度指示器完成，并防止Esc键或停止按钮中断长轮询请求。当请求成功返回时，count的内容更新为当前的库存量
	jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
		function(data, status, xhr) {
			$('#count').html(data['inventoryCount']);
			setTimeout(requestInventory, 0);
		}
	);
}