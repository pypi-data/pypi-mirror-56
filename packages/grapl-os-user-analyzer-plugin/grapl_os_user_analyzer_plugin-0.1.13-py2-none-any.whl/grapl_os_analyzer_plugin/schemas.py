from grapl_analyzerlib.schemas import ProcessSchema, NodeSchema


class AuidSchema(NodeSchema):
    def __init__(self):
        super(AuidSchema, self).__init__()
        (
            self
            .with_int_prop('auid')
        )

    @staticmethod
    def self_type() -> str:
        return 'Auid'


class AuidAssumptionSchema(NodeSchema):
    def __init__(self):
        super(AuidAssumptionSchema, self).__init__()
        (
            self
            .with_int_prop('assumed_timestamp')
            .with_int_prop('assuming_process_id')
            .with_forward_edge('assumed_auid', AuidSchema)
            .with_forward_edge('assuming_process', ProcessSchema)
        )


    @staticmethod
    def self_type() -> str:
        return 'AuidAssumption'


class UserIdSchema(NodeSchema):
    def __init__(self):
        super(UserIdSchema, self).__init__()
        (
            self
                .with_int_prop('user_id')
        )

    @staticmethod
    def self_type() -> str:
        return 'UserId'


class UserIdAssumptionSchema(NodeSchema):
    def __init__(self):
        super(UserIdAssumptionSchema, self).__init__()
        (
            self
                .with_int_prop('assumed_timestamp')
                .with_int_prop('assuming_process_id')
                .with_forward_edge('assumed_user_id', UserIdSchema)
                .with_forward_edge('assuming_process', ProcessSchema)
        )


    @staticmethod
    def self_type() -> str:
        return 'UserIdAssumption'