$(document).ready(function() {
	var buttons = ['0', '1'];
	
	var hup = "hang_up";
	var pup = "pick_up";

	$("#mp_receiver")
		.html(pup)
		.click(function() {
			if($(this).html() == hup) {
				next_state = pup;
			} else if($(this).html() == pup) {
				next_state = hup;
			}

			$.ajax({
				url : $(this).html(),
				context : this
			}).done(function(json) {
				console.info(json);				
				$(this).html(next_state);
			});
		});
	
	var tr = $(document.createElement('tr'));

	for(var i=0; i<buttons.length; i++) {
		var td = $(document.createElement('td'));
		var a = $(document.createElement('a'))
			.html("<p class=\"num\">" + buttons[i] + "</p>")
			.click(function() {
				var mapping = $($(this).find('.num')[0]).html();
				$.ajax({
					url : "mapping/" + (Number(mapping) + 3)
				}).done(function(json) {
					console.info(json);
				});
			});

		$(td).append(a);
		$(tr).append(td);
	}

	$("#mp_main").append(tr);
});