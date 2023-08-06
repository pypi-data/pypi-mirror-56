from mail_relay.daemon.export_state import ExportState
from pvHelpers.request import ExportRequest
from pvHelpers.utils import jdumps, jloads


class ExportStateBucket:
    NAME = u'export_state'
    CURRENT_VERSION = 0

    @staticmethod
    def key():
        return u'export_state'

    @staticmethod
    def serialize(export_state, bucket_version):
        if bucket_version == 0:
            return ExportStateBucket._serialize_v0(export_state)
        else:
            raise ValueError(u'unsupported bucket bucket_version {}'.format(bucket_version))

    @staticmethod
    def deserialize(blob, bucket_version):
        if bucket_version == 0:
            return ExportStateBucket._deserialize_v0(blob)
        else:
            raise ValueError(u'unsupported bucket bucket_version {}'.format(bucket_version))

    @staticmethod
    def _serialize_v0(export_state):
        return jdumps({
            'request': export_state.request.to_dict(),
            'approver_signatures': export_state.approver_signatures,
            'export_group': export_state.export_group
        })

    @staticmethod
    def _deserialize_v0(blob):
        j = jloads(blob)
        r = j['request']
        approvers_info = {
            id_: {'approver_shards': {}, 'approver_signature': s} for id_, s in j['approver_signatures'].iteritems()}

        return ExportState(
            ExportRequest(r['request_payload'], r['signature'], r['request_id']), j['export_group'], approvers_info)
