EXAMPLES = {
    "WorkflowExecution": {
        "recipe_id": "24b44ee2-2594-4c7b-ad3c-e1498d219f22",
        "started_by": {
            "given_name": "Bilbo",
            "family_name": "Baggins"
        },
        "stages": [{
            "type": "data analysis",
            "input": [{
                "description":
                "arcp://uuid,b2020c9c-9e93-46c7-b87d-14078bd50247/workflow/packed.cwl#main/analysis/input_file",
                "file_name": "sub-1_chs-32_hem-RH_ana-ISO000_stim-SPN.mat",
                "format": "application/5-mat",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "495534ad6bc23e91b3db8df24ef86fdf23e5e232"
                },
                "location": "file://input/sub-1_chs-32_hem-RH_ana-ISO000_stim-SPN.mat",
                "size": 153765472
            }, {
                "description":
                "Computes the PSD (Power Spectral Density) for every selected channel in the signal",
                "file_name": "step1/analysis.py",
                "format": "text/x-python",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "80f6e6cbfa8337c2bcc068e346c9d39116a98603"
                },
                "location": "https://gitlab.ebrains.eu/technical-coordination/project-internal/workflows/cwl-workflows/-/blob/main/PSD_workflow_no_fetch/step1/analysis.py",
                "size": 1375
            }],
            "output": [{
                "description": "arcp://uuid,b2020c9c-9e93-46c7-b87d-14078bd50247/workflow/packed.cwl#main/analysis/output_file",
                "file_name": "psd.json",
                "format": "application/json",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "2fa22815decc53f71607249792ccae03dfce2574"
                },
                "location": None,
                "size": 3515921
            }],
            "environment": {
                "name": "docker-registry.ebrains.eu/tc/cwl-workflows/psd_workflow_analysis@sha256:6a9014185aa4a47729f301c78050fc562491e3b95ef91482fdb907bf9aec84c3",
                "hardware": "generic",
                "configuration": [{
                    "items": [
                        {"name": "platform", "value": "macOS-12.2.1-arm64-arm-64bit"}
                    ]
                }],
                "software": [{
                    "software_name": "Docker",
                    "software_version": "20.10.12"
                }, {
                    "software_name": "cwltool",
                    "software_version": "3.1.20220224085855"
                }, {
                    "software_name": "Python",
                    "software_version": "3.8.9"
                }],
                "description": "Docker container run from docker-registry.ebrains.eu/tc/cwl-workflows/psd_workflow_analysis:latest on Andrew Davison's MacBook Pro (14-inch, 2021)"
            },
            "launch_config": {
                "executable": "python",
                "arguments": [
                    "input/sub-1_chs-32_hem-RH_ana-ISO000_stim-SPN.mat",
                    "--channels 0 1 2 3 4", "--output_file psd.json"
                ],
                "environment_variables": None
            },
            "start_time": "2022-03-28T16:04:00.381279",
            "end_time": "2022-03-28T16:06:42.421212",
            "status": "completed",
            "resource_usage": [{
                "value": 162.39933,
                "units": "second"
            }],
            "tags": ["demo", "cwl"],
            "description": "Run of workflow/packed.cwl#main/analysis"
        }, {
            "type": "visualization",
            "description": "Run of workflow/packed.cwl#main/visualization",
            "end_time": "2022-03-28T16:07:07.786379",
            "environment": {
                "configuration": [{
                    "items": [
                        {"name": "platform", "value": "macOS-12.2.1-arm64-arm-64bit"}
                    ]
                }],
                "description": "Docker container run from docker-registry.ebrains.eu/tc/cwl-workflows/psd_workflow_visualization:latest on Andrew Davison's MacBook Pro (14-inch, 2021)",
                "hardware": "generic",
                "name": "docker-registry.ebrains.eu/tc/cwl-workflows/psd_workflow_visualization@sha256:b4c6a687da51e3117f97dcf5de1611e5e09eebb7865e8d9194151fe81e823b54",
                "software": None
            },
            "input": [{
                "description": "arcp://uuid,b2020c9c-9e93-46c7-b87d-14078bd50247/workflow/packed.cwl#main/visualization/input_file",
                "file_name": "psd.json",
                "format": "application/json",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "2fa22815decc53f71607249792ccae03dfce2574"
                },
                "location": None,
                "size": 3515921
            }, 
            {
                "description":
                "Computes the PSD (Power Spectral Density) for every selected channel in the signal",
                "file_name": "step2/visualization.py",
                "format": "text/x-python",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "4b7eef5db00d535457fa5b4002c3fa4e01fceb72"
                },
                "location": "https://gitlab.ebrains.eu/technical-coordination/project-internal/workflows/cwl-workflows/-/blob/main/PSD_workflow_no_fetch/step2/visualization.py",
                "size": 1257
            }],
            "launch_config": {
                "arguments": [],
                "environment_variables": None,
                "executable": "python"
            },
            "output": [{
                "description": "final_output",
                "format": "image/png",
                "location": "https://drive.ebrains.eu/f/5e2f90de59ef4559813d/?dl=1",
                "file_name": "output.png",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "ec7ede9a48002ba61627ace37ae2b4dbba34b858"
                },
                "size": 64935
            }],
            "resource_usage": [{
                "units": "second",
                "value": 25
            }],
            "start_time": "2022-03-28T16:06:42.433013",
            "status": "completed",
            "tags": ["demo", "cwl"]
        }]
    }
}
