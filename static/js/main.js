// document.addEventListener('DOMContentLoaded', () => {
//     // Mobile navigation toggle
//     const menuToggle = document.getElementById('menuToggle');
//     const navMenu = document.getElementById('navMenu');

//     if (menuToggle && navMenu) {
//         menuToggle.addEventListener('click', () => {
//             navMenu.classList.toggle('active');
//             if (navMenu.classList.contains('active')) {
//                 menuToggle.innerHTML = '&times;';
//             } else {
//                 menuToggle.innerHTML = '&#9776;';
//             }
//         });

//         // Close menu on link click for mobile screens
//         navMenu.querySelectorAll('a').forEach(link => {
//             link.addEventListener('click', () => {
//                 navMenu.classList.remove('active');
//                 if (menuToggle) {
//                     menuToggle.innerHTML = '&#9776;';
//                 }
//             });
//         });
//     }

//     // Smooth scroll for internal anchor links
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener('click', function(e) {
//             const targetId = this.getAttribute('href');
//             if (targetId.length > 1) {
//                 const targetElement = document.querySelector(targetId);
//                 if (targetElement) {
//                     e.preventDefault();
//                     targetElement.scrollIntoView({
//                         behavior: 'smooth',
//                         block: 'start'
//                     });
//                 }
//             }
//         });
//     });
// });

// // --- ADDITIONAL JAVASCRIPT FOR NEW PAGES ---
// document.addEventListener('DOMContentLoaded', () => {
//     // 1. Password Visibility Toggle
//     const togglePasswordBtn = document.getElementById('togglePassword');
//     const passwordInput = document.getElementById('password');
//     if (togglePasswordBtn && passwordInput) {
//         togglePasswordBtn.addEventListener('click', () => {
//             const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
//             passwordInput.setAttribute('type', type);
//             togglePasswordBtn.innerHTML = type === 'password' ? '&#128065;' : '&#128276;';
//         });
//     }

//     // 2. Processes Page Search & Filtering
//     const processSearch = document.getElementById('processSearch');
//     const filterBtns = document.querySelectorAll('.filter-btn');
//     const processCards = document.querySelectorAll('.process-grid .process-card');

//     if (processSearch || filterBtns.length > 0) {
//         let currentFilter = 'all';
//         let searchQuery = '';

//         function filterProcesses() {
//             processCards.forEach(card => {
//                 const category = card.getAttribute('data-category');
//                 const name = card.getAttribute('data-name');
//                 const matchesCategory = currentFilter === 'all' || category === currentFilter;
//                 const matchesSearch = name.includes(searchQuery.toLowerCase());

//                 if (matchesCategory && matchesSearch) {
//                     card.style.display = 'flex';
//                 } else {
//                     card.style.display = 'none';
//                 }
//             });
//         }

//         if (processSearch) {
//             processSearch.addEventListener('input', (e) => {
//                 searchQuery = e.target.value.trim();
//                 filterProcesses();
//             });
//         }

//         filterBtns.forEach(btn => {
//             btn.addEventListener('click', () => {
//                 filterBtns.forEach(b => b.classList.remove('active'));
//                 btn.classList.add('active');
//                 currentFilter = btn.getAttribute('data-filter');
//                 filterProcesses();
//             });
//         });
//     }

//     // 3. Document Upload Drag & Drop & Preview
//     const dropZone = document.getElementById('dropZone');
//     const fileInput = document.getElementById('fileInput');
//     const dropContent = document.getElementById('dropContent');
//     const filePreview = document.getElementById('filePreview');
//     const fileNameDisplay = document.getElementById('fileNameDisplay');
//     const fileSizeDisplay = document.getElementById('fileSizeDisplay');
//     const removeFileBtn = document.getElementById('removeFileBtn');
//     const submitUploadBtn = document.getElementById('submitUploadBtn');

//     if (dropZone && fileInput) {
//         ['dragenter', 'dragover'].forEach(eventName => {
//             dropZone.addEventListener(eventName, (e) => {
//                 e.preventDefault();
//                 dropZone.classList.add('dragover');
//             }, false);
//         });

//         ['dragleave', 'drop'].forEach(eventName => {
//             dropZone.addEventListener(eventName, (e) => {
//                 e.preventDefault();
//                 dropZone.classList.remove('dragover');
//             }, false);
//         });

//         dropZone.addEventListener('drop', (e) => {
//             const files = e.dataTransfer.files;
//             if (files.length > 0) {
//                 fileInput.files = files;
//                 handleFileSelection(files[0]);
//             }
//         });

//         fileInput.addEventListener('change', (e) => {
//             if (fileInput.files.length > 0) {
//                 handleFileSelection(fileInput.files[0]);
//             }
//         });

//         function handleFileSelection(file) {
//             const validExtensions = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
//             if (!validExtensions.includes(file.type)) {
//                 alert('Please upload a valid PDF, JPG, or PNG file.');
//                 return;
//             }

//             if (file.size > 10 * 1024 * 1024) {
//                 alert('File size exceeds 10MB limit.');
//                 return;
//             }

//             fileNameDisplay.textContent = file.name;
//             const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
//             fileSizeDisplay.textContent = `${sizeMB} MB • Ready for verification`;

//             dropContent.style.display = 'none';
//             filePreview.style.display = 'flex';
//             if (submitUploadBtn) submitUploadBtn.removeAttribute('disabled');
//         }

//         if (removeFileBtn) {
//             removeFileBtn.addEventListener('click', () => {
//                 fileInput.value = '';
//                 dropContent.style.display = 'block';
//                 filePreview.style.display = 'none';
//                 if (submitUploadBtn) submitUploadBtn.setAttribute('disabled', 'true');
//             });
//         }
//     }
// });


document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile navigation toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.innerHTML = navMenu.classList.contains('active') ? '&times;' : '&#9776;';
        });

        // Close menu on link click for mobile screens
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                if (menuToggle) menuToggle.innerHTML = '&#9776;';
            });
        });
    }

    // 2. Smooth scroll for internal anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId.length > 1) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // 3. Password Visibility Toggle
    const togglePasswordBtn = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePasswordBtn.innerHTML = type === 'password' ? '&#128065;' : '&#128276;';
        });
    }

    // 4. Processes Page Search & Filtering
    const processSearch = document.getElementById('processSearch');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const processCards = document.querySelectorAll('.process-grid .process-card');

    if (processSearch || filterBtns.length > 0) {
        let currentFilter = 'all';
        let searchQuery = '';

        function filterProcesses() {
            processCards.forEach(card => {
                const category = card.getAttribute('data-category');
                const name = card.getAttribute('data-name');
                const matchesCategory = currentFilter === 'all' || category === currentFilter;
                const matchesSearch = name.includes(searchQuery.toLowerCase());

                card.style.display = (matchesCategory && matchesSearch) ? 'flex' : 'none';
            });
        }

        if (processSearch) {
            processSearch.addEventListener('input', (e) => {
                searchQuery = e.target.value.trim().toLowerCase();
                filterProcesses();
            });
        }

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter');
                filterProcesses();
            });
        });
    }

    // 5. Document Upload Drag & Drop & Preview (Only for upload.html)
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const dropContent = document.getElementById('dropContent');
    const filePreview = document.getElementById('filePreview');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const fileSizeDisplay = document.getElementById('fileSizeDisplay');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const submitUploadBtn = document.getElementById('submitUploadBtn');

    if (dropZone && fileInput) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelection(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                handleFileSelection(fileInput.files[0]);
            }
        });

        function handleFileSelection(file) {
            const validExtensions = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
            if (!validExtensions.includes(file.type)) {
                alert('Please upload a valid PDF, JPG, or PNG file.');
                return;
            }

            if (file.size > 10 * 1024 * 1024) {
                alert('File size exceeds 10MB limit.');
                return;
            }

            fileNameDisplay.textContent = file.name;
            const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
            fileSizeDisplay.textContent = `${sizeMB} MB • Ready for verification`;

            dropContent.style.display = 'none';
            filePreview.style.display = 'flex';
            if (submitUploadBtn) submitUploadBtn.removeAttribute('disabled');
        }

        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', () => {
                fileInput.value = '';
                dropContent.style.display = 'block';
                filePreview.style.display = 'none';
                if (submitUploadBtn) submitUploadBtn.setAttribute('disabled', 'true');
            });
        }
    }
});



