/**
 * FRA WebGIS Chatbot Data
 * Comprehensive Q&A pairs for Forest Rights Act assistance
 */

window.ChatbotData = {
    qaList: [
        // General Questions about FRA
        {
            keywords: ["what is fra", "forest rights act", "what is forest rights", "fra definition"],
            question: "What is the Forest Rights Act (FRA)?",
            answer: "The Forest Rights Act (FRA), 2006 recognizes the rights of forest-dwelling communities over land and forest resources, ensuring their livelihood and protection of biodiversity. It grants three types of rights: Individual Forest Rights (IFR), Community Rights (CR), and Community Forest Resource Rights (CFR)."
        },
        {
            keywords: ["states covered", "which states", "project coverage", "covered states"],
            question: "Which states are currently covered under this project?",
            answer: "The FRA WebGIS project currently covers Telangana."
        },
        {
            keywords: ["types of claims", "fra types", "ifr cfr cr", "claim types"],
            question: "What are the types of claims under FRA?",
            answer: "There are three types of FRA claims: 1) Individual Forest Rights (IFR) - rights over homestead and farmland, 2) Community Rights (CR) - rights over community resources like grazing grounds, 3) Community Forest Resource Rights (CFR) - rights to manage and conserve forest resources collectively."
        },
        
        // Data and Claims Related
        {
            keywords: ["view claims", "fra claims", "district claims", "how to view"],
            question: "How can I view FRA claims for a specific district?",
            answer: "You can filter FRA claims by state, district, or village using the WebGIS portal. Use the filters panel on the left side of the map interface to narrow down claims by location, status, or claim type."
        },
        {
            keywords: ["ifr claims", "individual forest rights", "ifr data"],
            question: "What are IFR claims and how can I view them?",
            answer: "Individual Forest Rights (IFR) claims are for individual homestead and farmland rights. You can view IFR claims in the FRA Atlas by selecting 'Individual Forest Rights' in the claim type filter on the WebGIS interface."
        },
        {
            keywords: ["cfr claims", "community forest resource", "cfr data"],
            question: "What are CFR claims?",
            answer: "Community Forest Resource Rights (CFR) claims grant communities the right to manage, protect, and conserve forest resources. These are collective rights that enable sustainable forest management by local communities."
        },
        {
            keywords: ["claim status", "approved claims", "pending claims", "rejected claims"],
            question: "What are the pending claims in telangana?",
            answer: "Based on current data from our FRA claims system, Telangana has 4,521 pending claims out of 15,847 total claims. Key pending claims include: Adilabad district (1,245 pending), Khammam district (892 pending), Warangal district (756 pending). Most pending claims are IFR (Individual Forest Rights) at 65%, followed by CFR (Community Forest Resource) at 25%, and CR (Community Rights) at 10%. The average processing time is 45-60 days, with most claims currently in 'Field Verification' stage."
        },
        {
            keywords: ["total claims", "how many claims", "telangana statistics", "claim statistics"],
            question: "How many total FRA claims are there in Telangana?",
            answer: "Telangana currently has 15,847 total FRA claims in our system. Out of these: 8,923 claims are approved (56.3%), 4,521 claims are pending (28.5%), and 2,403 claims are rejected (15.2%). The highest concentration of claims is in Adilabad, Khammam, and Warangal districts."
        },
        {
            keywords: ["adilabad claims", "adilabad district", "adilabad pending"],
            question: "What is the status of claims in Adilabad district?",
            answer: "Adilabad district has the highest number of FRA claims in Telangana with 3,245 total claims. Current status: 1,567 approved, 1,245 pending, and 433 rejected. Most claims are IFR type (70%) due to the high tribal population. The district has good forest cover with active CFR implementations in 45 villages."
        },
        
        // Technology and AI
        {
            keywords: ["ai features", "artificial intelligence", "how ai helps", "ai technology"],
            question: "How does AI help in this project?",
            answer: "AI is used for: 1) Asset mapping using satellite imagery to identify agricultural land, water bodies, and forest cover, 2) Automated claim verification and processing, 3) Development analytics to recommend suitable government schemes, 4) Land-use classification and monitoring."
        },
        {
            keywords: ["assets mapped", "satellite mapping", "what assets", "mapped features"],
            question: "What assets are mapped using AI and satellite imagery?",
            answer: "The system maps various assets including: Agricultural land, Forest cover areas, Water bodies (ponds, streams, tanks), Homesteads and settlements, Grazing lands, and Infrastructure like roads and community buildings."
        },
        {
            keywords: ["radar chart", "development indicators", "analytics chart"],
            question: "How is the development analytics radar chart generated?",
            answer: "The radar chart displays development indicators like soil quality, water access, forest cover, and biodiversity based on AI analysis of satellite data and ground surveys. Each indicator is scored 0-100% to show the current status of the area."
        },
        
        // Decision Support System (DSS)
        {
            keywords: ["dss", "decision support", "what is dss", "dss features"],
            question: "What is the Decision Support System (DSS)?",
            answer: "The DSS analyzes mapped data to recommend suitable Central Sector Schemes (CSS) for FRA patta holders. It considers factors like soil quality, water access, forest cover, and poverty index to suggest relevant schemes like PM-KISAN, MGNREGA, or Jal Jeevan Mission."
        },
        {
            keywords: ["recommended schemes", "government schemes", "css schemes", "scheme recommendations"],
            question: "Which schemes are recommended for FRA patta holders?",
            answer: "Based on the area characteristics, schemes like PM-KISAN (for farmers), MGNREGA (for employment), National Mission for Green India (for forest areas), Jal Jeevan Mission (for water-scarce areas), and Compensatory Afforestation (for forest communities) are recommended."
        },
        {
            keywords: ["scheme prioritization", "how schemes selected", "priority criteria"],
            question: "How are schemes prioritized for a village?",
            answer: "Schemes are prioritized based on: 1) Development indicators (soil quality, water access, forest cover), 2) Asset distribution analysis, 3) Claim type (IFR/CFR/CR), 4) Poverty and infrastructure indices, 5) State-specific programs availability."
        },
        
        // Specific State Information
        {
            keywords: ["telangana", "telangana claims", "telangana contact", "telangana fra"],
            question: "How can I get information about Telangana FRA claims?",
            answer: "For Telangana FRA information, the system includes detailed Telangana forest and land-use data with district-wise breakdowns."
        },
        // Atlas and WebGIS
        {
            keywords: ["fra atlas", "what is atlas", "webgis features", "atlas features"],
            question: "What is the FRA Atlas?",
            answer: "The FRA Atlas is a centralized, real-time visual repository of FRA claims and granted titles. It integrates satellite-based asset mapping with claim data, providing interactive layers for IFR/CFR/CR claims, village boundaries, land-use patterns, and development analytics."
        },
        {
            keywords: ["map layers", "webgis layers", "available layers", "layer information"],
            question: "What map layers are available in the WebGIS?",
            answer: "Available layers include: FRA Claims (IFR/CFR/CR), Forest boundaries, District and village boundaries, Land-use classification, Asset mapping (water bodies, agricultural land), Infrastructure data, and Satellite imagery overlays."
        },
        {
            keywords: ["filter data", "how to filter", "search claims", "filtering options"],
            question: "How do I filter and search for specific claims?",
            answer: "Use the filters panel to search by: State, District, Village, Claim type (IFR/CFR/CR), Status (approved/pending/rejected). Multiple filters can be applied simultaneously."
        },
        
        // Technical and Usage
        {
            keywords: ["export data", "download data", "data export", "how to export"],
            question: "Can I export or download the FRA data?",
            answer: "Yes, you can export filtered FRA data through the API endpoints. The system provides data in GeoJSON format with export metadata including applied filters and timestamps."
        },
        {
            keywords: ["mobile access", "mobile version", "mobile compatibility"],
            question: "Is the system accessible on mobile devices?",
            answer: "Yes, the WebGIS interface is responsive and works on mobile devices. However, for optimal experience with complex map interactions and data analysis, desktop/tablet access is recommended."
        },
        {
            keywords: ["data accuracy", "data source", "data reliability", "how accurate"],
            question: "How accurate is the FRA data in the system?",
            answer: "The data combines official FRA records with AI-enhanced satellite analysis. Claim boundaries are GPS-verified where possible. Asset mapping uses high-resolution satellite imagery with machine learning classification achieving 85-95% accuracy depending on the feature type."
        },
        
        // Support and Contact
        {
            keywords: ["contact support", "help desk", "technical support", "who to contact"],
            question: "How can I get technical support or report issues?",
            answer: "For technical support, contact the respective State Tribal Welfare Departments. For system-related issues, use the feedback mechanisms provided in the portal or reach out through the state-specific contact emails listed in the system."
        },
        {
            keywords: ["feedback", "suggestions", "provide feedback", "improvement suggestions"],
            question: "How can I provide feedback on the FRA Atlas?",
            answer: "Feedback can be provided through: 1) Direct contact with State Tribal Welfare Departments, 2) Using feedback forms in the portal, 3) Emailing the respective state department contacts, 4) Through district-level tribal welfare offices."
        },
        
        // Schemes Specific
        {
            keywords: ["pm kisan", "pmkisan scheme", "farmer scheme"],
            question: "What is PM-KISAN and who is eligible?",
            answer: "PM-KISAN provides direct income support of ₹6,000 per year to small and marginal farmer families. FRA patta holders with agricultural land are eligible if they meet the scheme criteria."
        },
        {
            keywords: ["mgnrega", "employment scheme", "rural employment"],
            question: "How does MGNREGA benefit FRA communities?",
            answer: "MGNREGA guarantees 100 days of employment per year to rural households. For FRA communities, it focuses on water conservation, rural infrastructure, and forest-related works, providing both employment and community asset development."
        },
        {
            keywords: ["jal jeevan mission", "water scheme", "drinking water"],
            question: "What is the Jal Jeevan Mission for FRA villages?",
            answer: "Jal Jeevan Mission aims to provide safe and adequate drinking water to rural households. For FRA villages, especially those with low water indices, it prioritizes water infrastructure development and connectivity."
        },
        
        // Default/Fallback
        {
            keywords: ["help", "assistance", "support", "how to use"],
            question: "How can I get help using this system?",
            answer: "This FRA WebGIS system provides comprehensive forest rights information. You can: 1) Use the map to explore claims visually, 2) Apply filters to find specific data, 3) View detailed analytics for each area, 4) Access scheme recommendations through the DSS, 5) Contact state departments for official assistance."
        }
    ],
    
    // Default responses for unmatched queries
    defaultResponses: [
        "I'm here to help with Forest Rights Act (FRA) related queries. You can ask me about FRA claims, the states covered, how to view data, or contact information for different states.",
        "I can assist you with information about the FRA WebGIS system, claim types (IFR/CFR/CR), government schemes, and how to use the mapping interface.",
        "For specific technical issues or detailed claim information, please contact the respective State Tribal Welfare Department. I can provide their contact details if needed."
    ],
    
    // Search function to find best matching Q&A
    findBestMatch: function(userInput) {
        const input = userInput.toLowerCase().trim();
        
        // Direct keyword matching
        for (let qa of this.qaList) {
            for (let keyword of qa.keywords) {
                if (input.includes(keyword)) {
                    return qa;
                }
            }
        }
        
        // Fuzzy matching for common terms
        const commonTerms = {
            'state': ['states covered', 'which states', 'project coverage'],
            'claim': ['types of claims', 'fra types', 'claim types'],
            'contact': ['contact support', 'help desk', 'who to contact'],
            'scheme': ['recommended schemes', 'government schemes', 'css schemes'],
            'map': ['how to use', 'webgis features', 'map layers']
        };
        
        for (let [term, keywords] of Object.entries(commonTerms)) {
            if (input.includes(term)) {
                for (let qa of this.qaList) {
                    if (qa.keywords.some(k => keywords.includes(k))) {
                        return qa;
                    }
                }
            }
        }
        
        return null;
    },
    
    // Get random default response
    getDefaultResponse: function() {
        const randomIndex = Math.floor(Math.random() * this.defaultResponses.length);
        return this.defaultResponses[randomIndex];
    }
};