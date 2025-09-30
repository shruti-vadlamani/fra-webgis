#!/usr/bin/env python3
"""
FRA WebGIS Integration Application
Comprehensive Forest Rights Act (IFR/CFR/CR) management system
"""

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import random

try:
    import psycopg2  # type: ignore
except Exception:
    psycopg2 = None

app = Flask(__name__)

# Configuration
FRA_GEOJSON_FILE = 'output/telangana_fra_realistic.geojson'
FRA_ANALYTICS_FILE = 'output/fra_analytics.json'
VANACHITRA_FRA_FILE = 'output/telangana_fra_realistic.geojson'
POLY_ATTR_JSON = 'output/polygon_attributes.json'
SCHEMES_FILE = os.path.join('static', 'schemes.json')
STATIC_DIR = 'static'
TEMPLATES_DIR = 'templates'
REACT_BUILD_DIR = 'react_build'

class FRAWebGISManager:
    def __init__(self, geojson_file, analytics_file):
        self.geojson_file = geojson_file
        self.analytics_file = analytics_file
        self.claims_data = None
        self.analytics_data = None
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load FRA claims and analytics data."""
        try:
            # Load claims data
            with open(self.geojson_file, 'r') as f:
                self.claims_data = json.load(f)
            
            # Load analytics data
            with open(self.analytics_file, 'r') as f:
                self.analytics_data = json.load(f)
            
            # Convert to DataFrame for easier processing
            features = []
            for feature in self.claims_data['features']:
                props = feature['properties'].copy()
                props['geometry'] = feature['geometry']
                features.append(props)
            
            self.df = pd.DataFrame(features)
            print(f"Loaded {len(self.df)} FRA claims")
            
        except Exception as e:
            print(f"Error loading FRA data: {e}")
            self.claims_data = {"type": "FeatureCollection", "features": []}
            self.analytics_data = {}
            self.df = pd.DataFrame()
    
    def get_filtered_claims(self, filters=None):
        """Get filtered FRA claims based on provided filters."""
        if self.df is None or len(self.df) == 0:
            return {"type": "FeatureCollection", "features": []}
        
        filtered_df = self.df.copy()
        
        if filters:
            # Apply filters
            if 'state' in filters and filters['state']:
                filtered_df = filtered_df[filtered_df['state'] == filters['state']]
            
            if 'district' in filters and filters['district']:
                filtered_df = filtered_df[filtered_df['district'] == filters['district']]
            
            if 'village' in filters and filters['village']:
                filtered_df = filtered_df[filtered_df['village'] == filters['village']]
            
            if 'fra_type' in filters and filters['fra_type']:
                filtered_df = filtered_df[filtered_df['fra_type'] == filters['fra_type']]
            
            if 'status' in filters and filters['status']:
                filtered_df = filtered_df[filtered_df['status'] == filters['status']]
            
            if 'tribal_community' in filters and filters['tribal_community']:
                filtered_df = filtered_df[filtered_df['tribal_community'] == filters['tribal_community']]
            
            if 'claim_area_min' in filters and filters['claim_area_min']:
                min_area = float(filters['claim_area_min'])
                filtered_df = filtered_df[filtered_df['claim_area_ha'] >= min_area]
            
            if 'claim_area_max' in filters and filters['claim_area_max']:
                max_area = float(filters['claim_area_max'])
                filtered_df = filtered_df[filtered_df['claim_area_ha'] <= max_area]
        
        # Convert back to GeoJSON format
        features = []
        for _, row in filtered_df.iterrows():
            # Clean properties to handle NaN values
            properties = {}
            for k, v in row.items():
                if k != 'geometry':
                    try:
                        if pd.isna(v):
                            properties[k] = None
                        elif isinstance(v, (np.integer, np.floating)):
                            if np.isnan(v):
                                properties[k] = None
                            else:
                                properties[k] = float(v) if isinstance(v, np.floating) else int(v)
                        else:
                            properties[k] = v
                    except (TypeError, ValueError):
                        # Handle any other conversion issues
                        properties[k] = str(v) if v is not None else None
            
            feature = {
                "type": "Feature",
                "properties": properties,
                "geometry": row['geometry']
            }
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "properties": {
                "total_claims": len(features),
                "filters_applied": filters or {}
            }
        }
    
    def get_analytics(self):
        """Get comprehensive FRA analytics."""
        try:
            # Ensure all data is JSON serializable
            import json
            json.dumps(self.analytics_data)  # Test if it's serializable
            return self.analytics_data
        except (TypeError, ValueError) as e:
            print(f"Analytics data not JSON serializable: {e}")
            # Return a simplified version
            return {
                "summary": {
                    "total_claims": len(self.df) if self.df is not None else 0,
                    "claims_by_type": self.df['fra_type'].value_counts().to_dict() if self.df is not None and len(self.df) > 0 else {},
                    "claims_by_status": self.df['status'].value_counts().to_dict() if self.df is not None and len(self.df) > 0 else {},
                    "claims_by_state": self.df['state'].value_counts().to_dict() if self.df is not None and len(self.df) > 0 else {}
                },
                "error": "Analytics data simplified due to serialization issues"
            }
    
    def get_claim_details(self, claim_id):
        """Get detailed information for a specific claim."""
        if self.df is None or len(self.df) == 0:
            return None
        
        claim = self.df[self.df['claim_id'] == claim_id]
        if len(claim) == 0:
            return None
        
        return claim.iloc[0].to_dict()

    def get_claim_by_polygon_id(self, polygon_id):
        """Lookup a feature by its claim_id/feature_id/fra_id for DSS."""
        if self.df is None or len(self.df) == 0:
            return None
        candidates = self.df[(self.df['claim_id'] == polygon_id) |
                             (self.df.get('feature_id') == polygon_id) |
                             (self.df.get('fra_id') == polygon_id)]
        if len(candidates) == 0:
            return None
        return candidates.iloc[0].to_dict()


def dss_rules_engine(attrs):
    """Return list of recommended schemes based on attribute thresholds and state."""
    recs = []
    # Note: state-specific additions handled by caller providing claim props via closure or separate logic
    # We keep this function generic and enrich later where we have state
    if attrs.get('forest_cover_percentage') is not None and attrs['forest_cover_percentage'] > 40:
        recs.extend(['CAMPA', 'Green India Mission'])
    if (attrs.get('water_level') is not None and attrs['water_level'] < 80) or \
       (attrs.get('groundwater_index') is not None and attrs['groundwater_index'] < 0.5):
        recs.extend(['PMKSY', 'Jal Jeevan Mission'])
    if attrs.get('soil_quality') == 'Poor':
        recs.extend(['Soil Health Card Scheme', 'Organic Farming Mission'])
    if attrs.get('poverty_index') is not None and attrs['poverty_index'] > 0.6:
        recs.append('MGNREGA')
    if attrs.get('crop_yield') is not None and attrs['crop_yield'] < 10:
        recs.extend(['PM-KISAN', 'Bhavantar Bhugtan'])
    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for r in recs:
        if r not in seen:
            seen.add(r)
            ordered.append(r)
    return ordered


def load_polygon_attributes_from_db(polygon_id):
    db_url = os.getenv('DATABASE_URL')
    if not db_url or psycopg2 is None:
        return None
    try:
        conn = psycopg2.connect(db_url)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT water_level, groundwater_index, soil_quality, crop_yield, forest_cover_percentage, poverty_index, infra_index FROM polygon_attributes WHERE polygon_id=%s",
                (polygon_id,)
            )
            row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {
            'water_level': row[0],
            'groundwater_index': float(row[1]) if row[1] is not None else None,
            'soil_quality': row[2],
            'crop_yield': float(row[3]) if row[3] is not None else None,
            'forest_cover_percentage': float(row[4]) if row[4] is not None else None,
            'poverty_index': float(row[5]) if row[5] is not None else None,
            'infra_index': float(row[6]) if row[6] is not None else None,
        }
    except Exception:
        return None


def load_polygon_attributes_from_json(polygon_id):
    if not os.path.exists(POLY_ATTR_JSON):
        return None
    try:
        with open(POLY_ATTR_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('items', {}).get(polygon_id)
    except Exception:
        return None


def load_all_schemes():
    try:
        with open(SCHEMES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def filter_applicable_schemes(claim_props, attrs):
    """Filter central and state schemes by geography and sector relevance."""
    state = claim_props.get('state')
    fra_type = claim_props.get('fra_type') or claim_props.get('feature_type') or claim_props.get('claim_type')
    sectors = set()
    # Determine sectors from fra_type and attributes
    if fra_type in ('Community Forest Resource Rights', 'Community Rights'):
        sectors.add('Forest')
        sectors.add('Tribal Welfare')
    if fra_type in ('Individual Forest Rights', 'Agriculture'):
        sectors.add('Agriculture')
    if fra_type in ('Water Body',):
        sectors.add('Water')
    # Attribute driven sectors
    if attrs.get('forest_cover_percentage', 0) > 30:
        sectors.add('Forest')
    if attrs.get('water_level', 999) < 100 or (attrs.get('groundwater_index') or 0) < 0.6:
        sectors.add('Water')

    schemes = load_all_schemes()
    applicable = []
    for s in schemes:
        geo = s.get('geography', [])
        if 'All-India' in geo or (state and state in geo):
            if sectors.intersection(set(s.get('sectors', []))):
                applicable.append(s)
    return applicable
    
    def get_state_wise_summary(self):
        """Get state-wise summary of FRA claims."""
        if self.df is None or len(self.df) == 0:
            return {}
        
        state_summary = self.df.groupby('state').agg({
            'claim_id': 'count',
            'claim_area_ha': 'sum',
            'status': lambda x: (x == 'approved').sum(),
            'fra_type': lambda x: x.value_counts().to_dict()
        }).rename(columns={
            'claim_id': 'total_claims',
            'status': 'approved_claims'
        })
        
        return state_summary.to_dict('index')
    
    def get_tribal_community_analysis(self):
        """Get analysis by tribal community."""
        if self.df is None or len(self.df) == 0:
            return {}
        
        tribal_analysis = self.df.groupby('tribal_community').agg({
            'claim_id': 'count',
            'claim_area_ha': 'sum',
            'status': lambda x: (x == 'approved').sum(),
            'fra_type': lambda x: x.value_counts().to_dict()
        }).rename(columns={
            'claim_id': 'total_claims',
            'status': 'approved_claims'
        })
        
        return tribal_analysis.to_dict('index')
    
    def get_timeline_analysis(self):
        """Get timeline analysis of FRA claims."""
        if self.df is None or len(self.df) == 0:
            return {}
        
        # Convert submission_date to datetime
        self.df['submission_date'] = pd.to_datetime(self.df['submission_date'])
        self.df['submission_year'] = self.df['submission_date'].dt.year
        self.df['submission_month'] = self.df['submission_date'].dt.month
        
        # Yearly analysis
        yearly = self.df.groupby('submission_year').agg({
            'claim_id': 'count',
            'claim_area_ha': 'sum',
            'status': lambda x: (x == 'approved').sum()
        }).rename(columns={
            'claim_id': 'claims_submitted',
            'status': 'claims_approved'
        })
        
        # Monthly analysis for current year
        current_year = datetime.now().year
        monthly = self.df[self.df['submission_year'] == current_year].groupby('submission_month').agg({
            'claim_id': 'count',
            'claim_area_ha': 'sum'
        }).rename(columns={'claim_id': 'claims_submitted'})
        
        return {
            'yearly': yearly.to_dict('index'),
            'monthly': monthly.to_dict('index')
        }
    
    def get_performance_metrics(self):
        """Get performance metrics for FRA implementation."""
        if self.df is None or len(self.df) == 0:
            return {}
        
        total_claims = len(self.df)
        approved_claims = len(self.df[self.df['status'] == 'approved'])
        pending_claims = len(self.df[self.df['status'].isin(['submitted', 'under_review', 'field_verification'])])
        
        return {
            'total_claims': total_claims,
            'approved_claims': approved_claims,
            'pending_claims': pending_claims,
            'rejected_claims': len(self.df[self.df['status'] == 'rejected']),
            'approval_rate': round(approved_claims / total_claims * 100, 2) if total_claims > 0 else 0,
            'pending_rate': round(pending_claims / total_claims * 100, 2) if total_claims > 0 else 0,
            'total_area_ha': round(self.df['claim_area_ha'].sum(), 2),
            'average_claim_size_ha': round(self.df['claim_area_ha'].mean(), 2),
            'field_verification_rate': round(len(self.df[self.df['field_verification_done']]) / total_claims * 100, 2) if total_claims > 0 else 0,
            'gps_verification_rate': round(len(self.df[self.df['gps_coordinates_verified']]) / total_claims * 100, 2) if total_claims > 0 else 0
        }

# Initialize FRA manager
fra_manager = FRAWebGISManager(FRA_GEOJSON_FILE, FRA_ANALYTICS_FILE)

@app.route('/')
def index():
    """Serve the React frontend (Vanachitra.AI landing page)."""
    return send_file(os.path.join(REACT_BUILD_DIR, 'index.html'))


@app.route('/gee')
def vanachitra_gee():
    """Google Earth Engine-style Telangana Land-use WebGIS interface."""
    return render_template('vanachitra_gee.html')

@app.route('/dss/<polygon_id>')
def dss_details(polygon_id):
    """Decision Support System: show attributes and recommendations for a polygon."""
    # Load polygon properties from FRA dataset
    claim = fra_manager.get_claim_details(polygon_id) or fra_manager.get_claim_by_polygon_id(polygon_id)
    if not claim:
        # Try scanning the raw GeoJSON for non-tabular ids
        try:
            with open(VANACHITRA_FRA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for feat in data.get('features', []):
                props = feat.get('properties', {})
                if polygon_id in (
                    props.get('claim_id'), props.get('feature_id'), props.get('fra_id'), props.get('id')
                ):
                    claim = props
                    break
        except Exception:
            claim = None

    if not claim:
        return jsonify({'error': 'Polygon not found'}), 404

    # Load attributes from DB or JSON fallback
    attrs = load_polygon_attributes_from_db(polygon_id) or load_polygon_attributes_from_json(polygon_id)

    # If still missing, generate deterministic synthetic attributes (seeded by polygon id)
    if not attrs:
        pid_seed = sum(ord(c) for c in str(polygon_id))
        rng = random.Random(pid_seed)
        soil_quality = rng.choice(['Poor', 'Moderate', 'Good'])
        attrs = {
            'water_level': rng.randint(50, 200),
            'groundwater_index': round(rng.uniform(0.3, 0.9), 2),
            'soil_quality': soil_quality,
            'crop_yield': round(rng.uniform(5, 25), 1),
            'forest_cover_percentage': round(rng.uniform(20, 80), 1),
            'poverty_index': round(rng.uniform(0, 1), 2),
            'infra_index': round(rng.uniform(0, 1), 2)
        }

    recommendations = dss_rules_engine(attrs)
    applicable_schemes = filter_applicable_schemes(claim, attrs)
    # Enrich recommendations with state-specific where applicable
    state = claim.get('state')
    if attrs.get('forest_cover_percentage', 0) > 40 and state == 'Odisha' and 'Ama Jungle Yojana' not in recommendations:
        recommendations.append('Ama Jungle Yojana')
    if ((attrs.get('water_level') or 999) < 80 or (attrs.get('groundwater_index') or 1) < 0.5) and state == 'Telangana' and 'Mission Kakatiya' not in recommendations:
        recommendations.append('Mission Kakatiya')
    if (attrs.get('poverty_index') or 0) > 0.6:
        if state == 'Odisha' and 'KALIA' not in recommendations:
            recommendations.append('KALIA')
        if state == 'Telangana' and 'Rythu Bandhu' not in recommendations:
            recommendations.append('Rythu Bandhu')
    # Prefer community-based schemes for community polygons
    fra_type = claim.get('fra_type') or claim.get('feature_type') or claim.get('claim_type')
    if fra_type in ('Community Forest Resource Rights', 'Community Rights', 'CFR', 'CR'):
        for name in ['OFSDP', 'Van Dhan Vikas Yojana', 'Mission Kakatiya']:
            if name not in recommendations:
                recommendations.append(name)

    # Always render the HTML template (no JSON responses)
    # Render dashboard
    return render_template('dss_details.html',
                           polygon_id=polygon_id,
                           attrs=attrs,
                           recs=recommendations,
                           schemes=applicable_schemes,
                           meta={
                               'fra_type': claim.get('fra_type') or claim.get('feature_type') or claim.get('claim_type'),
                               'state': claim.get('state'),
                               'district': claim.get('district'),
                               'village': claim.get('village'),
                               'households': claim.get('total_households') or claim.get('beneficiary_households'),
                               'area_hectares': claim.get('area_claimed') or claim.get('area_hectares')
                           })

@app.route('/api/vanachitra_fra_data')
def api_vanachitra_fra_data():
    """Serve Vanachitra.AI FRA data as GeoJSON."""
    try:
        if not os.path.exists(VANACHITRA_FRA_FILE):
            return jsonify({'error': 'Vanachitra FRA data not found. Please generate it first.'}), 404
        
        with open(VANACHITRA_FRA_FILE, 'r') as f:
            data = json.load(f)
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telangana_fra_constrained')
def api_telangana_fra_constrained():
    """Serve Telangana FRA data placed at specific forest coordinates as GeoJSON."""
    try:
        # Use the new realistic FRA data with proper sizing
        telangana_fra_file = 'output/telangana_fra_realistic.geojson'
        
        # Fallback to coordinate-based version
        if not os.path.exists(telangana_fra_file):
            telangana_fra_file = 'output/telangana_fra_coordinates.geojson'
        
        # Fallback to forest-only version if coordinates version doesn't exist
        if not os.path.exists(telangana_fra_file):
            telangana_fra_file = 'output/telangana_fra_forest_only.geojson'
        
        # Final fallback to older version
        if not os.path.exists(telangana_fra_file):
            telangana_fra_file = 'output/telangana_fra_forest_constrained.geojson'
        
        if not os.path.exists(telangana_fra_file):
            return jsonify({'error': 'Telangana FRA data not found. Please generate it first.'}), 404
        
        with open(telangana_fra_file, 'r') as f:
            data = json.load(f)
        
        print(f"Serving FRA data: {telangana_fra_file} with {len(data.get('features', []))} parcels")
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assets')
def get_assets():
    """API endpoint to get asset data."""
    try:
        # Try to load enhanced assets first, fallback to original
        assets_files = ['output/assets_enhanced.geojson', 'output/assets.geojson']
        assets_data = None
        
        for assets_file in assets_files:
            try:
                with open(assets_file, 'r') as f:
                    assets_data = json.load(f)
                print(f"Loaded assets from {assets_file}")
                break
            except FileNotFoundError:
                continue
        
        if assets_data is None:
            raise FileNotFoundError("No assets file found")
            
        # Add filtering based on query parameters
        filters = {
            'asset_type': request.args.get('asset_type'),
            'state': request.args.get('state'),
            'min_area': request.args.get('min_area'),
            'max_area': request.args.get('max_area')
        }
        
        # Apply filters if provided
        if any(filters.values()):
            filtered_features = []
            for feature in assets_data['features']:
                props = feature['properties']
                
                # Asset type filter
                if filters['asset_type'] and props.get('class') != filters['asset_type']:
                    continue
                
                # State filter
                if filters['state'] and props.get('state') != filters['state']:
                    continue
                
                # Area filters
                area = props.get('area_km2', 0)
                if filters['min_area'] and area < float(filters['min_area']):
                    continue
                if filters['max_area'] and area > float(filters['max_area']):
                    continue
                
                filtered_features.append(feature)
            
            assets_data['features'] = filtered_features
        
        return jsonify(assets_data)
    except Exception as e:
        return jsonify({
            'error': f'Error loading assets: {str(e)}',
            'type': 'FeatureCollection',
            'features': []
        }), 500

@app.route('/api/fra-claims')  
def get_fra_claims():
    """API endpoint to get FRA claims data."""
    try:
        # Get filters from query parameters
        filters = {
            'state': request.args.get('state'),
            'district': request.args.get('district'),
            'village': request.args.get('village'),
            'fra_type': request.args.get('fra_type'),
            'status': request.args.get('status'),
            'tribal_community': request.args.get('tribal_community'),
            'claim_area_min': request.args.get('claim_area_min'),
            'claim_area_max': request.args.get('claim_area_max')
        }
        
        # Remove empty filters
        filters = {k: v for k, v in filters.items() if v}
        
        data = fra_manager.get_filtered_claims(filters)
        return jsonify(data)
    
    except Exception as e:
        return jsonify({
            'error': f'Error loading FRA claims: {str(e)}',
            'type': 'FeatureCollection',
            'features': []
        }), 500

@app.route('/test')
def test_page():
    """Serve the test page."""
    return send_from_directory('.', 'test_fra_webgis.html')

@app.route('/chatbot-test')
def chatbot_test():
    """Serve the chatbot test page."""
    return render_template('chatbot_test.html')

@app.route('/api/claims')
def get_claims():
    """API endpoint to get filtered FRA claims (legacy endpoint)."""
    return get_fra_claims()

@app.route('/api/analytics')
def get_analytics():
    """API endpoint to get FRA analytics."""
    try:
        analytics = fra_manager.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/claim/<claim_id>')
def get_claim_details(claim_id):
    """API endpoint to get detailed claim information."""
    try:
        claim_details = fra_manager.get_claim_details(claim_id)
        if claim_details is None:
            return jsonify({'error': 'Claim not found'}), 404
        return jsonify(claim_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/state-summary')
def get_state_summary():
    """API endpoint to get state-wise summary."""
    try:
        summary = fra_manager.get_state_wise_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tribal-analysis')
def get_tribal_analysis():
    """API endpoint to get tribal community analysis."""
    try:
        analysis = fra_manager.get_tribal_community_analysis()
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline')
def get_timeline_analysis():
    """API endpoint to get timeline analysis."""
    try:
        timeline = fra_manager.get_timeline_analysis()
        return jsonify(timeline)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance')
def get_performance_metrics():
    """API endpoint to get performance metrics."""
    try:
        metrics = fra_manager.get_performance_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filter-options')
def get_filter_options():
    """API endpoint to get available filter options."""
    try:
        if fra_manager.df is None or len(fra_manager.df) == 0:
            return jsonify({})
        
        options = {
            'states': sorted(fra_manager.df['state'].unique().tolist()),
            'districts': sorted(fra_manager.df['district'].unique().tolist()),
            'villages': sorted(fra_manager.df['village'].unique().tolist()),
            'fra_types': sorted(fra_manager.df['fra_type'].unique().tolist()),
            'statuses': sorted(fra_manager.df['status'].unique().tolist()),
            'tribal_communities': sorted(fra_manager.df['tribal_community'].unique().tolist())
        }
        
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def export_claims():
    """API endpoint to export filtered claims data."""
    try:
        # Get filters from query parameters
        filters = {
            'state': request.args.get('state'),
            'district': request.args.get('district'),
            'village': request.args.get('village'),
            'fra_type': request.args.get('fra_type'),
            'status': request.args.get('status'),
            'tribal_community': request.args.get('tribal_community'),
            'claim_area_min': request.args.get('claim_area_min'),
            'claim_area_max': request.args.get('claim_area_max')
        }
        
        # Remove empty filters
        filters = {k: v for k, v in filters.items() if v}
        
        data = fra_manager.get_filtered_claims(filters)
        
        # Add export metadata
        data['export_info'] = {
            'exported_at': datetime.now().isoformat(),
            'filters_applied': filters,
            'total_claims': len(data['features'])
        }
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/landuse_data/<state>')
def get_state_landuse(state):
    """API endpoint to get land-use dummy data for any state."""
    try:
        # Map state names to file names
        state_files = {
            'telangana': 'output/telangana_landuse_dummy.geojson',
            'odisha': 'output/odisha_landuse_dummy.geojson',
            'madhya pradesh': 'output/madhya_pradesh_landuse_dummy.geojson',
            'tripura': 'output/tripura_landuse_dummy.geojson'
        }
        
        state_lower = state.lower()
        landuse_file = state_files.get(state_lower)
        
        if not landuse_file:
            return jsonify({
                'error': f'Land-use data not available for {state}',
                'available_states': list(state_files.keys())
            }), 404
        
        if not os.path.exists(landuse_file):
            return jsonify({
                'error': f'{state.title()} land-use data not found. Please generate it first.',
                'suggestion': f'Run: python scripts/generate_multi_state_landuse.py'
            }), 404
        
        with open(landuse_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add filtering based on query parameters
        filters = {
            'landuse_type': request.args.get('landuse_type'),
            'district': request.args.get('district'),
            'min_area': request.args.get('min_area'),
            'max_area': request.args.get('max_area')
        }
        
        # Apply filters if provided
        if any(filters.values()):
            filtered_features = []
            for feature in data['features']:
                props = feature['properties']
                
                # Land-use type filter
                if filters['landuse_type'] and props.get('landuse_type') != filters['landuse_type']:
                    continue
                
                # District filter
                if filters['district'] and props.get('district') != filters['district']:
                    continue
                
                # Area filters
                area = props.get('area_km2', 0)
                if filters['min_area'] and area < float(filters['min_area']):
                    continue
                if filters['max_area'] and area > float(filters['max_area']):
                    continue
                
                filtered_features.append(feature)
            
            data['features'] = filtered_features
            data['properties']['filtered_features'] = len(filtered_features)
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({
            'error': f'Error loading {state} land-use data: {str(e)}',
            'type': 'FeatureCollection',
            'features': []
        }), 500

# Keep the old endpoint for backward compatibility
@app.route('/api/telangana_landuse_dummy')
def get_telangana_landuse():
    """API endpoint to get Telangana land-use dummy data (backward compatibility)."""
    return get_state_landuse('telangana')

@app.route('/api/telangana_landuse_categories')
def get_telangana_landuse_categories():
    """API endpoint to get land-use categories for legend."""
    try:
        categories_file = 'output/telangana_landuse_categories.json'
        
        if not os.path.exists(categories_file):
            return jsonify({'error': 'Categories file not found'}), 404
        
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        return jsonify(categories)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telangana_forest')
def get_telangana_forest():
    """API endpoint to get actual Telangana forest boundaries."""
    try:
        # Use the dense forest leaflet file optimized for web display
        forest_file = 'dense_forest_leaflet.geojson'
        
        if not os.path.exists(forest_file):
            return jsonify({'error': 'Dense forest data not found'}), 404
        
        with open(forest_file, 'r', encoding='utf-8') as f:
            forest_data = json.load(f)
        
        print(f"Serving dense forest data with {len(forest_data.get('features', []))} features")
        return jsonify(forest_data)
    
    except Exception as e:
        print(f"Error loading forest data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/boundaries/<state>')
def get_state_boundaries(state):
    """API endpoint to get state and district boundaries."""
    try:
        state_lower = state.lower()
        
        # Map state names to available boundary files
        boundary_files = {
            'telangana': {
                'districts': os.path.join(os.path.dirname(__file__), 'telangana_districts_33.geojson'),
                'blocks': os.path.join(os.path.dirname(__file__), 'telangana/blocks.json')
            }
        }
        
        if state_lower not in boundary_files:
            return jsonify({
                'error': f'Boundary data not available for {state}',
                'available_states': list(boundary_files.keys())
            }), 404
        
        result = {}
        
        # Load district boundaries
        districts_file = boundary_files[state_lower]['districts']
        if os.path.exists(districts_file):
            with open(districts_file, 'r', encoding='utf-8') as f:
                districts_data = json.load(f)
            result['districts'] = districts_data
        
        # Load blocks if requested
        if request.args.get('include_blocks') == 'true':
            blocks_file = boundary_files[state_lower]['blocks']
            if os.path.exists(blocks_file):
                with open(blocks_file, 'r', encoding='utf-8') as f:
                    blocks_data = json.load(f)
                result['blocks'] = blocks_data
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/districts/<state>')
def get_state_districts(state):
    """API endpoint to get list of districts for a state."""
    try:
        state_lower = state.lower()
        
        if state_lower == 'telangana':
            districts_file = 'telangana_districts_33.geojson'
            if os.path.exists(districts_file):
                with open(districts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract district names
                districts = []
                for feature in data['features']:
                    district_name = feature['properties'].get('DISTRICT_N', '')
                    if district_name:
                        districts.append(district_name.title())
                
                return jsonify({
                    'state': state.title(),
                    'districts': sorted(districts)
                })
        
        # For other states, return hardcoded lists for demo
        state_districts = {
            'odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh'],
            'madhya pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha'],
            'tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura']
        }
        
        districts = state_districts.get(state_lower, [])
        return jsonify({
            'state': state.title(),
            'districts': districts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, filename)

# Serve React static files
@app.route('/static/css/<path:filename>')
def serve_react_css(filename):
    """Serve React CSS files."""
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'static', 'css'), filename)

@app.route('/static/js/<path:filename>')
def serve_react_js(filename):
    """Serve React JS files."""
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'static', 'js'), filename)

@app.route('/images/<path:filename>')
def serve_react_images(filename):
    """Serve React image files."""
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'images'), filename)

# Fallback for React Router (SPA routing)
@app.route('/upload')
def react_upload():
    """Serve React app for /upload route."""
    return send_file(os.path.join(REACT_BUILD_DIR, 'index.html'))

@app.route('/fra-claims')
def react_fra_claims():
    """Serve React app for /fra-claims route."""
    return send_file(os.path.join(REACT_BUILD_DIR, 'index.html'))

if __name__ == '__main__':
    print("=== FRA WebGIS Integration Application ===")
    print("Starting FRA WebGIS server...")
    print("Open your browser to: http://127.0.0.1:5001")
    print("Press Ctrl+C to stop the server\n")
    
    # Check if output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')
        print("Created output directory")
    
    # Check if templates directory exists
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        print("Created templates directory")
    
    # Check if static directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
        print("Created static directory")
    
    # Generate FRA data if it doesn't exist
    if not os.path.exists(FRA_GEOJSON_FILE):
        print("Generating FRA data...")
        os.system('python scripts/fra_webgis_generator.py')
    
    app.run(debug=True, host='127.0.0.1', port=5001)
