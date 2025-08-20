import cv2

def compare_signatures(sig1_path: str, sig2_path: str) -> float:
    """Compare two signatures using ORB feature matching."""
    img1 = cv2.imread(sig1_path, 0)
    img2 = cv2.imread(sig2_path, 0)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0.0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    if not matches:
        return 0.0

    score = len(matches) / max(len(kp1), len(kp2)) * 100
    return score
