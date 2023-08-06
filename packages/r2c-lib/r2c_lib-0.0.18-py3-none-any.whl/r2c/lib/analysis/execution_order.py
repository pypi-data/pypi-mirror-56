from typing import List, Optional, Union

import attr

from r2c.lib.registry import RegistryData
from r2c.lib.specified_analyzer import SpecifiedAnalyzer


@attr.s(auto_attribs=True)
class ExecutionEntry:
    """Indicates which analyzer should be executed."""

    analyzer: SpecifiedAnalyzer
    # If true, this should be run in 'interactive' mode.
    interactive: bool = False


@attr.s(auto_attribs=True)
class ExecutionOrder:
    fetch_phase: List[ExecutionEntry]
    analysis_phase: List[ExecutionEntry]

    def all_phases(self) -> List[ExecutionEntry]:
        return self.fetch_phase + self.analysis_phase

    @classmethod
    def compute(
        cls,
        registry_data: RegistryData,
        analyzer: SpecifiedAnalyzer,
        code_fetcher: Optional[SpecifiedAnalyzer] = None,
        interactive: Optional[Union[str, int]] = None,
    ) -> "ExecutionOrder":
        """Resolves which analyzers should be executed, and in which order.

        `interactive` specifies whether to run an analyzer interactively. If it's a
        string, analyzers whose name contains that string are interactive. If an
        int, then it's used as an offset into the list of execution entries.
        (Negative numbers are OK.)

        Raises an Exception if interactive is not None, but no analyzers matched
        it.
        """
        # TODO: Deduplicate so if an analyzer shows up in both, we don't wind
        # up running it in both phases.
        fetcher_deps = registry_data.sorted_deps(code_fetcher) if code_fetcher else []
        analyzer_deps = registry_data.sorted_deps(analyzer)
        all_deps = analyzer_deps + fetcher_deps

        if isinstance(interactive, int) and interactive < 0:
            # Deal with negative offsets.
            interactive += len(all_deps)

        def is_interactive(index: int, dep: SpecifiedAnalyzer) -> bool:
            if isinstance(interactive, str):
                return interactive in dep.versioned_analyzer.name
            elif isinstance(interactive, int):
                return interactive == index
            else:
                return False

        fetch_phase = [
            ExecutionEntry(dep, interactive=is_interactive(index, dep))
            for index, dep in enumerate(fetcher_deps)
        ]
        analysis_phase = [
            ExecutionEntry(
                dep, interactive=is_interactive(index + len(fetch_phase), dep)
            )
            for index, dep in enumerate(analyzer_deps)
        ]

        if interactive is not None and not any(
            entry.interactive for entry in fetch_phase + analysis_phase
        ):
            raise Exception(
                f"An interactive analyzer was requested via specifier `{interactive}`, but no matching analyzer was run!"
            )
        return cls(fetch_phase=fetch_phase, analysis_phase=analysis_phase)
