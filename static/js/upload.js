// EduGenie – Upload JS
// Handles drag & drop and file selection

(function () {
  var dropZone     = document.getElementById('dropZone');
  var fileInput    = document.getElementById('pdf_file');
  var dropContent  = document.getElementById('dropContent');
  var fileSelected = document.getElementById('fileSelected');
  var selectedName = document.getElementById('selectedFileName');
  var uploadBtn    = document.getElementById('uploadBtn');

  if (!dropZone || !fileInput) return;

  // ── Click anywhere on drop zone to open file picker ──
  dropZone.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    fileInput.click();
  });

  // ── File selected via file picker ──
  fileInput.addEventListener('change', function () {
    if (fileInput.files && fileInput.files.length > 0) {
      showFile(fileInput.files[0]);
    }
  });

  // ── Drag over ──
  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
  });

  // ── Drag leave ──
  dropZone.addEventListener('dragleave', function (e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
  });

  // ── Drop file ──
  dropZone.addEventListener('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');

    var files = e.dataTransfer.files;
    if (files && files.length > 0) {
      if (files[0].name.toLowerCase().endsWith('.pdf')) {
        try {
          var dataTransfer = new DataTransfer();
          dataTransfer.items.add(files[0]);
          fileInput.files = dataTransfer.files;
        } catch (err) {
          console.log('DataTransfer not supported, using fallback');
        }
        showFile(files[0]);
      } else {
        alert('Please upload a PDF file only.');
      }
    }
  });

  // ── Show selected file name ──
  function showFile(file) {
    // Hide drop content
    if (dropContent)  dropContent.style.display  = 'none';
    // Show file selected
    if (fileSelected) fileSelected.style.display = 'flex';
    // Set file name
    if (selectedName) selectedName.textContent = file.name + ' (' + formatSize(file.size) + ')';
    // Enable upload button
    if (uploadBtn) {
      uploadBtn.disabled    = false;
      uploadBtn.textContent = '⚡ Process PDF with AI';
      uploadBtn.style.opacity = '1';
      uploadBtn.style.cursor  = 'pointer';
    }
  }

  // ── Format file size ──
  function formatSize(bytes) {
    if (bytes < 1024)     return bytes + ' B';
    if (bytes < 1048576)  return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

})();
