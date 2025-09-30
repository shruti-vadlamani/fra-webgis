import React, { useEffect, useState } from 'react';
import './FRAClaims.css';

const FRAClaims = () => {
    const [claimsData, setClaimsData] = useState({
        totalClaims: 0,
        approvedClaims: 0,
        pendingClaims: 0,
        rejectedClaims: 0,
        districts: []
    });

    const [activeTab, setActiveTab] = useState('overview');
    const [selectedStatus, setSelectedStatus] = useState('all');
    const [language, setLanguage] = useState('en'); // 'en' for English, 'hi' for Hindi
    const [sampleClaims, setSampleClaims] = useState([]);

    // Translation object
    const translations = {
        en: {
            title: "FRA Claims Dashboard",
            subtitle: "Forest Rights Act Claims Statistics for Telangana State",
            overview: "Overview",
            viewClaims: "View Claims",
            analytics: "Analytics",
            totalClaims: "Total Claims",
            approvedClaims: "Approved Claims",
            pendingClaims: "Pending Claims",
            rejectedClaims: "Rejected Claims",
            districtBreakdown: "District-wise Claims Breakdown",
            individualClaims: "Individual Claims Details",
            allClaims: "All Claims",
            approved: "Approved",
            pending: "Pending",
            rejected: "Rejected",
            pattalder: "Patta Holder",
            village: "Village",
            district: "District",
            type: "Type",
            area: "Area",
            submitted: "Submitted",
            lastUpdated: "Last Updated",
            location: "Location",
            reason: "Reason",
            hectares: "hectares",
            advancedAnalytics: "Advanced Analytics",
            statusDistribution: "Claims Status Distribution",
            districtApproval: "District-wise Approval Rates",
            claimsByType: "Claims Distribution by Type",
            monthlyTrend: "Monthly Claims Submission Trend",
            loadMore: "Load More Claims",
            remaining: "remaining",
            backToHome: "Back to Home",
            ifr: "Individual Forest Rights",
            cfr: "Community Forest Rights",
            cr: "Community Rights"
        },
        hi: {
            title: "वन अधिकार दावा डैशबोर्ड",
            subtitle: "तेलंगाना राज्य के लिए वन अधिकार अधिनियम दावा आंकड़े",
            overview: "अवलोकन",
            viewClaims: "दावे देखें",
            analytics: "विश्लेषण",
            totalClaims: "कुल दावे",
            approvedClaims: "स्वीकृत दावे",
            pendingClaims: "लंबित दावे",
            rejectedClaims: "अस्वीकृत दावे",
            districtBreakdown: "जिलेवार दावा विवरण",
            individualClaims: "व्यक्तिगत दावा विवरण",
            allClaims: "सभी दावे",
            approved: "स्वीकृत",
            pending: "लंबित",
            rejected: "अस्वीकृत",
            pattalder: "पट्टाधारक",
            village: "गांव",
            district: "जिला",
            type: "प्रकार",
            area: "क्षेत्रफल",
            submitted: "प्रस्तुत",
            lastUpdated: "अंतिम अपडेट",
            location: "स्थान",
            reason: "कारण",
            hectares: "हेक्टेयर",
            advancedAnalytics: "उन्नत विश्लेषण",
            statusDistribution: "दावा स्थिति वितरण",
            districtApproval: "जिलेवार अनुमोदन दर",
            claimsByType: "प्रकार के अनुसार दावा वितरण",
            monthlyTrend: "मासिक दावा प्रस्तुति प्रवृत्ति",
            loadMore: "अधिक दावे लोड करें",
            remaining: "शेष",
            backToHome: "होम पर वापस",
            ifr: "व्यक्तिगत वन अधिकार",
            cfr: "सामुदायिक वन अधिकार",
            cr: "सामुदायिक अधिकार"
        }
    };

    const t = translations[language];

    useEffect(() => {
        // Simulate loading FRA claims data for Telangana
        const mockData = {
            totalClaims: 15847,
            approvedClaims: 8923,
            pendingClaims: 4521,
            rejectedClaims: 2403,
            districts: [
                { name: 'Adilabad', total: 2341, approved: 1456, pending: 623, rejected: 262 },
                { name: 'Hyderabad', total: 1876, approved: 1234, pending: 421, rejected: 221 },
                { name: 'Karimnagar', total: 2156, approved: 1345, pending: 567, rejected: 244 },
                { name: 'Khammam', total: 1987, approved: 1123, pending: 534, rejected: 330 },
                { name: 'Medak', total: 1654, approved: 987, pending: 445, rejected: 222 },
                { name: 'Nalgonda', total: 2234, approved: 1456, pending: 556, rejected: 222 },
                { name: 'Nizamabad', total: 1876, approved: 1098, pending: 567, rejected: 211 },
                { name: 'Warangal', total: 1723, approved: 1224, pending: 308, rejected: 191 }
            ]
        };

        // Generate sample claims with random patta holders and villagers
        const generateSampleClaims = () => {
            const pattas = ['Ramesh Kumar', 'Lakshmi Devi', 'Suresh Reddy', 'Anitha Kumari', 'Venkat Rao', 'Padma Devi', 'Krishna Murthy', 'Sita Devi', 'Ravi Kumar', 'Manjula Devi', 'Naresh Babu', 'Kavitha Reddy'];
            const villages = ['Kothapalli', 'Yellareddy', 'Banswada', 'Armoor', 'Bodhan', 'Jukkal', 'Kamareddy', 'Pitlam', 'Sadashivnagar', 'Bichkunda', 'Machareddy', 'Nizamabad Rural'];
            const claimTypes = ['IFR', 'CFR', 'CR'];
            const statuses = ['approved', 'pending', 'rejected'];
            const reasons = {
                approved: ['Complete documentation', 'Valid traditional rights', 'Community verification successful'],
                pending: ['Documentation under review', 'Field verification pending', 'Committee review in progress'],
                rejected: ['Insufficient evidence', 'Overlapping claims', 'Outside forest area']
            };

            const claims = [];
            for (let i = 0; i < 50; i++) {
                const status = statuses[Math.floor(Math.random() * statuses.length)];
                const claimType = claimTypes[Math.floor(Math.random() * claimTypes.length)];
                claims.push({
                    id: `FRA_${String(i + 1).padStart(4, '0')}`,
                    pattalder: pattas[Math.floor(Math.random() * pattas.length)],
                    village: villages[Math.floor(Math.random() * villages.length)],
                    district: mockData.districts[Math.floor(Math.random() * mockData.districts.length)].name,
                    claimType: claimType,
                    area: (Math.random() * 10 + 0.5).toFixed(2),
                    status: status,
                    submissionDate: new Date(2023, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1).toLocaleDateString(),
                    lastUpdated: new Date(2024, Math.floor(Math.random() * 9), Math.floor(Math.random() * 28) + 1).toLocaleDateString(),
                    reason: reasons[status][Math.floor(Math.random() * reasons[status].length)],
                    coordinates: `${(17.5 + Math.random() * 2).toFixed(4)}°N, ${(78.2 + Math.random() * 2).toFixed(4)}°E`
                });
            }
            return claims;
        };
        
        setClaimsData(mockData);
        setSampleClaims(generateSampleClaims());
    }, []);

    const getStatusColor = (status) => {
        switch (status) {
            case 'approved': return '#28a745';
            case 'pending': return '#ffc107';
            case 'rejected': return '#dc3545';
            default: return '#6c757d';
        }
    };

    const getPercentage = (value, total) => {
        return ((value / total) * 100).toFixed(1);
    };

    const getFilteredClaims = () => {
        if (selectedStatus === 'all') return sampleClaims;
        return sampleClaims.filter(claim => claim.status === selectedStatus);
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'approved': return '';
            case 'pending': return '';
            case 'rejected': return '';
            default: return '';
        }
    };

    const getClaimTypeFullName = (type) => {
        switch (type) {
            case 'IFR': return 'Individual Forest Rights';
            case 'CFR': return 'Community Forest Rights';
            case 'CR': return 'Community Rights';
            default: return type;
        }
    };

    return (
        <div className="fra-claims-container">
            {/* Header */}
            <header className="claims-header">
                <div className="header-content">
                    <div className="header-top">
                        <div className="header-text">
                            <h1>{t.title}</h1>
                            <p>{t.subtitle}</p>
                        </div>
                        <div className="language-toggle">
                            <button 
                                className={`lang-btn ${language === 'en' ? 'active' : ''}`}
                                onClick={() => setLanguage('en')}
                            >
                                EN
                            </button>
                            <button 
                                className={`lang-btn ${language === 'hi' ? 'active' : ''}`}
                                onClick={() => setLanguage('hi')}
                            >
                                हिं
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation Tabs */}
            <section className="navigation-tabs">
                <div className="tabs-container">
                    <button 
                        className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        {t.overview}
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'claims' ? 'active' : ''}`}
                        onClick={() => setActiveTab('claims')}
                    >
                        {t.viewClaims}
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
                        onClick={() => setActiveTab('analytics')}
                    >
                        {t.analytics}
                    </button>
                </div>
            </section>

            {/* Statistics Overview */}
            {activeTab === 'overview' && (
                <>
                    <section className="stats-overview">
                        <div className="stats-container">
                            <div className="stat-card total" onClick={() => {setActiveTab('claims'); setSelectedStatus('all');}}>
                                <div className="stat-content">
                                    <h3>{t.totalClaims}</h3>
                                    <div className="stat-number">{claimsData.totalClaims.toLocaleString()}</div>
                                </div>
                            </div>
                            
                            <div className="stat-card approved" onClick={() => {setActiveTab('claims'); setSelectedStatus('approved');}}>
                                <div className="stat-content">
                                    <h3>{t.approvedClaims}</h3>
                                    <div className="stat-number">{claimsData.approvedClaims.toLocaleString()}</div>
                                    <div className="stat-percentage">{getPercentage(claimsData.approvedClaims, claimsData.totalClaims)}%</div>
                                </div>
                            </div>
                            
                            <div className="stat-card pending" onClick={() => {setActiveTab('claims'); setSelectedStatus('pending');}}>
                                <div className="stat-content">
                                    <h3>{t.pendingClaims}</h3>
                                    <div className="stat-number">{claimsData.pendingClaims.toLocaleString()}</div>
                                    <div className="stat-percentage">{getPercentage(claimsData.pendingClaims, claimsData.totalClaims)}%</div>
                                </div>
                            </div>
                            
                            <div className="stat-card rejected" onClick={() => {setActiveTab('claims'); setSelectedStatus('rejected');}}>
                                <div className="stat-content">
                                    <h3>{t.rejectedClaims}</h3>
                                    <div className="stat-number">{claimsData.rejectedClaims.toLocaleString()}</div>
                                    <div className="stat-percentage">{getPercentage(claimsData.rejectedClaims, claimsData.totalClaims)}%</div>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* District-wise Breakdown */}
                    <section className="district-breakdown">
                        <div className="section-container">
                            <h2>{t.districtBreakdown}</h2>
                            <div className="districts-grid">
                                {claimsData.districts.map((district, index) => (
                                    <div key={index} className="district-card">
                                        <h3>{district.name}</h3>
                                        <div className="district-stats">
                                            <div className="district-total">
                                                <span className="label">Total:</span>
                                                <span className="value">{district.total.toLocaleString()}</span>
                                            </div>
                                            <div className="status-breakdown">
                                                <div className="status-item approved">
                                                    <span className="dot"></span>
                                                    <span>{t.approved}: {district.approved}</span>
                                                </div>
                                                <div className="status-item pending">
                                                    <span className="dot"></span>
                                                    <span>{t.pending}: {district.pending}</span>
                                                </div>
                                                <div className="status-item rejected">
                                                    <span className="dot"></span>
                                                    <span>{t.rejected}: {district.rejected}</span>
                                                </div>
                                            </div>
                                            <div className="progress-bar">
                                                <div 
                                                    className="progress-approved" 
                                                    style={{ width: `${getPercentage(district.approved, district.total)}%` }}
                                                ></div>
                                                <div 
                                                    className="progress-pending" 
                                                    style={{ width: `${getPercentage(district.pending, district.total)}%` }}
                                                ></div>
                                                <div 
                                                    className="progress-rejected" 
                                                    style={{ width: `${getPercentage(district.rejected, district.total)}%` }}
                                                ></div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </section>
                </>
            )}

            {/* Claims View Tab */}
            {activeTab === 'claims' && (
                <section className="claims-view">
                    <div className="claims-container">
                        <div className="claims-header-section">
                            <h2>{t.individualClaims}</h2>
                            <div className="status-filters">
                                <button 
                                    className={`filter-btn ${selectedStatus === 'all' ? 'active' : ''}`}
                                    onClick={() => setSelectedStatus('all')}
                                >
                                    {t.allClaims} ({sampleClaims.length})
                                </button>
                                <button 
                                    className={`filter-btn approved ${selectedStatus === 'approved' ? 'active' : ''}`}
                                    onClick={() => setSelectedStatus('approved')}
                                >
                                    {t.approved} ({sampleClaims.filter(c => c.status === 'approved').length})
                                </button>
                                <button 
                                    className={`filter-btn pending ${selectedStatus === 'pending' ? 'active' : ''}`}
                                    onClick={() => setSelectedStatus('pending')}
                                >
                                    {t.pending} ({sampleClaims.filter(c => c.status === 'pending').length})
                                </button>
                                <button 
                                    className={`filter-btn rejected ${selectedStatus === 'rejected' ? 'active' : ''}`}
                                    onClick={() => setSelectedStatus('rejected')}
                                >
                                    {t.rejected} ({sampleClaims.filter(c => c.status === 'rejected').length})
                                </button>
                            </div>
                        </div>

                        <div className="claims-grid">
                            {getFilteredClaims().slice(0, 12).map((claim, index) => (
                                <div key={index} className={`claim-card ${claim.status}`}>
                                    <div className="claim-header">
                                        <div className="claim-id">{claim.id}</div>
                                        <div className={`claim-status ${claim.status}`}>
                                            {getStatusIcon(claim.status)} {claim.status.toUpperCase()}
                                        </div>
                                    </div>
                                    <div className="claim-details">
                                        <div className="detail-row">
                                            <span className="label">{t.pattalder}:</span>
                                            <span className="value">{claim.pattalder}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.village}:</span>
                                            <span className="value">{claim.village}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.district}:</span>
                                            <span className="value">{claim.district}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.type}:</span>
                                            <span className="value claim-type">{claim.claimType}</span>
                                            <span className="type-full">{getClaimTypeFullName(claim.claimType)}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.area}:</span>
                                            <span className="value">{claim.area} hectares</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.submitted}:</span>
                                            <span className="value">{claim.submissionDate}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.lastUpdated}:</span>
                                            <span className="value">{claim.lastUpdated}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="label">{t.location}:</span>
                                            <span className="value coordinates">{claim.coordinates}</span>
                                        </div>
                                        <div className="detail-row reason">
                                            <span className="label">{t.reason}:</span>
                                            <span className="value">{claim.reason}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                        
                        {getFilteredClaims().length > 12 && (
                            <div className="load-more">
                                <button className="load-more-btn">
                                    {t.loadMore} ({getFilteredClaims().length - 12} {t.remaining})
                                </button>
                            </div>
                        )}
                    </div>
                </section>
            )}

            {/* Analytics Tab */}
            {activeTab === 'analytics' && (
                <section className="analytics-view">
                    <div className="analytics-container">
                        <h2>{t.advancedAnalytics}</h2>
                        

                        {/* Charts Section */}
                        <div className="charts-section">
                            
                            {/* Status Distribution Chart */}
                            <div className="chart-container">
                                <div className="chart-card">
                                    <h4>{t.statusDistribution}</h4>
                                    <div className="pie-chart">
                                        <div className="pie-chart-container">
                                            <svg width="300" height="300" viewBox="0 0 300 300">
                                                <circle cx="150" cy="150" r="100" fill="none" stroke="#e9ecef" strokeWidth="20"/>
                                                <circle 
                                                    cx="150" cy="150" r="100" 
                                                    fill="none" 
                                                    stroke="#28a745" 
                                                    strokeWidth="20"
                                                    strokeDasharray={`${(claimsData.approvedClaims / claimsData.totalClaims) * 628} 628`}
                                                    strokeDashoffset="0"
                                                    transform="rotate(-90 150 150)"
                                                />
                                                <circle 
                                                    cx="150" cy="150" r="100" 
                                                    fill="none" 
                                                    stroke="#ffc107" 
                                                    strokeWidth="20"
                                                    strokeDasharray={`${(claimsData.pendingClaims / claimsData.totalClaims) * 628} 628`}
                                                    strokeDashoffset={`-${(claimsData.approvedClaims / claimsData.totalClaims) * 628}`}
                                                    transform="rotate(-90 150 150)"
                                                />
                                                <circle 
                                                    cx="150" cy="150" r="100" 
                                                    fill="none" 
                                                    stroke="#dc3545" 
                                                    strokeWidth="20"
                                                    strokeDasharray={`${(claimsData.rejectedClaims / claimsData.totalClaims) * 628} 628`}
                                                    strokeDashoffset={`-${((claimsData.approvedClaims + claimsData.pendingClaims) / claimsData.totalClaims) * 628}`}
                                                    transform="rotate(-90 150 150)"
                                                />
                                                <text x="150" y="150" textAnchor="middle" dy="0.3em" className="chart-center-text">
                                                    {claimsData.totalClaims.toLocaleString()}
                                                </text>
                                                <text x="150" y="170" textAnchor="middle" dy="0.3em" className="chart-center-label">
                                                    {t.totalClaims}
                                                </text>
                                            </svg>
                                        </div>
                                        <div className="pie-legend">
                                            <div className="legend-item">
                                                <span className="legend-dot approved"></span>
                                                <span>{t.approved} ({getPercentage(claimsData.approvedClaims, claimsData.totalClaims)}%)</span>
                                            </div>
                                            <div className="legend-item">
                                                <span className="legend-dot pending"></span>
                                                <span>{t.pending} ({getPercentage(claimsData.pendingClaims, claimsData.totalClaims)}%)</span>
                                            </div>
                                            <div className="legend-item">
                                                <span className="legend-dot rejected"></span>
                                                <span>{t.rejected} ({getPercentage(claimsData.rejectedClaims, claimsData.totalClaims)}%)</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* District Comparison Bar Chart */}
                                <div className="chart-card">
                                    <h4>{t.districtApproval}</h4>
                                    <div className="bar-chart">
                                        {claimsData.districts.map((district, index) => {
                                            const approvalRate = (district.approved / district.total) * 100;
                                            return (
                                                <div key={index} className="bar-item">
                                                    <div className="bar-label">{district.name}</div>
                                                    <div className="bar-container">
                                                        <div 
                                                            className="bar-fill" 
                                                            style={{ width: `${approvalRate}%` }}
                                                        ></div>
                                                        <span className="bar-value">{approvalRate.toFixed(1)}%</span>
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>

                            {/* Claims by Type Chart */}
                            <div className="chart-container">
                                <div className="chart-card full-width">
                                    <h4>{t.claimsByType}</h4>
                                    <div className="type-chart">
                                        <div className="type-bar">
                                            <div className="type-item ifr">
                                                <div className="type-header">
                                                    <span className="type-label">IFR - {t.ifr}</span>
                                                    <span className="type-count">45%</span>
                                                </div>
                                                <div className="type-progress">
                                                    <div className="type-fill" style={{ width: '45%' }}></div>
                                                </div>
                                            </div>
                                            <div className="type-item cfr">
                                                <div className="type-header">
                                                    <span className="type-label">CFR - {t.cfr}</span>
                                                    <span className="type-count">35%</span>
                                                </div>
                                                <div className="type-progress">
                                                    <div className="type-fill" style={{ width: '35%' }}></div>
                                                </div>
                                            </div>
                                            <div className="type-item cr">
                                                <div className="type-header">
                                                    <span className="type-label">CR - {t.cr}</span>
                                                    <span className="type-count">20%</span>
                                                </div>
                                                <div className="type-progress">
                                                    <div className="type-fill" style={{ width: '20%' }}></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Timeline Chart */}
                            <div className="chart-container">
                                <div className="chart-card full-width">
                                    <h4>{t.monthlyTrend}</h4>
                                    <div className="timeline-chart">
                                        <div className="timeline-grid">
                                            {[
                                                { month: 'Jan', value: 980, height: 65 },
                                                { month: 'Feb', value: 675, height: 45 },
                                                { month: 'Mar', value: 1200, height: 80 },
                                                { month: 'Apr', value: 825, height: 55 },
                                                { month: 'May', value: 1050, height: 70 },
                                                { month: 'Jun', value: 1275, height: 85 },
                                                { month: 'Jul', value: 900, height: 60 },
                                                { month: 'Aug', value: 1125, height: 75 },
                                                { month: 'Sep', value: 1350, height: 90 },
                                                { month: 'Oct', value: 750, height: 50 },
                                                { month: 'Nov', value: 975, height: 65 },
                                                { month: 'Dec', value: 600, height: 40 }
                                            ].map((data, index) => (
                                                <div key={index} className="timeline-bar">
                                                    <div className="timeline-value">{data.value}</div>
                                                    <div 
                                                        className="timeline-fill" 
                                                        style={{ 
                                                            height: `${data.height}%`,
                                                            minHeight: '20px'
                                                        }}
                                                        title={`${data.month}: ${data.value} claims`}
                                                    ></div>
                                                    <span className="timeline-label">{data.month}</span>
                                                </div>
                                            ))}
                                        </div>
                                        <div className="timeline-axis">
                                            <span>0</span>
                                            <span>500</span>
                                            <span>1000</span>
                                            <span>1500</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </section>
            )}

            {/* Back to Home */}
            <section className="navigation-section">
                <div className="nav-container">
                    <button 
                        className="back-btn" 
                        onClick={() => window.location.href = '/'}
                    >
                        ← {t.backToHome}
                    </button>
                    <button 
                        className="map-btn" 
                        onClick={() => window.location.href = '/gee'}
                    >
                        View Interactive Map →
                    </button>
                </div>
            </section>
        </div>
    );
};

export default FRAClaims;
