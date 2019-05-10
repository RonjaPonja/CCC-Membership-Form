/*
 * Synchronize form fields in screenParentId whose "name" attribute starts with
 * screenPrefix to their counterparts in printParentId (same "name" attribute
 * minus screenPrefix).
 *
 * "select" elements are synchronized to "text" inputs in printParentId.
 */
function syncFormFields (screenParentId, printParentId, screenPrefix) {
    var screenParent = document.getElementById(screenParentId);
    var printParent = document.getElementById(printParentId);

    var inputs = screenParent.querySelectorAll(`input[name^=${screenPrefix}]`);
    inputs.forEach(function (source) {
        var name = source.getAttribute('name').substring(screenPrefix.length);
        var type = source.getAttribute('type');
        var value = source.getAttribute('value');
        var selector = `input[type=${type}][name=${name}]`;
        if (value !== null) {
            selector = `input[type=${type}][name=${name}][value=${value}]`;
        }
        syncElement(source, printParent, selector);
    });

    var selects = screenParent.querySelectorAll(`select[name^=${screenPrefix}]`);
    selects.forEach(function (source) {
        var name = source.getAttribute('name').substring(screenPrefix.length);
        var selector = `input[type=text][name=${name}]`;
        syncElement(source, printParent, selector);
    });

    var textareas = screenParent.querySelectorAll(`textarea[name^=${screenPrefix}]`);
    textareas.forEach(function (source) {
        var name = source.getAttribute('name').substring(screenPrefix.length);
        var selector = `textarea[name=${name}]`;
        syncElement(source, printParent, selector);
    });
}

/*
 * Synchronize the value or checked state of the source element to the
 * selector-chosen element in parent.
 */
function syncElement (source, parent, selector) {
    var target = parent.querySelector(selector);
    if (target !== null) {
        if (source.tagName === 'INPUT') {
            var type = source.getAttribute('type');
            switch (type) {
                case 'checkbox':
                    target.checked = source.checked;
                    break;
                case 'radio':
                    target.checked = source.checked;
                    break;
                default:
                    target.value = source.value;
                    break;
            }
        } else {
           target.value = source.value;
        }
    } else {
        console.warn(`No match for selector "${selector}"`);
    }
}
