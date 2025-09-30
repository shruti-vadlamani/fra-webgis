import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Page loader
        const loader = document.getElementById('loader');
        if (loader) {
            setTimeout(() => {
                loader.classList.add('hidden');
            }, 1500);
        }

        // Header scroll effect
        const handleScroll = () => {
            const header = document.getElementById('header');
            if (header) {
                if (window.scrollY > 100) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            }
        };

        window.addEventListener('scroll', handleScroll);

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add hover effect for action cards
        document.querySelectorAll('.action-card').forEach(card => {
            const handleMouseEnter = function() {
                this.style.transform = 'translateY(-15px) scale(1.02)';
            };
            
            const handleMouseLeave = function() {
                this.style.transform = 'translateY(0) scale(1)';
            };

            card.addEventListener('mouseenter', handleMouseEnter);
            card.addEventListener('mouseleave', handleMouseLeave);
        });

        // Parallax effect for hero section
        const handleParallax = () => {
            const scrolled = window.pageYOffset;
            const hero = document.querySelector('.hero');
            if (hero) {
                hero.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        };

        window.addEventListener('scroll', handleParallax);

        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe info cards and action cards
        document.querySelectorAll('.info-card, .action-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });

        // Cleanup event listeners
        return () => {
            window.removeEventListener('scroll', handleScroll);
            window.removeEventListener('scroll', handleParallax);
        };
    }, []);

    const navigateToUpload = () => {
        navigate('/upload');
    };

    const navigateToMap = () => {
        // Navigate to the GEE-style interface with FRA and forest data
        window.location.href = '/gee';
    };

    const navigateToFRAClaims = () => {
        // Navigate to the FRA Claims statistics page
        window.location.href = '/fra-claims';
    };

    return (
        <>
            <div className="page-loader" id="loader">
                <div className="loader-content">
                    <div className="loader-spinner"></div>
                    <p>Loading Vanachitra.ai...</p>
                </div>
            </div>

            <header className="header" id="header">
                <div className="nav-container">
                    <a href="#" className="logo">vanachitra.ai</a>
                    <nav className="nav-menu">
                        <a href="#home" className="nav-link">Home</a>
                        <a href="#about" className="nav-link">About</a>
                        <a href="#features" className="nav-link">Features</a>
                        <a href="#contact" className="nav-link">Contact</a>
                    </nav>
                </div>
            </header>

            <section className="hero" id="home">
                {/* Floating Leaves */}
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>
            <div className="leaf"></div>                <div className="hero-content">
                    <h1 className="hero-title">vanachitra.ai</h1>
                    <p className="hero-subtitle">Forest Rights Act Atlas & Decision Support System</p>
                    <p className="hero-description">
                        Empowering forest-dwelling communities through AI-powered mapping, digitization of FRA records, 
                        and intelligent decision support for sustainable forest governance across Madhya Pradesh, 
                        Tripura, Odisha, and Telangana.
                    </p>
                </div>
            </section>

            <section className="info-section" id="about">
                <div className="info-container">
                    <div className="info-grid">
                        <div className="info-card">
                            <img src="/images/fraimg.jpg" alt="AI-Powered Atlas" className="info-image" />
                            <div className="info-card-content">
                                <h3 className="info-title">AI-Powered Atlas</h3>
                                <p className="info-text">
                                    Interactive WebGIS platform visualizing FRA claims, granted titles, and forest resources 
                                    using satellite imagery and machine learning for comprehensive spatial analysis.
                                </p>
                            </div>
                        </div>
                        <div className="info-card">
                            <img src="/images/dssimg.jpg" alt="Decision Support System" className="info-image" />
                            <div className="info-card-content">
                                <h3 className="info-title">Decision Support System</h3>
                                <p className="info-text">
                                    Intelligent recommendation engine linking FRA holders with Central Sector Schemes like 
                                    PM-KISAN, Jal Jeevan Mission, and MGNREGA for targeted development interventions.
                                </p>
                            </div>
                        </div>
                        <div className="info-card">
                            <img src="/images/asstmpimg.jpg" alt="Digital Asset Mapping" className="info-image" />
                            <div className="info-card-content">
                                <h3 className="info-title">Digital Asset Mapping</h3>
                                <p className="info-text">
                                    Computer vision and remote sensing technology to identify and map agricultural land, 
                                    water bodies, forest cover, and community assets in FRA villages.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="action-section" id="features">
                <div className="action-container">
                    <h2 className="section-title">Get Started</h2>
                    <p className="section-subtitle">Choose an action to begin exploring the FRA Atlas system</p>
                    
                    <div className="action-cards">
                        <div className="action-card" onClick={navigateToUpload}>
                            <div className="card-content">
                                <div className="action-icon notepad"></div>
                                <h3 className="action-title">Upload FRA Document</h3>
                                <p className="action-description">
                                    Digitize and process FRA documents using AI-powered OCR and NER technologies. 
                                    Extract key information and add to the central repository.
                                </p>
                                <button className="action-btn">Upload Document</button>
                            </div>
                        </div>
                        
                        <div className="action-card" onClick={navigateToMap}>
                            <div className="card-content">
                                <div className="action-icon globe"></div>
                                <h3 className="action-title">View Interactive Map</h3>
                                <p className="action-description">
                                    Explore the comprehensive FRA Atlas with satellite imagery, claim boundaries, 
                                    asset mapping, and scheme eligibility visualization.
                                </p>
                                <button className="action-btn">View Map</button>
                            </div>
                        </div>
                        
                        <div className="action-card" onClick={navigateToFRAClaims}>
                            <div className="card-content">
                                <div className="action-icon chart"></div>
                                <h3 className="action-title">FRA Claims</h3>
                                <p className="action-description">
                                    View comprehensive statistics of FRA claims for Telangana state including 
                                    approved, pending, and rejected claims with detailed analytics.
                                </p>
                                <button className="action-btn">View Claims</button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <footer className="footer" id="contact">
                <div className="footer-content">
                    <p className="footer-text">
                        Vanachitra.ai - Empowering Forest Communities through Technology
                    </p>
                    <div className="footer-links">
                        <a href="#" className="footer-link">Ministry of Tribal Affairs</a>
                        <a href="#" className="footer-link">Forest Department</a>
                        <a href="#" className="footer-link">Revenue Department</a>
                        <a href="#" className="footer-link">Support</a>
                    </div>
                    <p className="footer-text" style={{fontSize: '0.9rem', opacity: '0.6'}}>
                        © 2025 Vanachitra.ai - Smart India Hackathon Prototype
                    </p>
                </div>
            </footer>
        </>
    );
};

export default Home;