import os
import json
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import subprocess
import sys

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
app.config['JSON_SORT_KEYS'] = False

# Global variables for ML models
kmeans_model = None
scaler = None
centroids = None
cluster_stats = None
df_with_clusters = None
feature_columns = None
encoded_feature_columns = None
categorical_cols = None

def load_credit_models():
    """Load KMeans model dan data CSV"""
    global kmeans_model, scaler, centroids, cluster_stats, df_with_clusters, feature_columns
    global encoded_feature_columns, categorical_cols
    
    try:
        # Load CSV dengan relative path (support untuk Railway)
        csv_path = os.path.join(os.path.dirname(__file__), 'credit_risk_with_clusters.csv')
        df_with_clusters = pd.read_csv(csv_path)
        
        # Get feature columns (semua except Cluster dan loan_status)
        feature_columns = [col for col in df_with_clusters.columns 
                          if col not in ['Cluster', 'loan_status']]
        
        # Prepare features
        X = df_with_clusters[feature_columns].copy()
        
        # Handle missing values - fill numeric with median, categorical with mode
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        
        for col in numeric_cols:
            X[col] = X[col].fillna(X[col].median())
        
        for col in categorical_cols:
            X[col] = X[col].fillna(X[col].mode()[0] if len(X[col].mode()) > 0 else 'UNKNOWN')
        
        # One-hot encode categorical variables
        X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
        encoded_feature_columns = X_encoded.columns.tolist()
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_encoded)
        
        # Load KMeans model (retrain dari data)
        n_clusters = int(df_with_clusters['Cluster'].max()) + 1
        kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans_model.fit(X_scaled)
        centroids = kmeans_model.cluster_centers_
        
        # Calculate default rate per cluster
        cluster_stats = {}
        for cluster_id in range(n_clusters):
            cluster_mask = df_with_clusters['Cluster'] == cluster_id
            default_rate = df_with_clusters[cluster_mask]['loan_status'].mean()
            cluster_size = cluster_mask.sum()
            cluster_stats[cluster_id] = {
                'default_rate': float(default_rate),
                'size': int(cluster_size),
                'approval_rate': float(1 - default_rate),
                'cluster_id': cluster_id
            }
        
        print("✓ Credit risk models loaded successfully")
        print(f"  - Clusters: {n_clusters}")
        print(f"  - Features: {len(encoded_feature_columns)}")
        print(f"  - Categorical columns: {categorical_cols}")
        return True
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        import traceback
        traceback.print_exc()
        return False

# Load models on startup
load_credit_models()

# Ensure visualizations exist (generate on server if missing)
def ensure_visualizations():
    """Generate visualization images by running `generate_visualizations.py`
    if any expected image is missing. This helps when images are not checked
    into the repo (we intentionally ignore `static/img` locally).
    """
    img_dir = os.path.join(os.path.dirname(__file__), 'static', 'img')
    expected_files = [
        os.path.join(img_dir, 'elbow_method.png'),
        os.path.join(img_dir, 'pca_clusters.png'),
        os.path.join(img_dir, 'cluster_heatmap.png'),
        os.path.join(img_dir, 'cluster_profiles.png'),
    ]

    missing = [p for p in expected_files if not os.path.exists(p)]
    if missing:
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'generate_visualizations.py')
            if os.path.exists(script_path):
                # Run the generator with the same Python interpreter
                subprocess.run([sys.executable, script_path], check=False)
                print("✓ generate_visualizations.py executed (missing images regenerated)")
            else:
                print(f"! generate_visualizations.py not found at {script_path}")
        except Exception as e:
            print(f"Error generating visualizations: {e}")

# Try to ensure visuals now (will run on import when Gunicorn loads the module)
ensure_visualizations()

