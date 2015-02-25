function unsuan(s) {
    var hostname = "www.blgl8.com/"
    var sw = "jmmh.net/|jmymh.com/|blgl8.com/";
    var su = hostname.toLowerCase() + "/";
    b = false;
    for (i = 0; i < sw.split("|").length; i++) {
        if (su.indexOf(sw.split("|")[i]) > -1) {
            b = true;
            break
        }
    }
    if (!b) return "";
    var x = s.substring(s.length - 1);
    var xi = "abcdefghijklmnopqrstuvwxyz".indexOf(x) + 1;
    var sk = s.substring(s.length - xi - 12, s.length - xi - 1);
    s = s.substring(0, s.length - xi - 12);
    var k = sk.substring(0, sk.length - 1);
    var f = sk.substring(sk.length - 1);
    for (i = 0; i < k.length; i++) {
        eval("s=s.replace(/" + k.substring(i, i + 1) + "/g,'" + i + "')")
    }
    var ss = s.split(f);
    s = "";
    for (i = 0; i < ss.length; i++) {
        s += String.fromCharCode(ss[i])
    }
    return s
}

// process.argv.forEach(function (val, index, array) {
//    console.log(index + ': ' + val);
// });

console.log(unsuan(process.argv[2]));
