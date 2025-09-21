// Upload page functions
function goBack() {
    window.location.href = './index.html';
}

// Sample data for different regions
const sampleData = {
    telangana: {
        claim_id: "IFR001-TG",
        name: "Ramesh Kumar",
        village: "Kothapalli",
        district: "Adilabad", 
        state: "Telangana",
        tribe_status: "Scheduled Tribe",
        tribe_name: "Gond",
        claim_type: "Individual Forest Rights (IFR)",
        area_claimed: "2.5 hectares",
        survey_number: "124/2A",
        status: "Approved",
        approval_date: "2024-03-15",
        patta_number: "FRA/AD/2024/001",
        geometry: {
            type: "Polygon",
            coordinates: [[[78.5234, 19.1456], [78.5267, 19.1456], [78.5267, 19.1489], [78.5234, 19.1489], [78.5234, 19.1456]]]
        }
    },
    odisha: {
        claim_id: "CFR002-OD", 
        name: "Santosh Majhi",
        village: "Bandhagaon",
        district: "Mayurbhanj",
        state: "Odisha",
        tribe_status: "Scheduled Tribe",
        tribe_name: "Santhal",
        claim_type: "Community Forest Resource Rights (CFR)",
        area_claimed: "15.8 hectares",
        survey_number: "89/1B",
        status: "Under Verification",
        approval_date: null,
        patta_number: null,
        geometry: {
            type: "Polygon", 
            coordinates: [[[86.2134, 21.9567], [86.2189, 21.9567], [86.2189, 21.9634], [86.2134, 21.9634], [86.2134, 21.9567]]]
        }
    },
    madhyaPradesh: {
        claim_id: "IFR003-MP",
        name: "Lakshmi Bai Bhilala", 
        village: "Jhiranya",
        district: "Jhabua",
        state: "Madhya Pradesh",
        tribe_status: "Scheduled Tribe",
        tribe_name: "Bhil",
        claim_type: "Individual Forest Rights (IFR)",
        area_claimed: "1.8 hectares",
        survey_number: "67/3A",
        status: "Approved",
        approval_date: "2024-01-28",
        patta_number: "FRA/JH/2024/045",
        geometry: {
            type: "Polygon",
            coordinates: [[[74.5923, 22.7689], [74.5945, 22.7689], [74.5945, 22.7712], [74.5923, 22.7712], [74.5923, 22.7689]]]
        }
    },
    tripura: {
        claim_id: "CR004-TR",
        name: "Bijoy Reang",
        village: "Gandacherra", 
        district: "Dhalai",
        state: "Tripura",
        tribe_status: "Scheduled Tribe",
        tribe_name: "Reang",
        claim_type: "Community Rights (CR)",
        area_claimed: "8.2 hectares",
        survey_number: "156/4B",
        status: "Approved",
        approval_date: "2024-02-10",
        patta_number: "FRA/DH/2024/012",
        geometry: {
            type: "Polygon",
            coordinates: [[[91.4567, 23.8234], [91.4601, 23.8234], [91.4601, 23.8267], [91.4567, 23.8267], [91.4567, 23.8234]]]
        }
    }
};

// File upload functionality
function initFileUploads() {
    const pdfUpload = document.getElementById('pdfUpload');
    const shapeUpload = document.getElementById('shapeUpload');
    const pdfFile = document.getElementById('pdfFile');
    const shapeFile = document.getElementById('shapeFile');

    // PDF Upload
    pdfUpload.addEventListener('click', () => pdfFile.click());
    pdfUpload.addEventListener('dragover', handleDragOver);
    pdfUpload.addEventListener('dragleave', handleDragLeave);
    pdfUpload.addEventListener('drop', (e) => handleDrop(e, 'pdf'));
    pdfFile.addEventListener('change', (e) => handleFileSelect(e, 'pdf'));

    // Shapefile Upload  
    shapeUpload.addEventListener('click', () => shapeFile.click());
    shapeUpload.addEventListener('dragover', handleDragOver);
    shapeUpload.addEventListener('dragleave', handleDragLeave);
    shapeUpload.addEventListener('drop', (e) => handleDrop(e, 'shape'));
    shapeFile.addEventListener('change', (e) => handleFileSelect(e, 'shape'));
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e, type) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        displayFileInfo(files[0], type);
    }
}

