//writen by dym 2014/4/7

;(function($){
	$.fn.extend({
		"alterBgColor": function(options){

			//设置默认值
			options = $.extend({
				origin: "originColor",
				hover: "hoverColor",
				selected: "selectedColor"
			}, options);
			$('tbody tr:not(.firstTr)', this).css("cursor", "pointer");
			$('tbody tr', this).addClass(options.origin);
			$('tbody tr:not(.firstTr)', this).mouseover(function(){
				$(this).addClass(options.hover);
			}).mouseout(function(){
				$(this).removeClass(options.hover);
			});
			$('tbody tr:not(.firstTr)', this).click(function(){

				//判断当前是否选中
				var hasSelected = $(this).hasClass(options.selected);
				$(this)[hasSelected?"removeClass":"addClass"](options.selected).find(':checkbox').attr('checked',!hasSelected);
			});

			//如果单选框默认情况下是选中的，则高亮
			$('tbody tr:not(.firstTr):has(:checked)', this).addClass(options.selected);
            
            //返回this,是方法可连缀
			return this;
		}
	});
})(jQuery);