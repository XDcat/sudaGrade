/**
 *解决toekn 过期 异地登录问题
 *
 * */

/**
 * 时间戳转时间
 * */
function getLocalTime(nS) {
    return new Date(parseInt(nS)).toLocaleString().replace(/:\d{1,2}$/, ' ');
}

/**
 * yyyy-MM-dd HH:mm:ss
 * */
function getLocalTime(value) {
    var time = new Date(value);
    var y = time.getFullYear();
    var m = time.getMonth() + 1;
    var d = time.getDate();
    var h = time.getHours();
    var mm = time.getMinutes();
    var s = time.getSeconds();
    return y + '-' + add0(m) + '-' + add0(d) + ' ' + add0(h) + ':' + add0(mm) + ':' + add0(s);
}

/**
 * yyyy-MM-dd
 * */
function getSimpleLocalTime(value) {
    var time = new Date(value);
    var y = time.getFullYear();
    var m = time.getMonth() + 1;
    var d = time.getDate();
    return y + '年' + add0(m) + '月' + add0(d) + "日";
}

/**
 * datetime-local
 * 2017-06-08T15:30
 */
function timeDateTimeLocal(value) {
    var time = new Date(value);
    var y = time.getFullYear();
    var m = time.getMonth() + 1;
    var d = time.getDate();
    var h = time.getHours();
    var mm = time.getMinutes();
    var s = time.getSeconds();
    return y + '-' + add0(m) + '-' + add0(d) + 'T' + add0(h) + ':' + add0(mm);
}

function add0(m) {
    return m < 10 ? '0' + m : m
}

/**
 * 日期格式化
 * */
Date.prototype.format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

/**
 * map
 * */
function Map() {
    var struct = function (key, value) {
        this.key = key;
        this.value = value;
    }
    var put = function (key, value) {
        for (var i = 0; i < this.arr.length; i++) {
            if (this.arr[i].key === key) {
                this.arr[i].value = value;
                return;
            }
        }
        this.arr[this.arr.length] = new struct(key, value);
    }
    var get = function (key) {
        for (var i = 0; i < this.arr.length; i++) {
            if (this.arr[i].key === key) {
                return this.arr[i].value;
            }
        }
        return null;
    }
    var remove = function (key) {
        var v;
        for (var i = 0; i < this.arr.length; i++) {
            v = this.arr.pop();
            if (v.key === key) {
                continue;
            }
            this.arr.unshift(v);
        }
    }
    var size = function () {
        return this.arr.length;
    }
    var isEmpty = function () {
        return this.arr.length <= 0;
    }
    this.arr = new Array();
    this.get = get;
    this.put = put;
    this.remove = remove;
    this.size = size;
    this.isEmpty = isEmpty;
}

/*
 倒计时
 * */
function countTimeByNow(t) {
    var newD = parseInt(t) + 24 * 60 * 60 * 1000;
    var t1 = getLocalTime(newD);
    if (new Date(t1) - new Date() > 0) {
        var d = cd(t1, new Date(), 'd');
        var h = cd(t1, new Date(), 'h');
        var m = cd(t1, new Date(), 'm');
        var s = cd(t1, new Date(), 's');
        return d + '天' + h + '时' + m + '分' + s + '秒';
    }
    return "";
}

/*
获取倒计时 返回值数字
t1 开始时 时间格式
t2 结束时 时间格式
tg 要获取的值 字符串
  d 天
  h 时
  m 分
  s 秒
*/
function cd(t1, t2, tg) {
    //相差的毫秒数
    var ms = Date.parse(t1) - Date.parse(t2);
    var minutes = 1000 * 60;
    var hours = minutes * 60;
    var days = hours * 24;
    var years = days * 365;
    //求出天数
    var d = Math.floor(ms / days);
    //求出除开天数，剩余的毫秒数
    ms %= days;
    var h = Math.floor(ms / hours);
    ms %= hours;
    var m = Math.floor(ms / minutes);
    ms %= minutes;
    var s = Math.floor(ms / 1000);
    //返回所需值并退出函数
    switch (tg) {
        case 'd':
            return d;
        case 'h':
            return h;
        case 'm':
            return m;
        case 's':
            return s;
    }
}

/*
 *
 * 获取token
 *
 * */

function getToken() {
    var token = getUrlParam("token");
    if (token) {
        setCookie("token", token);
    } else {
        token = getCookie("token")
    }
    return token;
}