function handleFileSelect(e, type) {
    const file = e.target.files[0];
    if (file) {
        displayFileInfo(file, type);
    }
}

function displayFileInfo(file, type) {
    const infoElement = document.getElementById(type === 'pdf' ? 'pdfInfo' : 'shapeInfo');
    const uploadArea = document.getElementById(type === 'pdf' ? 'pdfUpload' : 'shapeUpload');
    
    // Validate file type
    let isValidFile = false;
    if (type === 'pdf' && file.type === 'application/pdf') {
        isValidFile = true;
    } else if (type === 'shape' && (file.name.endsWith('.shp') || file.name.endsWith('.zip') || file.type === 'application/zip')) {
        isValidFile = true;
    }
    
    if (!isValidFile) {
        alert(`Please select a valid ${type === 'pdf' ? 'PDF' : 'shapefile (.shp or .zip)'} file.`);
        return;
    }
    
    const maxSize = type === 'pdf' ? 10 * 1024 * 1024 : 20 * 1024 * 1024; // 10MB for PDF, 20MB for shapefiles
    if (file.size > maxSize) {
        alert(`File size too large. Maximum allowed: ${type === 'pdf' ? '10MB' : '20MB'}`);
        return;
    }
    
    infoElement.innerHTML = `
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">${type === 'pdf' ? '📄' : '🗺️'}</span>
            <div>
                <strong>${file.name}</strong><br>
                <small>Size: ${(file.size / 1024 / 1024).toFixed(2)} MB</small><br>
                <small style="color: var(--forest-accent);">✓ Ready for processing</small>
            </div>
        </div>
    `;
    infoElement.style.display = 'block';
    uploadArea.style.border = '3px solid var(--forest-accent)';
    uploadArea.style.background = 'rgba(125, 180, 108, 0.15)';
    
    checkProcessButton();
}

function checkProcessButton() {
    const pdfInfo = document.getElementById('pdfInfo');
    const shapeInfo = document.getElementById('shapeInfo');
    const processBtn = document.getElementById('processBtn');
    
    if (pdfInfo.style.display !== 'none' && shapeInfo.style.display !== 'none') {
        processBtn.disabled = false;
        processBtn.innerHTML = '<span class="btn-icon">🚀</span> Process Documents with AI';
        processBtn.style.opacity = '1';
        processBtn.style.cursor = 'pointer';
    }
}

