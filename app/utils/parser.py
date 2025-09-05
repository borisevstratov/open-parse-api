from typing import List

from openparse import Node, processing


def get_document_markdown(nodes: List[Node]) -> str:
    return "\n\n".join(node.text for node in nodes)


class CustomIngestionPipeline(processing.IngestionPipeline):
    def __init__(self):
        self.transformations = [
            processing.RemoveTextInsideTables(),
            processing.CombineNodesSpatially(criteria="either_stub"),
            processing.CombineBullets(),
            processing.CombineHeadingsWithClosestText(),
            processing.RemoveFullPageStubs(max_area_pct=0.20),
        ]