/*
 *
 * 获取 uerNo
 *
 * */

function getUserNo() {
    var userNo = getUrlParam("userNo");

    if (userNo) {
        setCookie("userNo", userNo);
    } else {
        userNo = getCookie("userNo")
    }
    return userNo;
}

/*
 *
 * 存储cokie
 *
 * */
function setCookie(name, value) {
    var Days = 90;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    if (name == "token" || name == "referer_url" || name == "userNo" || name == "app") {
        removeCookie(name);
        document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/";
    } else {
        document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
    }
}

function removeCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 30 * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape("") + ";expires=" + exp.toGMTString();
    try {
        if (name == "token" || name == "referer_url" || name == "userNo" || name == "app") {
            document.cookie = name + "=" + escape("") + ";expires=" + exp.toGMTString() + ";path=/";
        }
    } catch (e) {
    }
}

/*
 *
 * 获取cokie
 *
 * */
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg)) return unescape(arr[2]);
    else return null;
}

/*
 * 截取url 参数
 * @parm key 参数名称
 *
 * */

function getUrlParam(key) {
    var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)");
    var result = window.location.search.substr(1).match(reg);
    return result ? decodeURIComponent(result[2]) : null;
};

//异地登录
function other_login() {
    removeCookie("token");
    removeCookie("userNo");
    try {
        exit.otherlogin();
    } catch (e) {
    }
    try {
        otherlogin();
    } catch (e) {
    }
    if (getCookie("app") == null) {
        var referer_url = window.location.href;
        if (referer_url.indexOf("?token") != -1 && referer_url.indexOf("&") != -1) {
            referer_url = referer_url.replace(/token=.*?[0-9a-z]{1,}&/g, '')
        } else if (referer_url.indexOf("?token") != -1) {
            referer_url = referer_url.replace(/\?token=.*?[0-9a-z]{1,}/g, '');
        }
        setCookie("referer_url", referer_url);
        window.location.href = "/static/html/main/login.html"
    }
}

/*
 *子页面 退出
 * */
function mBack() {
    if (getUrlParam("isquit") == 1) {
        back();
    } else {
        window.history.back();
    }
}

/*
  退出 app
 * */
function back() {
    try {
        exit.exit();
    } catch (e) {
    }

    try {
        exit();
    } catch (e) {
    }
    if (getCookie("app") == null) {
        if (getToken() == null) return;
        window.location.href = "/static/html/main/mycollege/index.html?token=" + getToken();
    }
}

/*
 *生成唯一标识
 * */
function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/*
 * $http angularjs 请求对象
 *
 * 封装请求 框架  get
 * success 成功的回调
 * fail 失败的回调
 * statusCode 200
 * */

function _get($http, url, success, fail) {
    try {
        $.showIndicator();
    } catch (e) {
    }
    $http({
        method: "get",
        url: url,
        timeout: 30000,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        try {
            $.hideIndicator();
        } catch (e) {
        }
        if (data.state == 200) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            fail(data);
            $.toast(data.message);
        }
    }).error(function (data, status) {
        $.hideIndicator();
        if (status == -1) $.toast("请求超时");
        fail(data);
    });

}

/*
 * $http angularjs 请求对象
 *
 * 封装请求 框架  post
 * success 成功的回调
 * fail 失败的回调
 * statusCode 200
 * */

function _post($http, url, data, success, fail) {
    $.showIndicator();
    $http({
        method: "post",
        url: url,
        timeout: 30000,
        data: data,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        $.hideIndicator();
        if (data.state == 200) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            fail(data);
            $.toast(data.message);
        }
    }).error(function (data, status) {
        $.hideIndicator();
        if (status == -1) $.toast("请求超时");
        fail(data);
    });

}

/*
 * $http angularjs 请求对象
 *
 * 封装请求 框架  post
 * success 成功的回调
 * fail 失败的回调
 * statusCode 200
 * */

function _put($http, url, data, success, fail) {
    $.showIndicator();
    $http({
        method: "PUT",
        url: url,
        timeout: 30000,
        data: data,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        $.hideIndicator();
        if (data.state == 200) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            fail(data);
            $.toast(data.message);
        }
    }).error(function (data, status) {
        $.hideIndicator();
        if (status == -1) $.toast("请求超时");
        fail(data);
    });

}