function processFiles() {
    const processBtn = document.getElementById('processBtn');
    const resultsSection = document.getElementById('resultsSection');
    
    // Show processing state
    processBtn.classList.add('processing');
    processBtn.disabled = true;
    processBtn.innerHTML = '<span class="btn-icon">🔄</span> Processing with AI...';
    
    // Add visual processing feedback
    const processingSteps = [
        'Reading PDF document...',
        'Applying OCR technology...',
        'Extracting text with NER...',
        'Processing shapefile coordinates...',
        'Validating spatial data...',
        'Generating results...'
    ];
    
    let stepIndex = 0;
    const stepInterval = setInterval(() => {
        if (stepIndex < processingSteps.length) {
            processBtn.innerHTML = `<span class="btn-icon">🔄</span> ${processingSteps[stepIndex]}`;
            stepIndex++;
        }
    }, 500);
    
    // Simulate processing time
    setTimeout(() => {
        clearInterval(stepInterval);
        
        // Randomly select sample data from one of the states
        const states = ['telangana', 'odisha', 'madhyaPradesh', 'tripura'];
        const randomState = states[Math.floor(Math.random() * states.length)];
        const selectedData = sampleData[randomState];
        
        // Display extracted data
        document.getElementById('extractedData').textContent = JSON.stringify(selectedData, null, 2);
        
        // Display coordinate information
        const coords = selectedData.geometry.coordinates[0];
        document.getElementById('coordinateDisplay').innerHTML = `
            <strong>Boundary Coordinates:</strong><br>
            Latitude: ${coords[0][1].toFixed(4)}°N to ${coords[2][1].toFixed(4)}°N<br>
            Longitude: ${coords[0][0].toFixed(4)}°E to ${coords[2][0].toFixed(4)}°E<br>
            <strong>Area:</strong> ${selectedData.area_claimed}<br>
            <strong>Survey No:</strong> ${selectedData.survey_number}
        `;
        
        // Update mini map with polygon and location info
        const miniMap = document.getElementById('miniMap');
        miniMap.innerHTML = `
            <div style="position: relative; width: 100%; height: 100%;">
                <!-- Terrain background -->
                <div style="position: absolute; inset: 0; background: linear-gradient(135deg, #87CEEB 0%, #98FB98 50%, #90EE90 100%);"></div>
                
                <!-- Forest areas -->
                <div style="position: absolute; top: 10%; left: 10%; width: 25%; height: 25%; 
                           background: #228B22; border-radius: 50%; opacity: 0.7;"></div>
                <div style="position: absolute; top: 20%; right: 15%; width: 20%; height: 20%; 
                           background: #006400; border-radius: 30%; opacity: 0.7;"></div>
                
                <!-- Claim boundary (main polygon) -->
                <div style="position: absolute; top: 30%; left: 25%; width: 45%; height: 40%; 
                           border: 3px solid var(--forest-primary); background: rgba(125, 180, 108, 0.4);
                           border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);"></div>
                
                <!-- Village marker -->
                <div style="position: absolute; top: 45%; left: 42%; width: 12px; height: 12px;
                           background: #FF4500; border: 2px solid white; border-radius: 50%;
                           box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                
                <!-- Location label -->
                <div style="position: absolute; bottom: 8px; right: 8px; 
                           background: rgba(255,255,255,0.9); padding: 0.25rem 0.5rem; border-radius: 4px;
                           font-size: 0.7rem; color: var(--forest-primary); font-weight: 500;
                           box-shadow: 0 1px 3px rgba(0,0,0,0.2);">
                    📍 ${selectedData.village}, ${selectedData.state}
                </div>
                
                <!-- Coordinates overlay -->
                <div style="position: absolute; top: 8px; left: 8px; 
                           background: rgba(26, 77, 58, 0.8); color: white; padding: 0.25rem 0.5rem; 
                           border-radius: 4px; font-size: 0.6rem; font-family: monospace;">
                    ${coords[0][1].toFixed(3)}°N, ${coords[0][0].toFixed(3)}°E
                </div>
            </div>
        `;
        
        // Show results with animation
        resultsSection.style.display = 'block';
        setTimeout(() => {
            resultsSection.style.opacity = '0';
            resultsSection.style.transform = 'translateY(20px)';
            resultsSection.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                resultsSection.style.opacity = '1';
                resultsSection.style.transform = 'translateY(0)';
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }, 100);
        
        // Reset button with success state
        processBtn.classList.remove('processing');
        processBtn.innerHTML = '<span class="btn-icon">✅</span> Processing Complete!';
        processBtn.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
    }, 3500); // Extended time to show all processing steps
}

