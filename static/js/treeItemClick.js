/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *   File:   Treeitem.js
 *
 *   Desc:   Setup click events for Tree widget examples
 */

'use strict';


/**
 * ARIA Treeview example
 *
 * @function onload
 * @description  after page has loaded initialize all treeitems based on the role=treeitem
 */
window.addEventListener('load', function () {
  var treeitems = document.querySelectorAll('[role="treeitem"]');

  for (var i = 0; i < treeitems.length; i++) {
    treeitems[i].addEventListener('click', function (event) {
      var treeitem = event.currentTarget;
      var label = treeitem.getAttribute('aria-label');
      if (!label) {
        var child = treeitem.firstElementChild;
        label = child ? child.innerText : treeitem.innerText;
      }
      var type = treeitem.getAttribute('type');
      // Retrieve all parent nodes
      var parents = getAllParents(treeitem);

      var xhr = new XMLHttpRequest();

      xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
          var parsedResponse = JSON.parse(xhr.responseText);
          var changeStatus = parsedResponse["change"];
          var contentResponse = parsedResponse["content"];
          if (changeStatus) {
            const codeOutput = document.getElementById('current-content-unique');
            codeOutput.querySelector('code').textContent = contentResponse;
            Prism.highlightAll();
          }
        }
      }
      xhr.open("POST", "/process_data", true);
      xhr.setRequestHeader("Content-Type", "application/json");
      var data = JSON.stringify({ "parents": parents, "label": label, "type": type });
      xhr.send(data);

      event.stopPropagation();
      event.preventDefault();
    });
  }

  function getAllParents(element) {
    var parents = [];
    var currentElement = element.parentElement;

    while (currentElement) {
      if (currentElement.getAttribute('role') === 'treeitem') {
        var parentLabel = currentElement.getAttribute('aria-label');
        if (!parentLabel) {
          var parentChild = currentElement.firstElementChild;
          parentLabel = parentChild ? parentChild.innerText : currentElement.innerText;
        }
        parents.unshift(parentLabel);
      }
      currentElement = currentElement.parentElement;
    }

    return parents;
  }
});