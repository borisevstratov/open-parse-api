from typing import List
from fastapi import APIRouter, File, UploadFile
from openparse import Node, DocumentParser
from pydantic import BaseModel

from app.utils.files import get_upload_file_path
from app.utils.parser import CustomIngestionPipeline, get_document_markdown

router = APIRouter(tags=["parse"], prefix="/parse")


class ResponseType(BaseModel):
    nodes: List[Node]
    markdown: str | None = None


@router.post("/basic")
def parse_basic(file: UploadFile = File(...)) -> ResponseType:
    tmp_path = get_upload_file_path(file)
    parser = DocumentParser()
    parsed_content = parser.parse(tmp_path)

    return ResponseType(
        nodes=parsed_content.nodes,
        markdown=get_document_markdown(parsed_content.nodes),
    )


@router.post("/custom")
def parse_custom(file: UploadFile = File(...)) -> ResponseType:
    tmp_path = get_upload_file_path(file)

    parser = DocumentParser(
        processing_pipeline=CustomIngestionPipeline(),
        table_args={"parsing_algorithm": "pymupdf"},
    )

    parsed_content = parser.parse(file=tmp_path, ocr=True)

    return ResponseType(
        nodes=parsed_content.nodes,
        markdown=get_document_markdown(parsed_content.nodes),
    )
