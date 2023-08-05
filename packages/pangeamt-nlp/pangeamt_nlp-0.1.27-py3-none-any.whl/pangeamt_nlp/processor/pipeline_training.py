from typing import List
from pangeamt_nlp.processor.base.processor_base import ProcessorBase
from pangeamt_nlp.seg import Seg

class PipelineTraining:
    def __init__(self, processors: List[ProcessorBase]):
        self._processors = processors

    def process(self, seg: Seg) -> None:
        for processor in self._processors:
            processor.process_train(seg)


