# datapackage-pipelines-fiscal

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datapackage-pipelines-fiscal.svg)](https://pypi.org/project/datapackage-pipelines-fiscal/)
[![Travis](https://travis-ci.org/openspending/datapackage-pipelines-fiscal.svg?branch=master)](https://travis-ci.org/openspending/datapackage-pipelines-fiscal)

Extension for datapackage-pipelines used for loading Fiscal Data Packages into:
- S3 (or compatible) storage, in a denormalized form
- a database in normalized form.
- Metadata will be stored in an elasticsearch instance (if available) via [os-package-registry](https://github.com/openspending/os-package-registry)
- A `babbage` model will also be generated and written to the datapackage for querying the database using its API

This extension works with a custom source spec and a set of processors. The generator will convert the source spec into a set of inter-dependent pipelines, which when run in order will perform data processing and loading to selected endpoints (based on environment variables).

This extension is used by [os-conductor](https://github.com/openspending/os-conductor) and [os-data-importers](https://github.com/openspending/os-data-importers).

## Environment variables

`DPP_DB_ENGINE` - connection string for an SQL database to dump data into

`ELASTICSEARCH_ADDRESS` [OPTIONAL] - connection string for an elasticsearch instance (used for package registry updating)

`S3_BUCKET_NAME` [OPTIONAL] - S3 bucket for uploading data. If not provided, local ZIP files will be created instead.

`AWS_ACCESS_KEY_ID` - S3 credentials (required if S3 bucket was specified)

`AWS_SECRET_ACCESS_KEY` - S3 credentials (required if S3 bucket was specified)

## Dependencies

In order to fully run the fiscal datapackage flow you need to have `os-types` installed, using npm:

`$ npm install -g os-types`

This external node.js utility is used to perform fiscal modelling for the processed datapackage.

## fiscal.source-spec.yaml

Each source-spec contains information regarding a single Fiscal Data Package.

Top level properties are:

#### `title`
Title, or Display name, of the data package

#### `dataset-name` [OPTIONAL]
A slug to be used as the data package's name.

If not provided, a slugified version of the title will be used.

#### `resource-name` [OPTIONAL]

A slug to be used as the main resource's name in the final data package.

If not provided, the dataset name will be used.

#### `owner-id`

The id of the owner of this datapackage.

This identifier is used to generate various paths and storage names.

#### `sources`

Contains a non-empty list of data sources for the fiscal data package.

Each data source has these properties:
- `url`: The location of the data
- `name`: [OPTIONAL] A name for this source (will later be used as an intermediate resource name)

Other `tabulator` parameters can also be added as properties here, e.g. `sheet`, `encoding`, `compression` etc.

#### `fields`

Contains a non-empty list of fields for the fiscal data package.

Each field definition has these properties:
- `header`: The `name` of the field in the resulting resource
- `title` [OPTIONAL]: The display name of the field in the resulting resource
- `columnType`: The _ColumnType_ of the field
- `options`: Extra options to be added to the field, e.g. json-table-schema properties such as `decimalChar` etc.

#### `measures` [OPTIONAL]

Extra information for measure normalization processing.
(Measure normalization is the process of reducing the number of measures to one while multipltying the number of rows and adding extra columns to contain values for identifying the original measure).

Contains the following sub-properties:
- `currency`: The currency code of the output measure column
- `title` [OPTIONAL]: The title for the output measure column
- `mapping`: Unpivoting map.

The unpivoting map is a map from a measure's name to its unpivoting data.

"Unpivoting data" is a map from an extra column's name to a value

Example:
```yaml
measures:
  currency: GTQ
  mapping:
    APPROVED:
      PHASE_ID: "0"
      PHASE: Inicial
    RELEASED:
      PHASE_ID: "1"
      PHASE: Vigente
    COMMITTED:
      PHASE_ID: "2"
      PHASE: Comprometido
```

- `currencies` [OPTIONAL]: List of currency codes to convert to ('USD' by default).
  See next section for details


#### `currency-conversion` [OPTIONAL]

Instructions for adding an extra column or columns with measure values in another currency.

- `date_measure` [OPTIONAL]: Column name from which a date can be extracted.
  If not provided, a guess will be made according to the _ColumnType_.

- `title` [OPTOINAL]: Title for the currency-converted measure columns.

#### `datapackage-url` [OPTIONAL]

Contains the URL for a source datapackage from which this data came from.
If provided, metadata for this datapackage will be loaded from this URL.

#### `deduplicate` [OPTIONAL]

If `true`, then the source data will be processed to remove duplicate rows (i.e. rows which have the same values in the primary key). Measure values for these rows will be summed in order to generate a single output row.

#### `postprocessing` [OPTIONAL]

A list of extra processors (and parameters) that will be applied to the data.
Format is as in any `pipeline-spec.yaml`

#### `suppress-os` [OPTIONAL, default is `False`]

If `False`, an OpenSpending compatible datapackage is created on the datastore. This basic datapackage ensures a basic FDP is available for editing with OpenSpending. Packages created with `os-conductor` already create this artefact, so would use `suppress-os: True`, to prevent another being created unnecessarily.

#### `keep-artifacts` [OPTIONAL, default is `False`]

By default, pipeline artifacts (temporary directories and files creating during pipeline execution) will be removed after all pipelines have successfully been run. To keep the artifact, set this option to `True`.


## Generated Pipelines

#### ./denormalized_flow

- Loads external metadata
- Collects all data from all sources
- Combines different sources onto one unified stream
- Does measure normalization
- Does currency conversion
- Does row deduplication
- Does extra processing steps

Outputs:
- Denormalized data (local file)
- List of fiscal years in a separate resource (local file)
- Updates os package registry (if configured)

#### ./finalize_datapackage_flow_splitter
_(depends on ` ./denormalized_flow`)_

- Loads denormalized package
- Writes separate per-year filtered copies of the data

#### ./finalize_datapackage_flow
_(depends on ` ./finalize_datapackage_flow_splitter`)_

- Loads all resources from the `splitter` pipeline as well as the full denormalized dataset

Outputs:
- Stores results in S3 bucket
- Zip file with the datapackage (in case an S3 bucket is not configured)
- Updates os package registry (if configured)

#### ./dimension_flow_{hierarchy}
_(depends on ` ./denormalized_flow`)_

- Loads denormalized data
- Picks only _hierarchy_ columns
- Add auto-incrementing id column
- Remove duplicates

Outputs:
- Normalized hierarchy data (local file)

#### ./normalized_flow
_(depends on ` ./denormalized_flow` and all `./dimension_flow_{hierarchy}`)_

- Loads denormalized data as fact table
- Loads all normalized hierarchy data
- Creates babbage model
- Replaces all hierarchy columns in fact table with corresponding ids from normalized hierarchy tables

Outputs:
- Normalized fact table (local file)
- Updates os package registry (if configured)

#### ./dumper_flow_{hierarchy}
_(depends on corresponding `./dimension_flow_{hierarchy}`)_

- Loads normalized hierarchy data
- Fixes nulls in primary key (replacing them with empty strings)

Outputs
- Saves data as a single table in an SQL database

#### ./dumper_flow
_(depends on `./normalized_flow`)_

- Loads normalized fact table data
- Fixes nulls in primary key (replacing them with empty strings)

Outputs
- Saves data as a single table in an SQL database

#### ./dumper_flow_update_status
_(depends on `./dumper_flow`)_

Outputs
- Updates os package registry (if configured) that the package was loaded successfully

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)
