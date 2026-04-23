import cv2
import ezdxf


def chaikin_smoothing(points, iterations=2):
    if len(points) < 3:
        return points

    smoothed = points[:]
    for _ in range(iterations):
        new_points = []
        count = len(smoothed)
        for i in range(count):
            p0 = smoothed[i]
            p1 = smoothed[(i + 1) % count]

            q = (0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1])
            r = (0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1])
            new_points.extend([q, r])

        smoothed = new_points

    return smoothed

# --- Step 1: Load image ---
img = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Input image not found: test.png")

# Increase tracing resolution before contour detection.
upscale_factor = 3.0
img_hr = cv2.resize(
    img,
    None,
    fx=upscale_factor,
    fy=upscale_factor,
    interpolation=cv2.INTER_CUBIC,
)

# --- Step 2: Edge detection ---
img_blur = cv2.GaussianBlur(img_hr, (5, 5), 0)
edges = cv2.Canny(img_blur, threshold1=80, threshold2=180)

# --- Step 3: Find contours (vector paths) ---
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# --- Step 4: Create DXF drawing ---
doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()

scale = 1  # Example: 1 pixel = 1 CAD unit

# Hybrid output tuning.
approx_epsilon_factor = 0.006
straight_segment_vertex_limit = 10

for cnt in contours:
    epsilon = approx_epsilon_factor * cv2.arcLength(cnt, True)
    simplified = cv2.approxPolyDP(cnt, epsilon, True)

    simplified_points = [
        (
            (float(pt[0][0]) / upscale_factor) * scale,
            (float(pt[0][1]) / upscale_factor) * scale,
        )
        for pt in simplified
    ]

    points = [
        (
            (float(pt[0][0]) / upscale_factor) * scale,
            (float(pt[0][1]) / upscale_factor) * scale,
        )
        for pt in cnt
    ]

    if len(simplified_points) > 2 and len(simplified_points) <= straight_segment_vertex_limit:
        # Preserve line segments exactly for straight-edged geometry.
        msp.add_lwpolyline(simplified_points, close=True)
    elif len(points) > 2:
        # Keep curved geometry smooth.
        smooth_points = chaikin_smoothing(points, iterations=2)
        msp.add_spline(fit_points=smooth_points + [smooth_points[0]], degree=3)

# --- Step 5: Save DXF ---
doc.saveas("output.dxf")

print("DXF drawing created successfully!")