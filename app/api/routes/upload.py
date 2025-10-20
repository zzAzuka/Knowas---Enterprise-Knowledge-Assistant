from fastapi import APIRouter, UploadFile, File, Depends
from core.auth import require_role
from schemas.uploadSchema import uploadOutput
from services.dataExtraction import extractedfFromS3
from services.pdfTextExtraction import pdfTextExtraction
import boto3
import mlflow
from datetime import datetime

BUCKET_NAME = 'knowledge-assistant-data-lake-sibirassal'
router = APIRouter()
s3_client = boto3.client('s3')

@router.post("/", response_model=uploadOutput)
async def uploadDocument(current_user=Depends(require_role("full_access")), file: UploadFile = File(...)):
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("Uplaod_Route_Experiment")

    with mlflow.start_run(run_name=f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        try:
            mlflow.log_param("bucketname", BUCKET_NAME)
            filename = file.filename

            if file.content_type == "application/pdf":
                mlflow.log_param("filename", filename)

                s3_client.upload_fileobj(file.file, BUCKET_NAME, filename)
                print(f"Uploaded {filename} to S3 bucket: {BUCKET_NAME}")

                extractedfFromS3(filename=filename)
                print(f"Downloaded {filename} locally!")

                pdfTextExtraction(filename=filename)
                print(f"Added vectors for {filename} to Pinecone.")
            else:
                print("Only accepting PDF files now!")

            mlflow.set_tag("upload_status", "completed")
            
            return {
            "filename": filename,
            "status": "success",
            "message": "File uploaded and processed successfully"
            }
        except Exception as e:
            mlflow.set_tag("upload_status", "failed")
            mlflow.log_param("error_message", str(e))
            return {
                "filename": filename,
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }
