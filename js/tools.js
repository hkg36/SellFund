if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            var type=typeof args[number];
            if(type!='undefined')
                return args[number]
            else
                return ""
        });
    };
}
String.prototype.formatO=function(obj){
    return this.replace(/{(\w+)}/g, function(match, name) {
        var type=typeof obj[name];
        if(type!='undefined')
            return obj[name];
        else
            return ""
    });
}

if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (obj, fromIndex) {
        if (fromIndex == null) {
            fromIndex = 0;
        } else if (fromIndex < 0) {
            fromIndex = Math.max(0, this.length + fromIndex);
        }
        for (var i = fromIndex, j = this.length; i < j; i++) {
            if (this[i] === obj)
                return i;
        }
        return -1;
    };
}
