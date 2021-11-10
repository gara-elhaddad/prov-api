
EXAMPLES = {
    "Visualisation": {
        "input": [
            {
                "description": "Simple script to plot the data in an electrophysiology data file, version 0.1.0",
                "format": "text/x-python",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "94c1ef1c18a67bea479c71c03d937ed704fd3a15"
                },
                "location": "https://drive.ebrains.eu/f/c004d5f69bde40a58e9d/",
                "file_name": "/mnt/user/shared/EBRAINS Workflows/examples/visualisation/plot_ephys_data.py",
                "size": 1612
            },
            {
                "description": "File(id='https://kg.ebrains.eu/api/instances/c69e8b64-1571-43a1-865e-ccf110923a3d')",
                "format": None,
                "hash": {
                    "algorithm": "MD5",
                    "value": "6c2a65bb8fedb3047edbd255a0c515ef"
                },
                "location": "https://object.cscs.ch/v1/AUTH_63ea6845b1d34ad7a43c8158d9572867/Freund_SGA1_T1.2.5/HC-awake-ephys/HBP_1/cell1/ephys/Freund_SGA1_T1.2.5_HC-awake-ephys_HBP_1_cell1_ephys__160712_cell1.smr",
                "file_name": "Freund_SGA1_T1.2.5_HC-awake-ephys_HBP_1_cell1_ephys__160712_cell1.smr",
                "size": None
            }
        ],
        "output": [
            {
                "description": "File generated by visualisation 6935971d-ab77-4b48-bda1-c121a5a007ea",
                "format": "image/png",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "9006f7ca30ee32d210249ba125dfd96d18b6669e"
                },
                "location": "https://drive.ebrains.eu/f/61ceb5c4aa3c4468a26c/",
                "file_name": "output_files/Freund_SGA1_T1.2.5_HC-awake-ephys_HBP_1_cell1_ephys__160712_cell1_LFP.png",
                "size": 60715
            },
            {
                "description": "File generated by visualisation 6935971d-ab77-4b48-bda1-c121a5a007ea",
                "format": "image/png",
                "hash": {
                    "algorithm": "SHA-1",
                    "value": "bd6378e49f754981dbbc7b74047fe28a0c307ce9"
                },
                "location": "https://drive.ebrains.eu/f/aa35210564db48b387e0/",
                "file_name": "output_files/Freund_SGA1_T1.2.5_HC-awake-ephys_HBP_1_cell1_ephys__160712_cell1_Unit.png",
                "size": 52810
            }
        ],
        "environment": {
            "name": "EBRAINS Lab 20211028",
            "hardware": "openstack_cscs",
            "configuration": [],
            "software": [
                {
                    "software_name": "python",
                    "software_version": "3.6.9"
                },
                {
                    "software_name": "neo",
                    "software_version": "0.8.0"
                },
                {
                    "software_name": "numpy",
                    "software_version": "1.18.1"
                },
                {
                    "software_name": "quantities",
                    "software_version": "0.12.5"
                },
                {
                    "software_name": "matplotlib",
                    "software_version": "3.3.1"
                }
            ],
            "description": "Standard EBRAINS Lab environment"
        },
        "launch_config": {
            "executable": "python",
            "arguments": [
                "plot_ephys_data.py",
                "https://object.cscs.ch/v1/AUTH_63ea6845b1d34ad7a43c8158d9572867/Freund_SGA1_T1.2.5/HC-awake-ephys/HBP_1/cell1/ephys/Freund_SGA1_T1.2.5_HC-awake-ephys_HBP_1_cell1_ephys__160712_cell1.smr"
            ],
            "environment_variables": None
        },
        "start_time": "2021-10-28T15:29:09.876476+00:00",
        "end_time": "2021-10-28T15:29:15.298888+00:00",
        "status": "completed",
        "resource_usage": [
            {
                "value": 5.422412,
                "units": "seconds"
            }
        ],
        "tags": [
            "demo",
            "electrophysiology"
        ],
        "id": "6935971d-ab77-4b48-bda1-c121a5a007ea"
    }
}
