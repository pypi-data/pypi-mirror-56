#!/usr/bin/env python

import logging
import shutil

import attr

from r2c.lib.analysis.mount_manager import MountManager
from r2c.lib.analysis.output_storage import OutputStorage
from r2c.lib.input import AnalyzerInput
from r2c.lib.jobdef import CacheKey
from r2c.lib.manifest import AnalyzerOutputType
from r2c.lib.registry import RegistryData
from r2c.lib.specified_analyzer import SpecifiedAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@attr.s(auto_attribs=True, frozen=True)
class DependencyMounter:
    """Mounts the dependencies of an analyzer.

    This class is responsible for figuring out where inside a MountManager's
    input directory each dependency should go and then fetching those
    dependencies from storage.
    """

    _registry_data: RegistryData
    output_storage: OutputStorage

    def mount_all(
        self,
        analyzer: SpecifiedAnalyzer,
        input: AnalyzerInput,
        mount_manager: MountManager,
    ) -> None:
        """Mounts all dependencies.

        Raises an exception if a dependency failed to mount.
        """
        logger.info(f"Mounting dependencies for {analyzer} on {input}")

        for dependency in self._registry_data.get_direct_dependencies(
            analyzer.versioned_analyzer
        ):
            if not self._mount(dependency, input, mount_manager):
                raise Exception(f"Error while mounting output of {dependency}")

    def _mount(
        self,
        dependency: SpecifiedAnalyzer,
        input: AnalyzerInput,
        mount_manager: MountManager,
    ) -> bool:
        """Mounts a single dependency."""
        cache_key = CacheKey(analyzer=dependency, input=input)
        logger.info(f"Mounting output of {dependency}")
        output_type = self._registry_data.manifest_for(
            dependency.versioned_analyzer
        ).output_type
        input_dir = mount_manager.input_dir()

        if output_type.has_json():
            target = input_dir / f"{dependency.versioned_analyzer.name}.json"
            fetched = self.output_storage.fetch_analyzer_output(
                cache_key, AnalyzerOutputType.json
            )
            if fetched is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(fetched, target)
            else:
                return False

        if output_type.has_filesystem():
            fetched = self.output_storage.fetch_analyzer_output(
                cache_key, AnalyzerOutputType.filesystem
            )
            if fetched is not None:
                shutil.copytree(fetched, input_dir / dependency.versioned_analyzer.name)
            else:
                return False

        return True

    def contains(self, cache_key: CacheKey) -> bool:
        """Returns if we already have output for the given analyzer/input. """
        output_type = self._registry_data.manifest_for(
            cache_key.analyzer.versioned_analyzer
        ).output_type

        return self.output_storage.contains(cache_key, output_type)