/*
 * $http angularjs 请求对象
 *
 * 封装请求 框架  patch
 * success 成功的回调
 * fail 失败的回调
 * statusCode 200
 * */

function _patch($http, url, data, success, fail) {
    $.showIndicator();
    $http({
        method: "patch",
        url: url,
        timeout: 30000,
        data: data,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        $.hideIndicator();
        if (data.state == 200) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            fail(data);
            $.toast(data.message);
        }
    }).error(function (data, status) {
        $.hideIndicator();
        if (status == -1) $.toast("请求超时");
        fail(data);
    });

}

/*
 * $http angularjs 请求对象
 *
 * 封装请求 框架  delete
 * success 成功的回调
 * fail 失败的回调
 * statusCode 200
 * */

function _delete($http, url, success, fail) {
    $.showIndicator();
    $http({
        method: "delete",
        url: url,
        timeout: 30000,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        $.hideIndicator();
        if (data.state == 200) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            $.toast(data.message);
        }
    }).error(function (data, status) {
        $.hideIndicator();
        fail(data);
    });

}

/*
 * $http angularjs 请求对象
 *
 * url 评教URL请求框架
 * success 成功的回调
 * fail 失败的回调
 * statusCode 000000
 * */

function _get_pj($http, url, success, fail) {
    $.showIndicator();
    $http.get(url)
        .success(function (data) {
            $.hideIndicator();
            if (data.statusCode == 000000) {
                success(data);
            } else if (data.state == 2003) {
                other_login();
            } else {
                $.toast(data.message);
            }
        }).error(function (data) {
        $.hideIndicator();
        fail(data);
    });
}

/*
 * $http angularjs 请求对象
 *
 * url 评教URL请求框架 post
 * success 成功的回调
 * fail 失败的回调
 * statusCode 000000
 * */
function _post_pj($http, url, data, success, fail) {
    $.showIndicator();
    console.log(JSON.stringify(data));
    $http({
        method: "post",
        url: url,
        data: data,
        headers: {
            "Content-Type": "application/json"
        }
    }).success(function (data) {
        $.hideIndicator();
        //		console.log("_get," + url)
        //		console.log("_get," + JSON.stringify(data))
        if (data.statusCode == 000000) {
            success(data);
        } else if (data.state == 2003) {
            other_login();
        } else {
            $.toast(data.message);
        }
    }).error(function (data) {
        //		console.log(JSON.stringify(data));
        $.hideIndicator();
        fail(data);
    });
}

/*获取设备*/
function getDevices() {
    if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
        return "ios";
    } else if (/(Android)/i.test(navigator.userAgent)) {
        return "android";
    } else {
        return "web";
    }
    ;
}

/*
 * Base64
 * 加密  encode
 * 解密  decode
 * */

