/* utilities to work with HTTP request 
    v0.4
*/

function addEvent(elm, evType, fn, useCapture) {
// addEvent and removeEvent
// cross-browser event handling for IE5+,  NS6 and Mozilla
// By Scott Andrew
    if (elm.addEventListener) {
        elm.addEventListener(evType, fn, useCapture);
        return true;
    } else if (elm.attachEvent) {
        var r = elm.attachEvent("on"+evType, fn);
        return r;
    }
}

function queryFromForm(form) {
    /* build a query string of all elements in given form */
    var data = '';
    var element;
    var lastelementname = '';
    for (var i = form.elements.length-1; i > -1 ; i--) {
        element = form.elements[i];
        switch (element.type) {
            // Text fields, hidden form elements
            case 'text':
            case 'hidden':
            case 'password':
            case 'textarea':
            case 'select-one':
                data += element.name + '=' + encodeURIComponent(element.value) + '&'
                break;
            // Radio
            case 'radio':
                if (element.checked) {
                    data += element.name + '=' + encodeURIComponent(element.value) + '&'
                }
                break;
            // Checkboxes
            case 'checkbox':
                if (element.checked) {
                    // continuing multiple, same-name checkboxes
                    if (element.name == lastelementname) {
                        // strip of end ampersand if there is one
                        if (data.lastIndexOf('&') == data.length-1) {
                            data = data.substr(0, data.length - 1);
                        }
                        // append value as comma-delimited string
                        data += ',' + encodeURIComponent(element.value);
                    }
                    else {
                        data += element.name + '=' + encodeURIComponent(element.value);
                    }
                    data += '&';
                    lastelementname = element.name;
                }
                break;
        }
    }
    // remove trailing ampersand
    data = data.substr(0, data.length - 1);
    return data;
}    


function xmlhttpPost(url, data, callback) {
    /* POST an XMLHttpRequest, return response object */
    var xmlHttpReq = false;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
            xmlHttpReq = new XMLHttpRequest();
            //breaks Opera:
            //xmlHttpReq.overrideMimeType('text/xml');
    }
    // IE
    else if (window.ActiveXObject) {
            xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    } 
    xmlHttpReq.open('POST', url, true);
    xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlHttpReq.onreadystatechange = function() {
        if (xmlHttpReq.readyState == 4) {
            switch (xmlHttpReq.status) {
                case 200:
                    callback(xmlHttpReq)
                    break
                case 404:
                    alert('Error: Not Found.  ' + url)
                    break;
                default:
                    document.body.innerHTML = xmlHttpReq.responseText;
                    break;
            }
        }
    }
    xmlHttpReq.send(data);
}
