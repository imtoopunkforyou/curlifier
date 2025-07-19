import pytest

from curlifier.builders.configurator import ConfigBuilder
from curlifier.structures.commands import CommandsConfigureEnum


@pytest.mark.parametrize('location', (True, False))
@pytest.mark.parametrize('verbose', (True, False))
@pytest.mark.parametrize('silent', (True, False))
@pytest.mark.parametrize('insecure', (True, False))
@pytest.mark.parametrize('include', (True, False))
@pytest.mark.parametrize('build_short', (True, False))
def test_config_builder(
    location,
    verbose,
    silent,
    insecure,
    include,
    build_short,
):
    builder = ConfigBuilder(
        location=location,
        verbose=verbose,
        silent=silent,
        insecure=insecure,
        include=include,
        build_short=build_short,
    )
    builded: str = builder.build()

    if location:
        assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) in builded
    else:
        assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) not in builded

    if verbose:
        assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) in builded
    else:
        assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) not in builded

    if silent:
        assert CommandsConfigureEnum.SILENT.get(shorted=build_short) in builded
    else:
        assert CommandsConfigureEnum.SILENT.get(shorted=build_short) not in builded

    if insecure:
        assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) in builded
    else:
        assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) not in builded

    if include:
        assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) in builded
    else:
        assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) not in builded
