/*
*应用于所有页面
*/

$(document).ready(function(){
	$("a[rel*=dialog]").leanModal({overlay:0.4, closeButton:".modal_close"}); //弹出框
	setMenuCss(); //页面ul菜单栏样式切换
	$('#table').alterBgColor();
});

//ajax全局请求
$(document).ajaxStart(function(){
	$('.ajaxLoading').show();
}).ajaxStop(function(){
	$('.ajaxLoading').hide();
});

//提示信息 by duym(2014-5-17)
var errorInfoFlag = false;
var infoFlag = false;

function showInfo(infoText){
	errorInfoFlag = true;
	$('.info-box').clearQueue();
	$('.info-box').stop();
	$('.info-box').text(infoText);
	$('.info-box').css({'margin-left': '-' + $('#info-box').width()/2 + 'px'});
	$('.info-box').show();
	setTimeout(function(){
		$('.info-box').fadeOut('normal');
		errorInfoFlag = false;
	}, 2000);//设置提示出现时间为2秒
}
//首页more按钮跳转——hockor(2014-03-13 19：38)
function click_scroll() {
  var scroll_offset = $("#explain").offset();  //得到pos这个div层的offset，包含两个值，top和left
  $("html,body").animate({
   scrollTop:scroll_offset.top  //让body的scrollTop等于pos的top，就实现了滚动
   },500);
 }

function hideDialog(){ //自动隐藏弹出框
    	$('.modal_close').click();
    }

//全选反选功能——hockor(2014-03-17)
var selAll = document.getElementById("selAll"); 
	function selectAll() 
		{ 
  		var obj = document.getElementsByName("checkAll"); 
  			if(document.getElementById("selAll").checked == false) 
  				{ 
  					for(var i=0; i<obj.length; i++) 
  						{ 
    						obj[i].checked=false; 
  						} 
  				}
  			else
  				{ 
 			 		for(var i=0; i<obj.length; i++) 
  				{	  
    				obj[i].checked=true; 
  				}			
  			}  
	} 

//当选中所有的时候，全选按钮会勾上 
function setSelectAll() 
	{ 
		var obj=document.getElementsByName("checkAll"); 
		var count = obj.length; 
		var selectCount = 0; 

	for(var i = 0; i < count; i++) 
	{ 
		if(obj[i].checked == true) 
			{ 
				selectCount++;	
			} 
	} 
		if(count == selectCount) 
			{	
				document.all.selAll.checked = true; 
			} 
		else 
			{ 
				document.all.selAll.checked = false; 
			} 
	} 

//反选按钮 
function inverse() { 
	var checkboxs=document.getElementsByName("checkAll"); 
		for (var i=0;i<checkboxs.length;i++) { 
  			 var e=checkboxs[i]; 
  			 e.checked=!e.checked; 
  			 setSelectAll(); 
	} 
} 

//页面ul菜单栏样式切换 by duyanmei
function setMenuCss(){
	$('.top_nav ul li').each(function(){
		var _this = this;
		$(_this).click(function(){
			$(_this).addClass('topul_hover').siblings().removeClass('topul_hover');
		});
	});
}