(function (global) {
    var global = global || {};
    var _Base64 = global.Base64;
    var version = "2.1.9";
    var buffer;
    var b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var b64tab = function (bin) {
        var t = {};
        for (var i = 0, l = bin.length; i < l; i++) {
            t[bin.charAt(i)] = i
        }
        return t
    }(b64chars);
    var fromCharCode = String.fromCharCode;
    var cb_utob = function (c) {
        if (c.length < 2) {
            var cc = c.charCodeAt(0);
            return cc < 128 ? c : cc < 2048 ? (fromCharCode(192 | (cc >>> 6)) + fromCharCode(128 | (cc & 63))) : (fromCharCode(224 | ((cc >>> 12) & 15)) + fromCharCode(128 | ((cc >>> 6) & 63)) + fromCharCode(128 | (cc & 63)))
        } else {
            var cc = 65536 + (c.charCodeAt(0) - 55296) * 1024 + (c.charCodeAt(1) - 56320);
            return (fromCharCode(240 | ((cc >>> 18) & 7)) + fromCharCode(128 | ((cc >>> 12) & 63)) + fromCharCode(128 | ((cc >>> 6) & 63)) + fromCharCode(128 | (cc & 63)))
        }
    };
    var re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
    var utob = function (u) {
        return u.replace(re_utob, cb_utob)
    };
    var cb_encode = function (ccc) {
        var padlen = [0, 2, 1][ccc.length % 3],
            ord = ccc.charCodeAt(0) << 16 | ((ccc.length > 1 ? ccc.charCodeAt(1) : 0) << 8) | ((ccc.length > 2 ? ccc.charCodeAt(2) : 0)),
            chars = [b64chars.charAt(ord >>> 18), b64chars.charAt((ord >>> 12) & 63), padlen >= 2 ? "=" : b64chars.charAt((ord >>> 6) & 63), padlen >= 1 ? "=" : b64chars.charAt(ord & 63)];
        return chars.join("")
    };
    var btoa = global.btoa ? function (b) {
        return global.btoa(b)
    } : function (b) {
        return b.replace(/[\s\S]{1,3}/g, cb_encode)
    };
    var _encode = buffer ? function (u) {
        return (u.constructor === buffer.constructor ? u : new buffer(u)).toString("base64")
    } : function (u) {
        return btoa(utob(u))
    };
    var encode = function (u, urisafe) {
        return !urisafe ? _encode(String(u)) : _encode(String(u)).replace(/[+\/]/g, function (m0) {
            return m0 == "+" ? "-" : "_"
        }).replace(/=/g, "")
    };
    var encodeURI = function (u) {
        return encode(u, true)
    };
    var re_btou = new RegExp(["[\xC0-\xDF][\x80-\xBF]", "[\xE0-\xEF][\x80-\xBF]{2}", "[\xF0-\xF7][\x80-\xBF]{3}"].join("|"), "g");
    var cb_btou = function (cccc) {
        switch (cccc.length) {
            case 4:
                var cp = ((7 & cccc.charCodeAt(0)) << 18) | ((63 & cccc.charCodeAt(1)) << 12) | ((63 & cccc.charCodeAt(2)) << 6) | (63 & cccc.charCodeAt(3)),
                    offset = cp - 65536;
                return (fromCharCode((offset >>> 10) + 55296) + fromCharCode((offset & 1023) + 56320));
            case 3:
                return fromCharCode(((15 & cccc.charCodeAt(0)) << 12) | ((63 & cccc.charCodeAt(1)) << 6) | (63 & cccc.charCodeAt(2)));
            default:
                return fromCharCode(((31 & cccc.charCodeAt(0)) << 6) | (63 & cccc.charCodeAt(1)))
        }
    };
    var btou = function (b) {
        return b.replace(re_btou, cb_btou)
    };
    var cb_decode = function (cccc) {
        var len = cccc.length,
            padlen = len % 4,
            n = (len > 0 ? b64tab[cccc.charAt(0)] << 18 : 0) | (len > 1 ? b64tab[cccc.charAt(1)] << 12 : 0) | (len > 2 ? b64tab[cccc.charAt(2)] << 6 : 0) | (len > 3 ? b64tab[cccc.charAt(3)] : 0),
            chars = [fromCharCode(n >>> 16), fromCharCode((n >>> 8) & 255), fromCharCode(n & 255)];
        chars.length -= [0, 0, 2, 1][padlen];
        return chars.join("")
    };
    var atob = global.atob ? function (a) {
        return global.atob(a)
    } : function (a) {
        return a.replace(/[\s\S]{1,4}/g, cb_decode)
    };
    var _decode = buffer ? function (a) {
        return (a.constructor === buffer.constructor ? a : new buffer(a, "base64")).toString()
    } : function (a) {
        return btou(atob(a))
    };
    var decode = function (a) {
        return _decode(String(a).replace(/[-_]/g, function (m0) {
            return m0 == "-" ? "+" : "/"
        }).replace(/[^A-Za-z0-9\+\/]/g, ""))
    };
    var noConflict = function () {
        var Base64 = global.Base64;
        global.Base64 = _Base64;
        return Base64
    };
    global.Base64 = {
        VERSION: version,
        atob: atob,
        btoa: btoa,
        fromBase64: decode,
        toBase64: encode,
        utob: utob,
        encode: encode,
        encodeURI: encodeURI,
        btou: btou,
        decode: decode,
        noConflict: noConflict
    };
    if (typeof Object.defineProperty === "function") {
        var noEnum = function (v) {
            return {
                value: v,
                enumerable: false,
                writable: true,
                configurable: true
            }
        };
        global.Base64.extendString = function () {
            Object.defineProperty(String.prototype, "fromBase64", noEnum(function () {
                return decode(this)
            }));
            Object.defineProperty(String.prototype, "toBase64", noEnum(function (urisafe) {
                return encode(this, urisafe)
            }));
            Object.defineProperty(String.prototype, "toBase64URI", noEnum(function () {
                return encode(this, true)
            }))
        }
    }
})(this);