from ._version import get_versions

from normality import normalize

from .mappings import mappings


__version__ = get_versions()["version"]
del get_versions


def to_shortname(name):
    # Remove Hector-style extensions.
    name = name.replace("_emissions", "").replace("_concentrations", "")
    normalized_name = normalize(name).replace(" ", "")
    try:
        return mappings[normalized_name]
    except KeyError:
        return name
