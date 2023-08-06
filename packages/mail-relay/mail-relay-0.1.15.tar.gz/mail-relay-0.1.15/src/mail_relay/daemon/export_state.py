from pvHelpers.request.export_local_state import ExportRequestLocalState
from pvHelpers.utils import CaseInsensitiveDict


class ExportState(ExportRequestLocalState):
    def __init__(self, request, export_group, approvers_info):
        super(ExportState, self).__init__(
            request, approvers_info, ExportRequestLocalState.INIT, u'', export_group)

    @property
    def valid_for(self):
        return 60 * 60 * 10

    @property
    def export_group(self):
        return self.group_info

    @property
    def approver_signatures(self):
        return CaseInsensitiveDict(
            {id_: info['approver_signature'] for id_, info in self.approvers_info.iteritems()})

    @property
    def members(self):
        return list(set([u['user_id'] for u in self.request.data['users']]))
