#!/usr/bin/env python3

from aws_cdk import (
    core,
    cx_api
)

import jsii


@jsii.implements(core.IAspect)
class tag_setter:
    def __init__(self, team_name: str) -> None:
        self.team_name = team_name

    def visit(self, construct: core.IConstruct) -> None:
        core.Tag.add(construct, "TeamName", self.team_name)
        for child in construct.node.children:
            child.node.apply_aspect(tag_setter(team_name=self.team_name))


class WaltersCoApp(core.App):
    def __init__(self, team_name: str):
        self.team_name = team_name
        super().__init__()

    def synth(self) -> cx_api.CloudAssembly:
        for child in self.node.children:
            child.node.apply_aspect(tag_setter(team_name=self.team_name))
        return jsii.invoke(self, "synth", [])

        # The code that defines your stack goes here
