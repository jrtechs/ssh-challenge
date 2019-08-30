for(var i = 0; i < 500; i++)
{
	console.log("Sending stonks.");
	$.ajax({
		type:'POST',
		url: "/stonks",
		crossDomain: true,
		dataType: "json",
		timeout: 3000
	});
}
