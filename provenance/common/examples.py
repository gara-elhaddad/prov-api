

EXAMPLES = {
    "File": {
        "description": "Demonstration data for validation framework",
        "format": "application/json",
        "hash": {
            "algorithm": "sha1",
            "value": "716c29320b1e329196ce15d904f7d4e3c7c46685"
        },
        "location": "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/VF_paper_demo/obs_data/InputResistance_data.json",
        "file_name": "InputResistance_data.json",
        "size": 34
    },
    "ComputationalEnvironment": {
        "name": "SpiNNaker default 2021-10-13",
        "hardware": "spinnaker",
        "configuration": [
            {
                "items": [{
                    "name": "parameter1",
                    "value": "value1"
                },
                    {
                    "name": "parameter2",
                    "value": "value2"
                }],
                "description": "hardware configuration for SpiNNaker 1M core machine"
            }
        ],
        "software": [
            {
                "software_name": "numpy",
                "software_version": "1.19.3"
            },
            {
                "software_name": "neo",
                "software_version": "0.9.0"
            },
            {
                "software_name": "spyNNaker",
                "software_version": "5.0.0"
            }
        ],
        "description": "Default environment on SpiNNaker 1M core machine as of 2020-10-13 (not really, this is just for example purposes)."
    },
    "LaunchConfiguration": {
        "executable": "/usr/bin/python",
        "arguments": [
            "-Werror"
        ],
        "environment_variables": {
            "items": [{
                "name": "COLLAB_ID",
                "value": "myspace"
            }]
        }
    },
    "ResourceUsage": {
        "value": 1017.3,
        "units": "second"
    }
}
