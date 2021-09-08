
import sys
from pydantic import parse_obj_as

sys.path.append(".")
from provenance.dataanalysis.data_models import DataAnalysis
from provenance.dataanalysis.examples import EXAMPLES


class TestDataAnalysis:

    def test_conversion_to_kg_objects(self):
        #pydantic_obj = DataAnalysis(**EXAMPLES["DataAnalysis"])
        pydantic_obj = parse_obj_as(DataAnalysis, EXAMPLES["DataAnalysis"])
        kg_client = None
        kg_objects = pydantic_obj.to_kg_objects(kg_client)
