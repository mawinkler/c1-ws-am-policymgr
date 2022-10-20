# Anti Malware Scan Configuration Manager

- [Anti Malware Scan Configuration Manager](#anti-malware-scan-configuration-manager)
  - [Setup](#setup)
  - [YAML Structure](#yaml-structure)
    - [`malware_scan_configuration`](#malware_scan_configuration)
    - [`exclusion_lists`](#exclusion_lists)
    - [`inclusion_lists`](#inclusion_lists)
  - [Results](#results)
  - [Support](#support)
  - [Contribute](#contribute)

Manages file-, directory- and file extension inclusion- and exclusion lists alongside scan configurations in Cloud One Workload Security based on a central YAML definition.

For official recommendations by Trend Micro Business Success follow this link: [Recommended scan exclusion list for Trend Micro Endpoint products](https://success.trendmicro.com/dcx/s/solution/1059770-recommended-scan-exclusion-list-for-trend-micro-endpoint-products?language=en_US)


> ***Note:*** This script is at *ALPHA* stage which means, that not all required functionalities are implemented yet. Additionally it is *NOT* tested in production environments as of now.
>
> Currently known missing functionality:
>
> - Deletion of orphaned lists
> - Potential management UI or CLI to create the YAML configuration (requested by not so YAML friendly ppl :-) )
> - Syntax check as required by Workload Security for the lists
>
> Additionally, some code clean-up, as usual.

## Setup

1. Ensure to have the dependencies satisfied

    ```sh
    pip install -r requirements.txt
    ```

2. Create a api endpoint url and api key configuration.

    ```sh
    $ sudo bash -c 'echo "us-1.cloudone.trendmicro.com" > /etc/cloudone-credentials/c1_url'
    $ sudo bash -c 'echo "<YOUR CLOUD ONE API KEY>" > /etc/cloudone-credentials/api_key'
    ```

3. Create or modify the configuration. See [YAML Structure](#yaml-structure)

4. Run the script by

    ```sh
    python3 policymgr/mgr.py
    ```

The script will automatically create or update existing lists within your Cloud One Workload Security.

## YAML Structure

The YAML file has three sections:

- `malware_scan_configuration`
- `exclusion_lists`
- `ìnclusion_lists`

To help writing the YAML configuration file the repo contains a schema definition. If using Visual Studio Code do the following:

- Go to Code (Mac) or File (Windows) -> Preferences -> Settings (or use the Command Pallete) to open the settings page and search for yaml.
- Open the settings for the YAML extension and search for "Yaml: Schemas" and click `Edit in settings.json`.
- The "settings.json" file will open. you need to search again for the "yaml.schemas" object. If it doesn´t exist yet, you will have to create it.
- This property represents a key-value, where the key is the *absolute path* to the schema file on your system and the value is a glob expression that specifies the files that the schema will be applied. In my case it looks like this:

    ```yaml
    "yaml.schemas": {
        "/home/markus/projects/trend/c1-ws-am-policymgr/c1-ws-am-policymgr-schema.json": "policymgr.cfg.yaml",
    },
    ```

- Save the file and reload VS Code to finish the process. A `Developer: Reload Window" is sufficient as well.

### `malware_scan_configuration`

Example:

```yaml
malware_scan_configuration:
  ## Realtime Scan Configuration
  realtime_scan_configuration:
    - name: windows_server_2019_domain_controller
      inclusions:
        - directory_lists:
            - windows_server
          file_extension_lists: []
      exclusions:
        - directory_lists:
            - windows_server_2019
          file_lists:
            - windows_server
            - windows_domain_controller
          file_extension_lists: []
    - name: windows_server_2019_member_server
      inclusions:
        - directory_lists:
            - windows_server
          file_extension_lists: []
      exclusions:
        - directory_lists:
            - windows_server_2019
          file_lists:
            - windows_server
            - windows_member_server
          file_extension_lists: []
```

The above defines the inclusions and exclusions for the defined scan configuration (referenced by `name`).

As an example, the windows server 2019 member server realtime scan configuration would get the file lists referenced as `windows_server` and `windows_member_server` assigned. The lists themselves are defined in the `exclusion_lists` and `inclusion_lists` sections.

Scheduled scan configuration are handled accordingly (see sample `config.yaml` provided).

### `exclusion_lists`

Example

```yaml
exclusion_lists:
  directory_lists:
    windows_server_2016:
      - '${windir}\SoftwareDistribution\Datastore\'
      - '${windir}\SoftwareDistribution\Datastore\Logs\'
    windows_server_2019:
      - '${windir}\SoftwareDistribution\Datastore\'
      - '${windir}\SoftwareDistribution\Datastore\Logs\'
    linux_root:
      - '/root/'
  file_lists:
    windows_server:
      - '${windir}\Security\Database\*.edb'
      - '${windir}\Security\Database\*.sdb'
      - '${windir}\Security\Database\*.log'
      - '${windir}\Security\Database\*.edb'
      - '${windir}\Security\Database\*.edb'
    windows_domain_controller:
      - '${windir}\Ntds\Ntds.dit'
      - '${windir}\Ntds\Ntds.pat'
      - '${windir}\Ntds\EDB*.log'
      - '${windir}\Ntds\Res*.log'
      - '${windir}\Ntds\Edb*.jrs'
      - '${windir}\Ntds\Ntds.pat'
    windows_member_server:
      - 'D:\TEST.LOG'
  file_extension_lists: []
```

Continuing the above example, the member server would get a file list for exclusions created containing the list elements of `windows_server` and `windows_member_server`.

### `inclusion_lists`

Same as for `exclusion_lists` but for includes

## Results

The example configuration provided will create/updates the following anti malware configurations:

```json
{"realtime_windows_server_2016_domain_controller_configuration": 168,
 "realtime_windows_server_2019_domain_controller_configuration": 169,
 "realtime_windows_server_2019_member_server_configuration": 170,
 "scheduled_linux_server_configuration": 173,
 "scheduled_windows_server_2016_domain_controller_configuration": 171,
 "scheduled_windows_server_2019_domain_controller_configuration": 172}
```

As defined in the configuration the chosen directory, extension and file lists are assigned to the configurations:

```json
{"directory_lists": {"exclusion_realtime_windows_server_2016_domain_controller": 12,
                     "exclusion_realtime_windows_server_2019_domain_controller": 13,
                     "exclusion_realtime_windows_server_2019_member_server": 15,
                     "exclusion_scheduled_linux_server": 17,
                     "inclusion_realtime_windows_server_2019_domain_controller": 14,
                     "inclusion_realtime_windows_server_2019_member_server": 16,
                     "inclusion_scheduled_windows_server_2019_domain_controller": 18},
 "file_extension_lists": {"Scan File Extension List (Windows)": 1},
 "file_lists": {"Process Image Files (Windows)": 1,
                "exclusion_realtime_windows_server_2016_domain_controller": 102,
                "exclusion_realtime_windows_server_2019_domain_controller": 81,
                "exclusion_realtime_windows_server_2019_member_server": 101}}
```

Whatever is changed in the lists propagetes up to the configuration(s) when rerunning the `mgr.py`.

## Support

This is an Open Source community project. Project contributors may be able to help, depending on their time and availability. Please be specific about what you're trying to do, your system, and steps to reproduce the problem.

For bug reports or feature requests, please [open an issue](../../issues). You are welcome to [contribute](#contribute).

Official support from Trend Micro is not available. Individual contributors may be Trend Micro employees, but are not official support.

## Contribute

I do accept contributions from the community. To submit changes:

1. Fork this repository.
2. Create a new feature branch.
3. Make your changes.
4. Submit a pull request with an explanation of your changes or additions.

I will review and work with you to release the code.
