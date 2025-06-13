// Licensed under a CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
// http://creativecommons.org/publicdomain/zero/1.0/
(function (win, doc) {
    'use strict';
    if (!win.XMLHttpRequest || !win.FormData || !win.addEventListener || !doc.querySelectorAll) {
        // doesn't cut the mustard.
        return;
    }
    function hijaxForm (formElement) {
        var progressBar;
        var xhr;
        function addProgressBar () {
            progressBar = doc.createElement('progress');
            progressBar.setAttribute('min', '0');
            progressBar.setAttribute('max', '100');
            progressBar.setAttribute('value', '0');
            formElement.appendChild(progressBar);
        }
        function updateProgressBar (ev) {
            if (ev.lengthComputable) {
                progressBar.value = (ev.loaded / ev.total) * 100;
            }
        }
        function ajax (elem) {
            addProgressBar();
            var method = elem.getAttribute('method');
            var url = elem.getAttribute('action');
            var data = new FormData(elem);
            xhr = new XMLHttpRequest();
            xhr.open(method, url, true);
            xhr.onload = function(ev) {
                win.location = url;
            };
            xhr.upload.onprogress = function (ev) {
                updateProgressBar(ev);
            };
            xhr.send(data);
        }
        formElement.addEventListener('submit', function (ev) {
            ajax(this);
            ev.preventDefault();
        }, false);
    }
    var formElements = doc.querySelectorAll('form[method="post"]');
    for (var i = 0; i < formElements.length; i = i + 1) {
        hijaxForm(formElements[i]);
    }
}(this, this.document));