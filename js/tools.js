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
