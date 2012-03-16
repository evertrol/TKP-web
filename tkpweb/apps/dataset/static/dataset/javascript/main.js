$(function ()
{
    $("img#sourceplot_0").load(function(){$("div#lightcurve").css('height', $(this).height())});
    $("img.thumbnail").hover(
        function ()
	{
	    $("img#sourceplot_" + $(this).attr("number")).css('display', 'block');
	},
	function ()
	{
	    $("img#sourceplot_" + $(this).attr("number")).css('display', 'none');
	});
});
