$(document).ready(function(){
	$("a[rel*=leanModal]").leanModal({overlay:0.5, closeButton:".modal_close"});
});

/* 首页more按钮跳转——hockor(2014-03-13 19：38)*/
function click_scroll() {
  var scroll_offset = $("#explain").offset();  //得到pos这个div层的offset，包含两个值，top和left
  $("html,body").animate({
   scrollTop:scroll_offset.top  //让body的scrollTop等于pos的top，就实现了滚动
   },500);
 }


/*全选反选功能——hockor(2014-03-17)*/

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

/*弹出框*/
$(document).ready(function(){
	$("a[rel*=upload]").leanModal({overlay:0.5, closeButton:".modal_close"});
});/*上传弹出框*/

$(document).ready(function(){
	$("a[rel*=layer]").leanModal({overlay:0.5, closeButton:".modal_close"});
});/*其他样式的弹出框*/
$(document).ready(function(){
	$("a[rel*=file]").leanModal({overlay:0.5, closeButton:".modal_close"});
});

/*鼠标变色*/
window.onload=function showtable(){
	var TableName=document.getElementById("table")
	var tr=document.getElementsByTagName("tr")
		for(var i=1;i<=tr.length;i++){
			tr[i].style.backgroundColor="#BEBCBC";
			tr[i].onmouseover=function(){
			this.style.backgroundColor="#EDEDED";
			}
			tr[i].onmouseout=function(){
			this.style.backgroundColor="#BEBCBC";
		}
	}
}
/*邮箱验证*/
$(function(){
	$("#regsiter_email").blur(function(){
		if($(this).val()==''){
			$("#emailInfo").text("邮箱不能为空！")；
			$(this).focus();
		}
		else{
			if(/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test($(this).val()) == false){
				$("#emailInfo").text("邮箱格式不正确，请重新填写！");
				$(this).focus();
			}
			else{
				$("#emailInfo").text("正确");
				state=true;
			}
		}
	})
})
/*密码长度验证*/
$(function(){
	$("#register_password").blur(function(){
		var pwd = document.getElementById("register_password").value;
		if($(this).val()==''){
			$("#passwordInfo").text("密码不能为空！");
			$(this).focus();
		}
		else{
			if(pwd.length<6 || pwd.length > 12){
				$("#passwordInfo").text("密码长度在6-12位！");
				$(this).focus();
			}
			else{
				$("#passwordInfo").text("正确");
				state=true;
			}
		}
	})
})
