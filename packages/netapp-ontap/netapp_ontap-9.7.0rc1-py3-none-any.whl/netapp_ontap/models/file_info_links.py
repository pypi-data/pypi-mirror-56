# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["FileInfoLinks", "FileInfoLinksSchema"]
__pdoc__ = {
    "FileInfoLinksSchema.resource": False,
    "FileInfoLinks": False,
}


class FileInfoLinksSchema(ResourceSchema):
    """The fields of the FileInfoLinks object"""

    files = fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="files")
    r""" The files field of the file_info_links. """

    self_ = fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="self")
    r""" The self_ field of the file_info_links. """

    @property
    def resource(self):
        return FileInfoLinks

    @property
    def patchable_fields(self):
        return [
            "files",
            "self_",
        ]

    @property
    def postable_fields(self):
        return [
            "files",
            "self_",
        ]


class FileInfoLinks(Resource):  # pylint: disable=missing-docstring

    _schema = FileInfoLinksSchema
