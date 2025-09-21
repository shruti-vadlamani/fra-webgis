import rasterio
from rasterio import features
import numpy as np
from scipy import ndimage
import json
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

# ---------- CONFIG ----------
input_raster = "Telangana_Forest.tif"
output_geojson = "dense_forest_leaflet.geojson"
cluster_size_threshold = 50  # min pixels to be considered a forest patch
# ----------------------------

# Step 1: Read raster
with rasterio.open(input_raster) as src:
    band = src.read(1)
    transform = src.transform

# Step 2: Mask forest pixels (assume white > 0 is forest)
forest_mask = band > 0

# Step 3: Label connected components (clusters)
labeled, num_features = ndimage.label(forest_mask)
sizes = ndimage.sum(forest_mask, labeled, range(num_features + 1))

# Step 4: Keep only clusters bigger than threshold
mask_size = sizes > cluster_size_threshold
dense_mask = mask_size[labeled]

# Step 5: Polygonize dense clusters
polygons = []
for geom, value in features.shapes(dense_mask.astype(np.int16), transform=transform):
    if value == 1:
        polygons.append(shape(geom))

# Step 6: Merge all polygons into fewer larger polygons to reduce GeoJSON size
if polygons:
    merged = unary_union(polygons)
    # Ensure we always have a list of polygons
    if merged.geom_type == "Polygon":
        merged = [merged]
    else:
        merged = list(merged.geoms)
else:
    merged = []

# Step 7: Prepare GeoJSON
geojson_features = []
for poly in merged:
    geojson_features.append({
        "type": "Feature",
        "geometry": mapping(poly),
        "properties": {}
    })

geojson = {
    "type": "FeatureCollection",
    "features": geojson_features
}

# Step 8: Save to file
with open(output_geojson, "w") as f:
    json.dump(geojson, f)

print(f"Dense forest GeoJSON saved to {output_geojson} with {len(geojson_features)} features")
