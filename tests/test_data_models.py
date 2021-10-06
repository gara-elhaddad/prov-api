
import sys
from copy import deepcopy
from datetime import datetime, timezone
from uuid import UUID
import json

import jsondiff

from pydantic import parse_obj_as

sys.path.append(".")
from provenance.dataanalysis.data_models import DataAnalysis
from provenance.dataanalysis.examples import EXAMPLES
import fairgraph.openminds.core as omcore
import fairgraph.openminds.controlledterms as omterms
import fairgraph.openminds.computation as omcmp
from fairgraph.base_v3 import IRI


class MockKGClient:
    pass


class TestDataAnalysis:

    def test_conversion_to_kg_objects(self):
        #pydantic_obj = DataAnalysis(**EXAMPLES["DataAnalysis"])
        pydantic_obj = parse_obj_as(DataAnalysis, EXAMPLES["DataAnalysis"])
        kg_client = None
        kg_objects = pydantic_obj.to_kg_objects(kg_client)

    def test_conversion_from_kg_objects(self):
        omcore.SoftwareVersion.set_strict_mode(False)
        omcore.ParameterSet.set_strict_mode(False, "context")

        started_by = omcore.Person(
            family_name="Destexhe",
            given_name="Alain",
            digital_identifiers=[omcore.ORCID(identifier="https://orcid.org/0000-0001-7405-0455")],
            id=UUID("{00000000-0000-0000-0000-000000000000}")
        )
        inputs = [
            omcore.File(
                content="Demonstration data for validation framework",
                format=omcore.ContentType(name="application/json", id=UUID("{00000000-0000-0000-0000-000000000000}")),
                hash=omcore.Hash(algorithm="sha1", digest="716c29320b1e329196ce15d904f7d4e3c7c46685"),
                iri=IRI("https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/VF_paper_demo/obs_data/InputResistance_data.json"),
                name="InputResistance_data.json",
                storage_size=omcore.QuantitativeValue(value=34.0, units=omterms.UnitOfMeasurement(name="bytes"))
            ),
            omcore.SoftwareVersion(
                name="Elephant",
                version_identifier="0.10.0",
                id=UUID("{00000000-0000-0000-0000-000000000000}")
            )
        ]
        outputs = [deepcopy(inputs[0])]
        environment = omcmp.Environment(
            name="SpiNNaker default 2021-10-13",
            hardware=omcmp.HardwareSystem(name="spinnaker"),
            configuration=omcore.ParameterSet(
                    parameters=[
                        omcore.StringParameter(name="parameter1", value="value1"),
                        omcore.StringParameter(name="parameter2", value="value2")
                    ],
                    context="hardware configuration for SpiNNaker 1M core machine"
            ),
            software=[
                omcore.SoftwareVersion(name="numpy", version_identifier="1.19.3", id=UUID("{00000000-0000-0000-0000-000000000000}")),
                omcore.SoftwareVersion(name="neo", version_identifier="0.9.0", id=UUID("{00000000-0000-0000-0000-000000000000}")),
                omcore.SoftwareVersion(name="spyNNaker", version_identifier="5.0.0", id=UUID("{00000000-0000-0000-0000-000000000000}"))
            ],
            description="Default environment on SpiNNaker 1M core machine as of 2020-10-13 (not really, this is just for example purposes)."

        )
        launch_configuration = omcmp.LaunchConfiguration(
            executable="/usr/bin/python",
            arguments=["-Werror"],
            environment_variables=omcore.ParameterSet(
                parameters=[omcore.StringParameter(name= "COLLAB_ID", value= "myspace")]
            )
        )
        resource_usage = [omcore.QuantitativeValue(value=1017.3, unit=omterms.UnitOfMeasurement(name="core-hours"))]
        data_analysis = omcmp.DataAnalysis(
            id=UUID("{00000000-0000-0000-0000-000000000000}"),
            inputs=inputs,
            outputs=outputs,
            environment=environment,
            launch_configuration=launch_configuration,
            started_at_time=datetime(2021, 5, 28, 16, 32, 58, 597000, tzinfo=timezone.utc),
            ended_at_time=datetime(2021, 5, 28, 16, 32, 58,  597000, tzinfo=timezone.utc),
            started_by=started_by,
            status=omterms.ActionStatusType(name="queued"),
            resource_usages=resource_usage,
            tags=["string"]
        )

        client = MockKGClient()
        pydantic_obj = DataAnalysis.from_kg_object(data_analysis, client)

        # remove IDs added by from_kg_object() for the comparison
        for item in pydantic_obj.environment.software:
            item.id = None
        pydantic_obj.input[1].id = None

        actual = pydantic_obj.json(exclude_none=True)
        expected = json.dumps(deepcopy(EXAMPLES["DataAnalysis"]))

        diff = jsondiff.diff(actual, expected, load=True, syntax="explicit")
        assert len(diff) == 0
