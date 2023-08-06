from typing import Type
# from typing_extensions import Protocol


class CanAssumeUserId:
    def with_user_id(self, user_id_query: 'Optional[UserIdQuery]' = None) -> 'CanAssumeUserId':
        return self

    def with_user_id_assumption(self) -> 'CanAssumeUserId':
        return self


class CanAssumeAuid:
    def with_auid(self) -> 'CanAssumeAuid':
        return self

    def with_auid_assumption(self) -> 'CanAssumeAuid':
        return self


if __name__ == '__main__':
    # Plugin registration
    from grapl_analyzerlib.nodes.process_node import ProcessQuery as _PQ


    class ProcessQuery(_PQ, CanAssumeUserId, CanAssumeAuid):
        pass

    # Code using plugins
    print(ProcessQuery().with_process_id().with_user_id())
