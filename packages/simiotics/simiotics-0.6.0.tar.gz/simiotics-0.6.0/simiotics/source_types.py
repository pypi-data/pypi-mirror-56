"""
This module enumerates and describes the source types supported by Simiotics dataset registries
"""

# Sources are where the samples from a dataset actually reside. The following types are the ones
# that Simiotics can meaningfully interact with.
SOURCE_UNKNOWN = 'UNKNOWN'
SOURCE_INTRINSIC = 'INTRINSIC'
SOURCE_LOCAL = 'LOCAL'
SOURCE_HTTP = 'HTTP'
SOURCE_S3 = 'S3'
SOURCE_GCS = 'GCS'

SOURCE_TYPES = {
    SOURCE_UNKNOWN: 'Unknown source',
    SOURCE_INTRINSIC: 'Content for a sample from this source completely describes the sample',
    SOURCE_LOCAL: 'Content for a sample from this source is a file system path',
    SOURCE_HTTP: 'Content for a sample from this source is a HTTP URL',
    SOURCE_S3: 'Content for a sample from this source is a AWS S3 path',
    SOURCE_GCS: 'Content for a sample from this source is a Google Cloud Storage path',
}
