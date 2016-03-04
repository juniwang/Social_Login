$(function(){
    function getUrlParam(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    }

    var redirect_url = $.cookie('redirect_url') + "?code=" + getUrlParam('code') + "&identity_provider=" +
                        $.cookie('identity_provider') + "&aad_openid=" + $("#aad_openid").attr('content');
    //alert($("#aad_openid").attr('content'));
    $.cookie('redirect_url', null);
    $.cookie('identity_provider', null);
    $(window.location).attr('href', redirect_url);
})