from typing import Union, Dict, AnyStr, Type, List

from .config import CONFIG

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'get_branch_types',
    'get_other_branch_type',
    'get_all_branch_types',
    'get_unreleased',
    'get_other_branch_type_key',
    'get_unreleased_key',
    'get_unreleased_key_label',
    'get_ignore_commits_exact_words',
)


def get_branch_types() -> Dict[str, str]:
    """Get branch types.

    :return:
    """
    return dict(CONFIG['BranchTypes'])


def get_other_branch_type() -> Dict[str, str]:
    """Get other branch type.

    :return:
    """
    return dict(CONFIG['OtherBranchType'])


def get_other_branch_type_key() -> str:
    return [k for k in get_other_branch_type().keys()][0]


def get_all_branch_types() -> Dict[str, str]:
    branch_types = get_branch_types()
    branch_types.update(get_other_branch_type())
    return branch_types


def get_unreleased():
    """Get unreleased.

    :return:
    """
    return dict(CONFIG['Unreleased'])


def get_unreleased_key() -> str:
    return [k for k in get_unreleased().keys()][0]


def get_unreleased_label() -> str:
    return [k for k in get_unreleased().keys()][1]


def get_unreleased_key_label():
    """Get unreleased.

    :return:
    """
    return [
        (key, value) for key, value in dict(CONFIG['Unreleased']).items()
    ][0]


def get_ignore_commits_exact_words() -> List[str]:
    """Get ignore commits exact words.

    :return:
    """
    return CONFIG['IgnoreCommits']['exact'].split('\n')
