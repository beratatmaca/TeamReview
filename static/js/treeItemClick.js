/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *   File:   Treeitem.js
 *
 *   Desc:   Setup click events for Tree widget examples
 */

'use strict';

function updateClassBasedOnExtension(fileExtension) {
  // Map file extensions to Prism language classes
  var extensionToLanguage = {
    '.js': 'language-javascript',
    '.html': 'language-html',
    '.css': 'language-css',
    '.java': 'language-java',
    '.py': 'language-python',
    '.php': 'language-php',
    '.ruby': 'language-ruby',
    '.h': 'language-cpp',
    '.hpp': 'language-cpp',
    '.hxx': 'language-cpp',
    '.c': 'language-c',
    '.cpp': 'language-cpp',
    '.swift': 'language-swift',
    '.go': 'language-go',
    '.typescript': 'language-typescript',
    '.json': 'language-json',
    '.xml': 'language-xml',
    '.markdown': 'language-markdown',
    '.bash': 'language-bash',
    '.sql': 'language-sql',
    '.yaml': 'language-yaml',
    '.docker': 'language-docker',
    '.scss': 'language-scss',
    '.less': 'language-less',
    '.coffeescript': 'language-coffeescript',
    '.rust': 'language-rust',
    '.jsx': 'language-jsx',
    '.tsx': 'language-tsx',
    // Add more mappings as needed
  };

  // Convert the file extension to lowercase
  fileExtension = fileExtension.toLowerCase();

  // Return the class name based on the file extension
  return extensionToLanguage[fileExtension] || 'language-none';
}

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
      var root_folder = parents.join('/');
      if (type === 'file') {
        activeFile = root_folder.concat('/',label);
      }

      var xhr = new XMLHttpRequest();

      xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
          var parsedResponse = JSON.parse(xhr.responseText);
          var changeStatus = parsedResponse["change"];
          var contentResponse = parsedResponse["content"];
          var fileSuffix = parsedResponse["suffix"];
          var is_reviewed = parsedResponse["is_reviewed"];
          if (changeStatus) {
            const codeOutput = document.getElementById('current-content-unique');
            const codeElement = document.getElementById('code-content-unique');
            codeElement.className = updateClassBasedOnExtension(fileSuffix);
            
            codeOutput.querySelector('code').textContent = contentResponse;
            if(is_reviewed === "False" || is_reviewed === "false") {
              document.getElementById('mark-as-reviewed').checked = false;
            } else {
              document.getElementById('mark-as-reviewed').checked = true;
            }
            
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