import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Set style - SAMA PERSIS SEPERTI TA10.ipynb
sns.set(style="whitegrid")

# Base path (script directory) and create images directory if not exists
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, 'static', 'img')
os.makedirs(IMG_DIR, exist_ok=True)

# Load data - SAMA PERSIS SEPERTI TA10.ipynb
csv_path = os.path.join(BASE_DIR, 'credit_risk_dataset.csv')
df = pd.read_csv(csv_path)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# ===== STEP 1: Kalau ada kolom target, drop (unsupervised) - SAMA DENGAN CELL #VSC-d39047d7 =====
target_cols = [c for c in df.columns if c.lower() in ["loan_status", "target", "default", "y"]]
print("Detected target columns:", target_cols)

X = df.drop(columns=target_cols) if len(target_cols) > 0 else df.copy()
print("Feature shape:", X.shape)

# ===== STEP 2: Pisahkan numeric vs categorical - SAMA DENGAN CELL #VSC-5c284c82 =====
num_cols = X.select_dtypes(include=np.number).columns
cat_cols = X.select_dtypes(exclude=np.number).columns

print("Numeric cols:", list(num_cols))
print("Categorical cols:", list(cat_cols))

# Isi missing numeric dengan median
for c in num_cols:
    X[c] = X[c].fillna(X[c].median())

# Isi missing categorical dengan modus
for c in cat_cols:
    X[c] = X[c].fillna(X[c].mode()[0])

# ===== STEP 3: One-Hot Encoding - SAMA DENGAN CELL #VSC-e5ac055c =====
X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)
print("Shape after encoding:", X_encoded.shape)

# ===== STEP 4: Scale - SAMA DENGAN CELL #VSC-91c29286 =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

# ===== VISUALIZATION 1: Elbow Method - SAMA DENGAN CELL #VSC-0d046bff =====
print("\n--- Generating Elbow Method (CELL #VSC-0d046bff) ---")
wcss = []
K_range = range(1, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init="auto")
    km.fit(X_scaled)
    wcss.append(km.inertia_)

plt.figure(figsize=(8,5))
plt.plot(K_range, wcss, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of clusters (k)")
plt.ylabel("WCSS / Inertia")
plt.xticks(K_range)
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'elbow_method.png'), bbox_inches='tight')
plt.close()
print("✓ Saved: static/img/elbow_method.png")

# ===== STEP 5: KMeans optimal_k=4 - SAMA DENGAN CELL #VSC-c2d6a157 =====
print("\n--- Running KMeans with k=4 (CELL #VSC-c2d6a157) ---")
optimal_k = 4  # ganti sesuai elbow kamu
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
clusters = kmeans.fit_predict(X_scaled)

df["Cluster"] = clusters
print(df["Cluster"].value_counts().sort_index())

# ===== VISUALIZATION 2: PCA 2D Clusters - SAMA DENGAN CELL #VSC-99942488 =====
print("\n--- Generating PCA 2D Clusters (CELL #VSC-99942488) ---")
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=clusters, palette="bright", alpha=0.7)
plt.title("KMeans Clusters (PCA 2D)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'pca_clusters.png'), bbox_inches='tight')
plt.close()
print("✓ Saved: static/img/pca_clusters.png")

# ===== STEP 6: Cluster Profile - SAMA DENGAN CELL #VSC-e0569166 =====
print("\n--- Computing Cluster Profiles (CELL #VSC-e0569166) ---")
cluster_profile = df.groupby("Cluster").mean(numeric_only=True)
print(cluster_profile)

# ===== VISUALIZATION 3: Cluster Heatmap - SAMA DENGAN CELL #VSC-b6fef279 =====
print("\n--- Generating Cluster Heatmap (CELL #VSC-b6fef279) ---")
plt.figure(figsize=(14,6))
sns.heatmap(cluster_profile.T, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("Cluster Feature Means (Heatmap)")
plt.ylabel("Features")
plt.xlabel("Cluster")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'cluster_heatmap.png'), bbox_inches='tight')
plt.close()
print("✓ Saved: static/img/cluster_heatmap.png")

# ===== VISUALIZATION 4: Cluster Profiles for Key Features - SAMA DENGAN CELL #VSC-d8086cfe =====
print("\n--- Generating Cluster Profiles Bar Chart (CELL #VSC-d8086cfe) ---")
key_features = [c for c in ["person_income","loan_amnt","loan_int_rate",
                           "loan_percent_income","person_age","cb_person_cred_hist_length"]
                if c in df.columns]

print("Key features used:", key_features)

cluster_profile[key_features].plot(kind="bar", figsize=(10,6))
plt.title("Cluster Profiles for Key Features")
plt.ylabel("Mean Value")
plt.xlabel("Cluster")
plt.xticks(rotation=0)
plt.legend(title="Feature")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'cluster_profiles.png'), bbox_inches='tight')
plt.close()
print("✓ Saved: static/img/cluster_profiles.png")

# ===== SAVE DATA WITH CLUSTERS - SAMA DENGAN CELL #VSC-becc9c73 =====
print("\n--- Saving data with clusters (CELL #VSC-becc9c73) ---")
df.to_csv("credit_risk_with_clusters.csv", index=False)
print("Saved: credit_risk_with_clusters.csv")

print("\n✅ ALL VISUALIZATIONS GENERATED - LOGIC 100% SAMA DENGAN TA10.ipynb")
