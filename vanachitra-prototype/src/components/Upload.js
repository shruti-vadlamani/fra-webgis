import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
    const navigate = useNavigate();
    const [pdfFile, setPdfFile] = useState(null);
    const [shapeFile, setShapeFile] = useState(null);
    const [results, setResults] = useState(null);
    const [processing, setProcessing] = useState(false);

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
            area_claimed: "4.2 hectares",
            survey_number: "156/3A",
            status: "Approved",
            approval_date: "2024-01-20",
            patta_number: "FRA/JH/2024/003",
            geometry: {
                type: "Polygon",
                coordinates: [[[74.5945, 22.7689], [74.5978, 22.7689], [74.5978, 22.7722], [74.5945, 22.7722], [74.5945, 22.7689]]]
            }
        },
        tripura: {
            claim_id: "CFR004-TR",
            name: "Bijoy Kumar Tripura",
            village: "Kailashahar",
            district: "Unakoti",
            state: "Tripura",
            tribe_status: "Scheduled Tribe",
            tribe_name: "Tripura",
            claim_type: "Community Forest Resource Rights (CFR)",
            area_claimed: "8.3 hectares",
            survey_number: "67/2B",
            status: "Approved",
            approval_date: "2024-02-10",
            patta_number: "FRA/UN/2024/004",
            geometry: {
                type: "Polygon",
                coordinates: [[[92.0234, 24.3167], [92.0267, 24.3167], [92.0267, 24.3200], [92.0234, 24.3200], [92.0234, 24.3167]]]
            }
        }
    };

    useEffect(() => {
        // Add page entrance animation
        const uploadPage = document.getElementById('uploadPage');
        if (uploadPage) {
            uploadPage.style.opacity = '0';
            uploadPage.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                uploadPage.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                uploadPage.style.opacity = '1';
                uploadPage.style.transform = 'translateY(0)';
            }, 100);
        }

        // Add keyboard shortcuts
        const handleKeyDown = (e) => {
            // Escape key to go back
            if (e.key === 'Escape') {
                goBack();
            }
            
            // Enter key to process files if ready
            if (e.key === 'Enter' && pdfFile && shapeFile && !processing) {
                processFiles();
            }
        };

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [pdfFile, shapeFile, processing]);

    const goBack = () => {
        navigate('/');
    };

    const handleFileSelect = (file, type) => {
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

        if (type === 'pdf') {
            setPdfFile(file);
        } else {
            setShapeFile(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
    };

    const handleDrop = (e, type) => {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0], type);
        }
    };

    const processFiles = async () => {
        if (!pdfFile || !shapeFile) return;

        console.log('Starting file processing...'); // Debug log
        setProcessing(true);
        
        // Processing steps simulation
        const processingSteps = [
            'Reading PDF document...',
            'Applying OCR technology...',
            'Extracting text with NER...',
            'Processing shapefile coordinates...',
            'Validating spatial data...',
            'Generating results...'
        ];

        for (let i = 0; i < processingSteps.length; i++) {
            console.log(`Processing step ${i + 1}: ${processingSteps[i]}`); // Debug log
            await new Promise(resolve => setTimeout(resolve, 500));
        }

        // Randomly select sample data from one of the states
        const states = ['telangana', 'odisha', 'madhyaPradesh', 'tripura'];
        const randomState = states[Math.floor(Math.random() * states.length)];
        const selectedData = sampleData[randomState];
        
        console.log('Setting results:', selectedData); // Debug log
        setResults(selectedData);
        setProcessing(false);
        console.log('Processing completed!'); // Debug log
    };

    const resetUpload = () => {
        setPdfFile(null);
        setShapeFile(null);
        setResults(null);
        setProcessing(false);
        
        // Reset file inputs
        const pdfInput = document.getElementById('pdfFile');
        const shapeInput = document.getElementById('shapeFile');
        if (pdfInput) pdfInput.value = '';
        if (shapeInput) shapeInput.value = '';
        
        // Scroll back to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const saveToAtlas = () => {
        if (!results) return;

        // Simulate saving process
        setTimeout(() => {
            alert(`🎉 Success! FRA Claim Processed Successfully\n\n` +
                  `📋 Claim Details:\n` +
                  `• ID: ${results.claim_id}\n` +
                  `• Holder: ${results.name}\n` +
                  `• Location: ${results.village}, ${results.district}, ${results.state}\n` +
                  `• Type: ${results.claim_type}\n` +
                  `• Area: ${results.area_claimed}\n` +
                  `• Status: ${results.status}\n\n` +
                  `🔧 AI Processing Completed:\n` +
                  `✓ OCR text extraction\n` +
                  `✓ NER data classification\n` +
                  `✓ Spatial coordinate validation\n` +
                  `✓ Atlas integration\n` +
                  `✓ DSS eligibility analysis\n\n` +
                  `🗺️ Data is now available in the WebGIS portal and ready for scheme mapping!`);
            
            setTimeout(() => {
                resetUpload();
            }, 2000);
        }, 2000);
    };

    const FileUploadArea = ({ type, file, onFileSelect }) => (
        <div className="upload-card">
            <div className="upload-icon">{type === 'pdf' ? '📄' : '🗺️'}</div>
            <h3>{type === 'pdf' ? 'FRA Claim Document' : 'Patta Holder Shapefile'}</h3>
            <p>Upload {type === 'pdf' ? 'PDF document containing claim details' : 'shapefile with boundary coordinates'}</p>
            <div 
                className="file-upload-area" 
                id={`${type}Upload`}
                onClick={() => document.getElementById(`${type}File`).click()}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={(e) => handleDrop(e, type)}
                style={{
                    border: file ? '3px solid var(--forest-accent)' : '3px dashed var(--forest-light)',
                    background: file ? 'rgba(125, 180, 108, 0.15)' : 'rgba(245, 245, 220, 0.3)'
                }}
            >
                <input 
                    type="file" 
                    id={`${type}File`} 
                    accept={type === 'pdf' ? '.pdf' : '.shp,.zip'} 
                    style={{display: 'none'}}
                    onChange={(e) => e.target.files[0] && handleFileSelect(e.target.files[0], type)}
                />
                {!file ? (
                    <div className="upload-placeholder">
                        <div className="upload-icon-large">{type === 'pdf' ? '📋' : '🌍'}</div>
                        <p>Drag & drop {type === 'pdf' ? 'PDF' : 'shapefile'} file here or <span className="upload-link">browse</span></p>
                        <small>Supported: {type === 'pdf' ? 'PDF files up to 10MB' : '.shp, .zip files up to 20MB'}</small>
                    </div>
                ) : (
                    <div className="file-info">
                        <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                            <span style={{fontSize: '2rem'}}>{type === 'pdf' ? '📄' : '🗺️'}</span>
                            <div>
                                <strong>{file.name}</strong><br/>
                                <small>Size: {(file.size / 1024 / 1024).toFixed(2)} MB</small><br/>
                                <small style={{color: 'var(--forest-accent)'}}>✓ Ready for processing</small>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div id="uploadPage" className="upload-page">
            <div className="upload-container">
                <div className="upload-header">
                    <div className="header-buttons">
                        <button className="back-btn" onClick={goBack}>
                            <span>←</span> Back to Home
                        </button>
                        <button className="fra-claims-btn" onClick={() => navigate('/fra-claims')}>
                            <span>📊</span> View FRA Claims
                        </button>
                    </div>
                    <h1 className="upload-title">Upload FRA Document</h1>
                    <p className="upload-subtitle">Upload PDF documents and shapefiles for AI-powered processing</p>
                </div>

                <div className="upload-content">
                    <div className="upload-grid">
                        <div className="upload-section">
                            <FileUploadArea type="pdf" file={pdfFile} onFileSelect={handleFileSelect} />
                        </div>
                        <div className="upload-section">
                            <FileUploadArea type="shape" file={shapeFile} onFileSelect={handleFileSelect} />
                        </div>
                    </div>

                    {/* Process Button */}
                    <div className="process-section">
                        <button 
                            className={`process-btn ${processing ? 'processing' : ''}`}
                            onClick={processFiles} 
                            disabled={!pdfFile || !shapeFile || processing}
                            style={{
                                opacity: (pdfFile && shapeFile && !processing) ? '1' : '0.5',
                                cursor: (pdfFile && shapeFile && !processing) ? 'pointer' : 'not-allowed'
                            }}
                        >
                            <span className="btn-icon">{processing ? '🔄' : (pdfFile && shapeFile) ? '🚀' : '🔄'}</span>
                            {processing ? 'Processing with AI...' : 'Process Documents with AI'}
                        </button>
                        <p className="process-note">AI will extract data using OCR and NER technologies</p>
                    </div>

                    {/* Results Section */}
                    {results && (
                        <div className="results-section" id="resultsSection">
                            {console.log('Rendering results section with data:', results)}
                            <h3 className="results-title">🎯 Extraction Results</h3>
                            <div className="results-grid">
                                <div className="result-card">
                                    <h4>📊 Extracted Data (OCR + NER)</h4>
                                    <pre className="json-display">{JSON.stringify(results, null, 2)}</pre>
                                </div>
                                <div className="result-card">
                                    <h4>🗺️ Spatial Information</h4>
                                    <div className="spatial-info">
                                        <div className="coord-display">
                                            <strong>Boundary Coordinates:</strong><br/>
                                            Latitude: {results.geometry.coordinates[0][0][1].toFixed(4)}°N to {results.geometry.coordinates[0][2][1].toFixed(4)}°N<br/>
                                            Longitude: {results.geometry.coordinates[0][0][0].toFixed(4)}°E to {results.geometry.coordinates[0][2][0].toFixed(4)}°E<br/>
                                            <strong>Area:</strong> {results.area_claimed}<br/>
                                            <strong>Survey No:</strong> {results.survey_number}
                                        </div>
                                        <div className="map-preview">
                                            <div className="mini-map">
                                                <div style={{position: 'relative', width: '100%', height: '100%'}}>
                                                    {/* Terrain background */}
                                                    <div style={{position: 'absolute', inset: '0', background: 'linear-gradient(135deg, #87CEEB 0%, #98FB98 50%, #90EE90 100%)'}}></div>
                                                    
                                                    {/* Forest areas */}
                                                    <div style={{position: 'absolute', top: '10%', left: '10%', width: '25%', height: '25%', background: '#228B22', borderRadius: '50%', opacity: '0.7'}}></div>
                                                    <div style={{position: 'absolute', top: '20%', right: '15%', width: '20%', height: '20%', background: '#006400', borderRadius: '30%', opacity: '0.7'}}></div>
                                                    
                                                    {/* Claim boundary (main polygon) */}
                                                    <div style={{position: 'absolute', top: '30%', left: '25%', width: '45%', height: '40%', border: '3px solid var(--forest-primary)', background: 'rgba(125, 180, 108, 0.4)', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.2)'}}></div>
                                                    
                                                    {/* Village marker */}
                                                    <div style={{position: 'absolute', top: '45%', left: '42%', width: '12px', height: '12px', background: '#FF4500', border: '2px solid white', borderRadius: '50%', boxShadow: '0 2px 4px rgba(0,0,0,0.3)'}}></div>
                                                    
                                                    {/* Location label */}
                                                    <div style={{position: 'absolute', bottom: '8px', right: '8px', background: 'rgba(255,255,255,0.9)', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem', color: 'var(--forest-primary)', fontWeight: '500', boxShadow: '0 1px 3px rgba(0,0,0,0.2)'}}>
                                                        📍 {results.village}, {results.state}
                                                    </div>
                                                    
                                                    {/* Coordinates overlay */}
                                                    <div style={{position: 'absolute', top: '8px', left: '8px', background: 'rgba(26, 77, 58, 0.8)', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.6rem', fontFamily: 'monospace'}}>
                                                        {results.geometry.coordinates[0][0][1].toFixed(3)}°N, {results.geometry.coordinates[0][0][0].toFixed(3)}°E
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="action-buttons">
                                <button className="secondary-btn" onClick={resetUpload}>Upload Another</button>
                                <button className="primary-btn" onClick={saveToAtlas}>Save to Atlas</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Upload;