async function uploadDocument(event, formElement) {
    event.preventDefault(); // Page reload hone se rokeyga
    
    const formData = new FormData(formElement);
    const submitBtn = formElement.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Uploading...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/upload_vault_doc', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Upload successful hone par button ka text badal dein ya success message dikhayein
            submitBtn.textContent = 'Uploaded Successfully! ✔';
            submitBtn.classList.remove('btn-primary');
            submitBtn.classList.add('btn-success');
            
            // Optional: Agar aap chahte hain ki upload hone ke baad wahan ek 'View' ya 'Uploaded' ka tag dikh jaye
        } else {
            alert('Upload failed. Please try again.');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

document.addEventListener("submit", async function(e) {
    // Check karo kya submit hone wala form apna .ajax-upload-form hai?
    if (!e.target.classList.contains('ajax-upload-form')) return;
    
    // Page reload rokne ke liye sabse pehle yeh
    e.preventDefault(); 
    
    const form = e.target;
    const fileField = form.querySelector('input[type="file"]');
    const statusSpan = form.querySelector('.upload-status');
    const submitBtn = form.querySelector('button[type="submit"]');
    const li = form.closest('li');

    if (fileField && !fileField.files.length) {
        alert('Please select a file first.');
        return;
    }

    if (submitBtn) submitBtn.disabled = true;
    if (statusSpan) {
        statusSpan.innerHTML = '⏳ Uploading...';
        statusSpan.style.color = '#6c757d';
    }

    const formData = new FormData(form);

    try {
        let response = await fetch('/upload_vault_doc', {
            method: 'POST',
            body: formData
        });

        let rawText = await response.text();
        let result;
        try {
            result = JSON.parse(rawText);
        } catch (jsonErr) {
            console.error("Non-JSON response from server:", rawText);
            throw new Error("Server did not return JSON");
        }

        console.log("Parsed Result:", result);

        if (response.ok && result.status === 'success') {
            if (statusSpan) {
                statusSpan.innerHTML = `✅ Done!`;
                statusSpan.style.color = '#198754';
            }

            // Target container dhoondo ya banao
            let targetArea = li ? li : form.parentElement;
            
            // Status badge update/inject
            let statusBadge = targetArea.querySelector('.doc-status-container');
            const badgeHtml = `<span style="background-color: #d1e7dd; color: #0f5132; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem; font-weight: bold;">✔ Uploaded</span>`;
            
            if (statusBadge) {
                statusBadge.innerHTML = badgeHtml;
            } else {
                form.insertAdjacentHTML('beforebegin', `<div class="doc-status-container" style="margin-bottom: 8px;">${badgeHtml}</div>`);
            }

            // Preview block update/inject
            let previewBlock = targetArea.querySelector('.file-preview-block');
            let fileName = (fileField && fileField.files[0]) ? fileField.files[0].name : (result.file_name || 'Uploaded File');
            let previewHtml = `
                <div style="background: #f8f9fa; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span>📄 Saved File: <strong>${fileName}</strong></span>
                    <span class="text-muted small">Just now</span>
                </div>
            `;

            if (previewBlock) {
                previewBlock.innerHTML = previewHtml;
            } else {
                form.insertAdjacentHTML('beforebegin', `<div class="file-preview-block">${previewHtml}</div>`);
            }

            if (submitBtn) submitBtn.innerHTML = 'Replace File';

        } else {
            if (statusSpan) {
                statusSpan.innerHTML = `❌ ${result.message || 'Failed'}`;
                statusSpan.style.color = 'red';
            }
        }
    } catch (err) {
        console.error("Upload error details:", err);
        if (statusSpan) {
            statusSpan.innerHTML = `❌ Error`;
            statusSpan.style.color = 'red';
        }
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
});