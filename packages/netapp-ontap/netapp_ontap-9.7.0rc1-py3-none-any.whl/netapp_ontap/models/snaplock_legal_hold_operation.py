# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

Manages the legal-hold operations for the specified litigation ID.
### Examples
1. Adds a Legal-Hold.
   <br/>
   ```
   POST "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations" '{"lh_operation.type" : "begin", "lh_operation.path" : "/a.txt"}'
   ```
   <br/>
2. Removes a Legal-Hold.
   <br/>
   ```
   POST "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations" '{"lh_operation.type" : "end", "lh_operation.path" : "/a.txt"}'
   ```
   <br/>
"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["SnaplockLegalHoldOperation", "SnaplockLegalHoldOperationSchema"]
__pdoc__ = {
    "SnaplockLegalHoldOperationSchema.resource": False,
    "SnaplockLegalHoldOperation": False,
}


class SnaplockLegalHoldOperationSchema(ResourceSchema):
    """The fields of the SnaplockLegalHoldOperation object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the snaplock_legal_hold_operation. """

    id = fields.Integer(data_key="id")
    r""" Operation ID.

Example: 16842759 """

    num_files_failed = fields.Str(data_key="num_files_failed")
    r""" Specifies the number of files on which legal-hold operation failed.

Example: 0 """

    num_files_processed = fields.Str(data_key="num_files_processed")
    r""" Specifies the number of files on which legal-hold operation was successful.

Example: 30 """

    num_files_skipped = fields.Str(data_key="num_files_skipped")
    r""" Specifies the number of files on which legal-hold begin operation was skipped. The legal-hold begin operation is skipped on a file if it is already under hold for a given litigation.

Example: 10 """

    num_inodes_ignored = fields.Str(data_key="num_inodes_ignored")
    r""" Specifies the number of inodes on which the legal-hold operation was not attempted because they were not regular files.

Example: 10 """

    path = fields.Str(data_key="path")
    r""" Specifies the path on which legal-hold operation is applied.

Example: /dir1 """

    state = fields.Str(data_key="state")
    r""" Specifies the status of legal-hold operation.

Valid choices:

* in_progress
* failed
* aborting
* completed """

    type = fields.Str(data_key="type")
    r""" Specifies the type of legal-hold operation.

Valid choices:

* begin
* end """

    @property
    def resource(self):
        return SnaplockLegalHoldOperation

    @property
    def patchable_fields(self):
        return [
            "type",
        ]

    @property
    def postable_fields(self):
        return [
            "path",
        ]


class SnaplockLegalHoldOperation(Resource):  # pylint: disable=missing-docstring

    _schema = SnaplockLegalHoldOperationSchema
