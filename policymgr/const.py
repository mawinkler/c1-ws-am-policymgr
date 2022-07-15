SCAN_CONFIGURATIONS = {
    "realtime_scan_configuration",
    "scheduled_scan_configuration",
}

LIST_TYPES = {
    "directory_lists": {
        "exclude": "excludedDirectoryListID",
        "include": "directoryListID",
    },
    "file_lists": {
        "exclude": "excludedFileListID",
        "include": ""
    },
    "file_extension_lists": {
        "exclude": "excludedFileExtensionListID",
        "include": "fileExtensionListID",
    },
}

DEFAULT_REALTIME_POLICY = {
    "description": "",
    "scanType": "real-time",
    "documentExploitProtectionEnabled": True,
    "documentExploitProtection": "critical-only",
    "documentExploitHeuristicLevel": "default",
    "machineLearningEnabled": True,
    "behaviorMonitoringEnabled": True,
    "documentRecoveryEnabled": False,
    "intelliTrapEnabled": True,
    "memoryScanEnabled": False,
    "spywareEnabled": True,
    "alertEnabled": True,
    "directoriesToScan": "all-directories",
    "filesToScan": "all-files",
    "excludedProcessImageFileListID": 1,
    "realTimeScan": "read-write",
    "scanCompressedEnabled": True,
    "scanCompressedMaximumSize": 2,
    "scanCompressedMaximumLevels": 2,
    "scanCompressedMaximumFiles": 10,
    "microsoftOfficeEnabled": True,
    "microsoftOfficeLayers": 3,
    "networkDirectoriesEnabled": False,
    "customRemediationActionsEnabled": False,
    "amsiScanEnabled": True,
    "scanActionForBehaviorMonitoring": "pass",
    "scanActionForMachineLearning": "pass",
    "scanActionForAmsi": "pass",
}
DEFAULT_SCHEDULED_POLICY = {
    "description": "",
    "scanType": "on-demand",
    "documentExploitProtectionEnabled": True,
    "documentExploitProtection": "critical-only",
    "documentExploitHeuristicLevel": "default",
    "spywareEnabled": True,
    "alertEnabled": True,
    "directoriesToScan": "all-directories",
    "filesToScan": "all-files",
    "scanCompressedEnabled": True,
    "scanCompressedMaximumSize": 2,
    "scanCompressedMaximumLevels": 2,
    "scanCompressedMaximumFiles": 10,
    "microsoftOfficeEnabled": True,
    "microsoftOfficeLayers": 3,
    "customRemediationActionsEnabled": False,
    "cpuUsage": "high"
}