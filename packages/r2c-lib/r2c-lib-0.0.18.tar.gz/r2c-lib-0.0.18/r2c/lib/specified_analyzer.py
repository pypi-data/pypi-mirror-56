import json
from typing import Any, Dict, Optional

import attr
from mypy_extensions import TypedDict

from r2c.lib.versioned_analyzer import VersionedAnalyzer, VersionedAnalyzerJson


class SpecifiedAnalyzerJson(TypedDict):
    versionedAnalyzer: VersionedAnalyzerJson
    parameters: Dict[str, str]


def _initialize_parameters(params: Optional[Dict[str, str]]) -> Dict[str, str]:
    return params or {}


# We have to say `hash=False` so attrs won't 'helpfully' delete our hashing
# implementation.
@attr.s(auto_attribs=True, hash=False)
class SpecifiedAnalyzer:
    """
        Class to represent a specific instance of an analyzer. This includes
        any parameters.

        Contains all necessary information to run an analyzer minus the target of analysis
    """

    versioned_analyzer: VersionedAnalyzer
    # We need to use frozen sets because otherwise we can't really hash this,
    # since dicts are unhashable.
    parameters: Dict[str, str] = attr.ib(converter=_initialize_parameters, factory=dict)

    @classmethod
    def from_json_str(cls, json_str: str) -> "SpecifiedAnalyzer":
        obj = json.loads(json_str)
        return cls.from_json(obj)

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]) -> "SpecifiedAnalyzer":
        if "parameters" in json_obj:
            parameters = json_obj["parameters"]
        else:
            parameters = {}
        va = VersionedAnalyzer.from_json(json_obj["versionedAnalyzer"])
        return cls(va, parameters)

    def to_json(self) -> SpecifiedAnalyzerJson:
        return {
            "versionedAnalyzer": self.versioned_analyzer.to_json(),
            "parameters": self.parameters,
        }

    def __hash__(self) -> int:
        return hash(
            (
                "an arbitrary salt",
                self.versioned_analyzer,
                json.dumps(self.parameters, sort_keys=True),
            )
        )
