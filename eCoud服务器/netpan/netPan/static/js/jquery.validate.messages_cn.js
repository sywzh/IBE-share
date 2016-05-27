/*
 * Translated default messages for the jQuery validation plugin.
 * Language: CN
 * Author: Fayland Lam <fayland at gmail dot com>
 */
jQuery.extend(jQuery.validator.messages, {
        required: "必选字段",
        remote: "请修正该字段",
        email: "请输入正确格式的电子邮件",
        url: "请输入合法的网址",
        date: "请输入合法的日期",
        dateISO: "请输入合法的日期 (ISO).",
        number: "请输入合法的数字",
        digits: "只能输入整数",
        creditcard: "请输入合法的信用卡号",
        equalTo: "请再次输入相同的值",
        accept: "请输入拥有合法后缀名的字符串",
        maxlength: jQuery.validator.format("请输入一个长度最多是 {0} 的字符串"),
        minlength: jQuery.validator.format("请输入一个长度最少是 {0} 的字符串"),
        rangelength: jQuery.validator.format("请输入一个长度介于 {0} 和 {1} 之间的字符串"),
        range: jQuery.validator.format("请输入一个介于 {0} 和 {1} 之间的值"),
        max: jQuery.validator.format("请输入一个最大为 {0} 的值"),
        min: jQuery.validator.format("请输入一个最小为 {0} 的值"),

});

//jquery Validate扩展验证
$(function(){

        //密码
        jQuery.validator.addMethod("passCheck",function(value, element){
        var str = /^[A-Za-z0-9!@#$%&]+$/ ;
                return this.optional(element) || str.test(value);
        }, "输入只能包含字母、数字和特殊字符!@#$%&");

        //用户名
        jQuery.validator.addMethod("userCheck",function(value, element){
        var str = /^[\u0391-\uFFE5A-Za-z0-9]+$/ ;
                return this.optional(element) || str.test(value);
        }, "输入只能包含汉字、字母、数字");

        //邮箱
        jQuery.validator.addMethod("emailCheck",function(value, element){
          var str = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
        
                return this.optional(element) || str.test(value);
        }, "请输入正确的e-mail格式");

});