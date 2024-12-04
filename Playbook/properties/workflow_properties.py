class WorkflowProperties:
    id: str
    team_id: str
    name: str

    def __init__(self, id, team_id, name):
        self.id = id
        self.team_id = team_id
        self.name = name