# In-memory storage untuk demo
contacts = []

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Landing page utama"""
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    """Halaman prediksi kredit"""
    return render_template('predict.html')

@app.route('/results')
def results_page():
    """Halaman hasil prediksi"""
    return render_template('results.html')

@app.route('/about')
def about():
    """Halaman tentang kami"""
    return render_template('about.html')

@app.route('/features')
def features():
    """Halaman fitur"""
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    """Halaman pricing"""
    return render_template('pricing.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validasi
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Semua field harus diisi'
            }), 400
        
        # Simpan contact (demo)
        contact_data = {
            'id': len(contacts) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'message': data.get('message'),
            'created_at': datetime.now().isoformat()
        }
        contacts.append(contact_data)
        
        # Log ke console (production: simpan ke database)
        print(f"New contact: {contact_data}")
        
        return jsonify({
            'success': True,
            'message': 'Pesan Anda telah dikirim! Kami akan menghubungi segera.',
            'data': contact_data
        }), 201
    
    return render_template('contact.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/stats')
def get_stats():
    """API endpoint untuk statistik"""
    stats = {
        'users': 50000,
        'transactions': 2500000,
        'growth': 156,
        'satisfaction': 98,
        'contacts_received': len(contacts)
    }
    return jsonify(stats)

@app.route('/api/testimonials')
def get_testimonials():
    """API endpoint untuk testimonials"""
    testimonials = [
        {
            'id': 1,
            'name': 'Ahmad Rizki',
            'role': 'Entrepreneur',
            'image': 'https://i.pravatar.cc/150?img=1',
            'text': 'Platform terbaik yang pernah saya gunakan. Interface intuitif dan support yang luar biasa responsif.',
            'rating': 5
        },
        {
            'id': 2,
            'name': 'Siti Nurhaliza',
            'role': 'Investor',
            'image': 'https://i.pravatar.cc/150?img=5',
            'text': 'Return on investment yang konsisten. Saya sangat merekomendasikan kepada semua investor muda.',
            'rating': 5
        },
        {
            'id': 3,
            'name': 'Budi Santoso',
            'role': 'Financial Analyst',
            'image': 'https://i.pravatar.cc/150?img=3',
            'text': 'Dashboard analytics sangat detail dan real-time. Membantu saya membuat keputusan investasi lebih baik.',
            'rating': 5
        },
        {
            'id': 4,
            'name': 'Maya Putri',
            'role': 'Student',
            'image': 'https://i.pravatar.cc/150?img=7',
            'text': 'Sempurna untuk pemula! Edukasi finansial yang disediakan sangat lengkap dan mudah dipahami.',
            'rating': 5
        },
        {
            'id': 5,
            'name': 'Rendra Wijaya',
            'role': 'Startup Founder',
            'image': 'https://i.pravatar.cc/150?img=10',
            'text': 'Fitur automation membuat operasional bisnis saya lebih efisien. Definitely game changer!',
            'rating': 5
        }
    ]
    return jsonify(testimonials)

@app.route('/api/sample-data')
def get_sample_data():
    """API endpoint untuk sample data layak & tidak layak"""
    try:
        if df_with_clusters is None:
            return jsonify({'success': False, 'message': 'Data tidak tersedia'}), 500
        
        # Filter approved (loan_status == 0) dan defaulted (loan_status == 1)
        approved = df_with_clusters[df_with_clusters['loan_status'] == 0]
        defaulted = df_with_clusters[df_with_clusters['loan_status'] == 1]
        
        # Sample 3 dari masing-masing
        approved_samples = approved.sample(min(3, len(approved)), random_state=42).to_dict('records')
        defaulted_samples = defaulted.sample(min(3, len(defaulted)), random_state=42).to_dict('records')
        
        return jsonify({
            'success': True,
            'approved': approved_samples,
            'defaulted': defaulted_samples,
            'approved_count': len(approved),
            'defaulted_count': len(defaulted),
            'total_count': len(df_with_clusters)
        })
    except Exception as e:
        print(f"Error in get_sample_data: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict_credit_risk():
    """
    API endpoint untuk prediksi kelayakan kredit
    
    Input: JSON dengan feature values (numeric + categorical)
    Output: JSON dengan prediksi cluster, default rate, dan rekomendasi
    """
    try:
        if kmeans_model is None or scaler is None:
            return jsonify({
                'success': False,
                'message': 'Model belum dimuat'
            }), 500
        
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                'success': False,
                'message': 'Data input kosong'
            }), 400
        
        # Build feature vector
        input_dict = {}
        for col in feature_columns:
            if col in data:
                input_dict[col] = data[col]
            else:
                return jsonify({
                    'success': False,
                    'message': f'Field "{col}" diperlukan'
                }), 400
        
        # Convert ke DataFrame
        input_df = pd.DataFrame([input_dict])
        
        # One-hot encode categorical variables
        input_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)
        
        # Ensure all encoded columns exist
        for col in encoded_feature_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        
        # Reorder columns
        input_encoded = input_encoded[encoded_feature_columns]
        
        # Standardize
        input_scaled = scaler.transform(input_encoded)
        
        # Find nearest cluster
        distances = np.linalg.norm(centroids - input_scaled[0], axis=1)
        nearest_cluster = np.argmin(distances)
        min_distance = distances[nearest_cluster]
        
        # Get cluster statistics
        cluster_info = cluster_stats.get(int(nearest_cluster), {})
        default_rate = cluster_info.get('default_rate', 0)
        approval_rate = cluster_info.get('approval_rate', 1)
        cluster_size = cluster_info.get('size', 0)
        
        # Determine recommendation
        if approval_rate >= 0.7:
            recommendation = "LAYAK"
            risk_level = "RENDAH"
            color = "green"
        elif approval_rate >= 0.5:
            recommendation = "LAYAK (DENGAN PERTIMBANGAN)"
            risk_level = "SEDANG"
            color = "yellow"
        else:
            recommendation = "TIDAK LAYAK"
            risk_level = "TINGGI"
            color = "red"
        
        result = {
            'success': True,
            'prediction': {
                'cluster_id': int(nearest_cluster),
                'distance_to_centroid': float(min_distance),
                'default_rate': float(default_rate),
                'approval_rate': float(approval_rate),
                'cluster_size': int(cluster_size),
                'recommendation': recommendation,
                'risk_level': risk_level,
                'color': color,
                'confidence': float((1 - min_distance / np.max(distances)) * 100) if np.max(distances) > 0 else 0
            },
            'input': data
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error in predict_credit_risk: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/cluster-info')
def get_cluster_info():
    """API endpoint untuk info semua clusters"""
    try:
        if cluster_stats is None:
            return jsonify({'success': False, 'message': 'Data tidak tersedia'}), 500
        
        clusters_info = []
        for cluster_id in sorted(cluster_stats.keys()):
            info = cluster_stats[cluster_id]
            clusters_info.append({
                'id': cluster_id,
                'default_rate': info['default_rate'],
                'approval_rate': info['approval_rate'],
                'size': info['size'],
                'percentage': float(info['size'] / len(df_with_clusters) * 100)
            })
        
        return jsonify({
            'success': True,
            'clusters': clusters_info,
            'total_records': len(df_with_clusters)
        }), 200
    except Exception as e:
        print(f"Error in get_cluster_info: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 error"""
    return render_template('500.html'), 500

@app.before_request
def before_request():
    """Before request hook"""
    pass

@app.after_request
def after_request(response):
    """After request hook - tambah security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