function resetUpload() {
    // Reset file inputs
    document.getElementById('pdfFile').value = '';
    document.getElementById('shapeFile').value = '';
    
    // Reset file info displays
    const pdfInfo = document.getElementById('pdfInfo');
    const shapeInfo = document.getElementById('shapeInfo');
    pdfInfo.style.display = 'none';
    shapeInfo.style.display = 'none';
    
    // Reset upload areas
    const uploads = ['pdfUpload', 'shapeUpload'];
    uploads.forEach(id => {
        const element = document.getElementById(id);
        element.style.border = '3px dashed var(--forest-light)';
        element.style.background = 'rgba(245, 245, 220, 0.3)';
    });
    
    // Reset process button
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = true;
    processBtn.classList.remove('processing');
    processBtn.innerHTML = '<span class="btn-icon">🔄</span> Process Documents with AI';
    processBtn.style.opacity = '0.5';
    processBtn.style.cursor = 'not-allowed';
    processBtn.style.background = 'var(--gradient-forest)';
    
    // Hide results with animation
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.opacity = '0';
    resultsSection.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
        resultsSection.style.display = 'none';
        resultsSection.style.opacity = '1';
        resultsSection.style.transform = 'translateY(0)';
        
        // Scroll back to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 300);
}

function saveToAtlas() {
    // Simulate saving to atlas
    const btn = event.target;
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '💾 Saving to Atlas...';
    btn.disabled = true;
    btn.style.background = 'var(--forest-secondary)';
    
    // Show progress simulation
    const progressSteps = [
        '💾 Validating data...',
        '🗂️ Creating atlas entry...',
        '📊 Updating spatial index...',
        '🔗 Linking to DSS...',
        '✅ Saved successfully!'
    ];
    
    let stepIndex = 0;
    const stepInterval = setInterval(() => {
        if (stepIndex < progressSteps.length) {
            btn.innerHTML = progressSteps[stepIndex];
            stepIndex++;
        }
    }, 600);
    
    setTimeout(() => {
        clearInterval(stepInterval);
        btn.innerHTML = '✅ Saved to Atlas!';
        btn.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
        
        setTimeout(() => {
            // Success message with detailed info
            const selectedData = JSON.parse(document.getElementById('extractedData').textContent);
            alert(`🎉 Success! FRA Claim Processed Successfully\n\n` +
                  `📋 Claim Details:\n` +
                  `• ID: ${selectedData.claim_id}\n` +
                  `• Holder: ${selectedData.name}\n` +
                  `• Location: ${selectedData.village}, ${selectedData.district}, ${selectedData.state}\n` +
                  `• Type: ${selectedData.claim_type}\n` +
                  `• Area: ${selectedData.area_claimed}\n` +
                  `• Status: ${selectedData.status}\n\n` +
                  `🔧 AI Processing Completed:\n` +
                  `✓ OCR text extraction\n` +
                  `✓ NER data classification\n` +
                  `✓ Spatial coordinate validation\n` +
                  `✓ Atlas integration\n` +
                  `✓ DSS eligibility analysis\n\n` +
                  `🗺️ Data is now available in the WebGIS portal and ready for scheme mapping!`);
            
            // Auto-reset after success
            setTimeout(() => {
                resetUpload();
            }, 2000);
        }, 1000);
    }, 3000);
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function validateCoordinates(coords) {
    // Basic coordinate validation for Indian boundaries
    const [lon, lat] = coords;
    return (lat >= 6 && lat <= 38 && lon >= 68 && lon <= 98);
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Upload page error:', e.error);
    alert('An error occurred. Please refresh the page and try again.');
});

// Prevent default drag behaviors on the entire page
document.addEventListener('dragover', function(e) {
    e.preventDefault();
});

document.addEventListener('drop', function(e) {
    e.preventDefault();
});

// Initialize upload functionality when page loads
document.addEventListener('DOMContentLoaded', function() {
    initFileUploads();
    
    // Add some loading animation for page entrance
    const uploadPage = document.getElementById('uploadPage');
    uploadPage.style.opacity = '0';
    uploadPage.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        uploadPage.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        uploadPage.style.opacity = '1';
        uploadPage.style.transform = 'translateY(0)';
    }, 100);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Escape key to go back
        if (e.key === 'Escape') {
            goBack();
        }
        
        // Enter key to process files if ready
        if (e.key === 'Enter' && !document.getElementById('processBtn').disabled) {
            processFiles();
        }
    });
});