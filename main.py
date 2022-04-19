from fastapi import FastAPI
from service import workflow_service
from pydantic import BaseModel


class Input(BaseModel):
    name: str
    fastq1: str
    fastq1filetype: str
    fastq2: str
    fastq2filetype: str
    reference: str | None = None
    referencefiletype: str | None = None


app = FastAPI()


@app.post("/workflow/run")
async def run(input: Input):
    return workflow_service.run(input.name,
                         input.fastq1, input.fastq1filetype,
                         input.fastq2, input.fastq2filetype,
                         input.reference, input.referencefiletype)