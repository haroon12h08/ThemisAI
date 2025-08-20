from fastapi import APIRouter, UploadFile, File
import shutil
import os
from detection.cheque_detector import process_cheque
from signature_verification.signature_match import compare_signatures
import traceback

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extract")
async def extract_cheque_details(
    cheque: UploadFile = File(...),
    signature: UploadFile = File(...)
):
    try:
        cheque_path = f"temp_{cheque.filename}"
        sig_path = f"temp_{signature.filename}"

        with open(cheque_path, "wb") as f:
            f.write(await cheque.read())
        with open(sig_path, "wb") as f:
            f.write(await signature.read())

        # Debug logs
        print("📄 Running process_cheque on:", cheque_path)
        details = process_cheque(cheque_path)
        print("📄 Extracted details:", details)

        print("✍️ Comparing signatures...")
        match_score = compare_signatures(sig_path, sig_path)
        print("✍️ Signature match score:", match_score)

        os.remove(cheque_path)
        os.remove(sig_path)

        return {
            "status": "success",
            "details": details if details else {},
            "signature_match_score": float(match_score) if match_score else 0.0
        }

    except Exception as e:
        print("⚠️ ERROR in cheque processing:")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}



@router.post("/cheque/verify_signature")
async def verify_signature(
    sig1: UploadFile = File(...),
    sig2: UploadFile = File(...)
):
    """
    Compare two signature images and return similarity score.
    """
    try:
        sig1_path = os.path.join(UPLOAD_DIR, sig1.filename)
        sig2_path = os.path.join(UPLOAD_DIR, sig2.filename)

        with open(sig1_path, "wb") as buffer:
            shutil.copyfileobj(sig1.file, buffer)
        with open(sig2_path, "wb") as buffer:
            shutil.copyfileobj(sig2.file, buffer)

        score = compare_signatures(sig1_path, sig2_path)

        # Cleanup
        os.remove(sig1_path)
        os.remove(sig2_path)

        return {"status": "success", "similarity_score": score}

    except Exception as e:
        print("⚠️ ERROR in signature verification:")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
