import re

import numpy as np

from ...sdk import *

from .. import _common
from .. import _login

from ._workbook import Workbook
from .._common import Status

from . import _workbook


def push(workbooks, *, path=None, label=None, datasource_map_folder=None, use_full_path=False,
         owner=None, access_control=None, override_max_interp=False, errors='raise',
         quiet=False, status=None):
    """
    Pushed workbooks into Seeq using a list of Workbook object definitions.

    Parameters
    ----------
    workbooks : list[Workbook]
        A list containing Workbook objects to be pushed into Seeq.

    path : str, default None
        A '>>'-delimited folder path to create to contain the workbooks. Note
        that a further subfolder hierarchy will be created to preserve the
        relative paths that the folders were in when they were searched for
        and pulled.

    label : str, default None
        A user-defined label that differentiates this push operation from
        others. Use this argument when you (or someone else) has already pushed
        a particular set of workbooks and you want to push a new copy of them.

    datasource_map_folder : str, default None
        A folder containing Datasource_Map_Xxxx_Yyyy_Zzzz.json files that can
        provides a means to map stored items (i.e., those originating from
        external datasources like OSIsoft PI) from one server to another. A
        default set of datasource map files is created during a pull/save
        sequence, and you can copy these default files to a folder, alter them,
        and then specify the folder as this argument.

    use_full_path : bool, default False
        If True, the original full path for an item is reconstructed, as
        opposed to the path that is relative to the Path property supplied to
        the spy.workbooks.search() call that originally helped create these
        workbook definitions. Note that this full path will still be inside
        the folder specified by the 'path' argument, if supplied.

    owner : str, default None
        Determines the ownership of pushed workbooks and folders.

        By default, the current owner will be preserved. If the content doesn't
        exist yet, the logged-in user will be the owner.

        All other options require that the logged-in user is an admin:

        If spy.workbooks.ORIGINAL_OWNER, ownership is assigned according to the
        original owner of the pulled content.

        If spy.workbooks.FORCE_ME_AS_OWNER, existing content will be
        reassigned to the logged-in user.

        If a username or a user's Seeq ID is supplied, that user will be
        assigned as owner.

        You may need to supply an appropriate datasource map if the usernames
        are different between the original and the target servers.

    access_control : str, default None
        Specifies of Access Control Lists should be treated, via the
        following keywords: add/replace,loose/strict

        If None, then no access control entries are pushed.
        If 'add', then existing access control entries will not be disturbed
          but new entries will be added.
        If 'replace', then existing access control entries will be removed
          and replaced with the entries from workbook definitions.

        If 'loose', then any unmapped users/groups from the workbook
          definitions will be silently ignored.
        If 'strict', then any unmapped users/groups will result in errors.

        Example: access_control='replace,loose'

    override_max_interp : bool, default False
        If True, then the Maximum Interpolation overrides from the source
        system will be written to the destination system.

    errors: {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame (errors='catalog' must be combined with
        status=<Status object>).

    quiet : bool
        If True, suppresses progress output.

    status : spy.Status
        If supplied, this Status object will be updated as the command
        progresses.

    """
    status = Status.validate(status, quiet)
    _common.validate_errors_arg(errors)

    status.update('Pushing workbooks', Status.RUNNING)

    item_map = dict()

    if not isinstance(workbooks, list):
        workbooks = [workbooks]

    # Sort such that Analyses are pushed before Topics, since the latter usually depends on the former
    remaining_workbooks = list()
    sorted_workbooks = sorted(list(workbooks), key=lambda w: w['Workbook Type'])
    for index in range(len(sorted_workbooks)):  # type: int
        workbook = sorted_workbooks[index]
        remaining_workbooks.append((index, workbook))
        status.df.at[index, 'ID'] = workbook.id if workbook.id else np.nan
        status.df.at[index, 'Name'] = workbook.name
        status.df.at[index, 'Workbook Type'] = workbook['Workbook Type']
        status.df.at[index, 'Count'] = 0
        status.df.at[index, 'Time'] = 0
        status.df.at[index, 'Result'] = 'Queued'

    datasource_maps = None if datasource_map_folder is None else Workbook.load_datasource_maps(datasource_map_folder)

    folder_id = _create_folder_path_if_necessary(path) if path is not None else None

    while len(remaining_workbooks) > 0:
        at_least_one_thing_pushed = False

        dependencies_not_found = list()
        for index, workbook in remaining_workbooks.copy():  # type: (int, Workbook)
            if not isinstance(workbook, Workbook):
                raise RuntimeError('"workbooks" argument contains a non Workbook item: %s' % workbook)

            try:
                status.reset_timer()

                status.current_df_index = index
                status.put('Count', 0)
                status.put('Time', 0)
                status.put('Result', 'Pushing')

                if datasource_maps is not None:
                    workbook.datasource_maps = datasource_maps

                workbook_folder_id = workbook.push_containing_folders(item_map, use_full_path, folder_id,
                                                                      owner, access_control)

                try:
                    workbook.push(folder_id=workbook_folder_id, item_map=item_map, label=label,
                                  owner=owner, access_control=access_control,
                                  override_max_interp=override_max_interp, status=status)

                    at_least_one_thing_pushed = True
                    remaining_workbooks.remove((index, workbook))
                    status.put('Result', 'Success')

                    if len(workbook.item_errors) > 0:
                        raise RuntimeError(workbook.item_errors_str)

                except _workbook.DependencyNotFound as e:
                    status.put('Count', 0)
                    status.put('Time', 0)
                    status.put('Result', 'Need dependency: %s' % e.message)

                    dependencies_not_found.append(str(e))

            except BaseException as e:
                status.exception(e)

                if errors == 'raise':
                    raise

                status.put('Result', _common.format_exception(e))

        if not at_least_one_thing_pushed:
            if errors == 'raise':
                raise RuntimeError('Could not find the following dependencies:\n%s\n'
                                   'Therefore, could not import the following workbooks:\n%s\n' %
                                   ('\n'.join(dependencies_not_found),
                                    '\n'.join([str(workbook) for workbook in workbooks])))

            break

    for index in range(len(workbooks)):
        workbook = workbooks[index]
        status.update('[%s/%s] Fixing up workbook-to-workbook links: %s' %
                      (index + 1, len(workbooks), str(workbook)), Status.RUNNING)
        workbook.push_fixed_up_workbook_links(item_map)

    unique_results = status.df['Result'].drop_duplicates()
    if len(unique_results) > 1 or (len(unique_results) == 1 and unique_results.iloc[0] != 'Success'):
        status.update('Errors encountered, look at Result column in returned DataFrame', Status.FAILURE)
    else:
        status.update('Push successful', Status.SUCCESS)

    return status.df


def _create_folder_path_if_necessary(path):
    folders_api = FoldersApi(_login.client)

    workbook_path = re.split(r'\s*>>\s*', path.strip())

    parent_id = None
    folder_id = None
    for i in range(0, len(workbook_path)):
        existing_content_id = None
        content_name = workbook_path[i]
        if parent_id:
            folders = folders_api.get_folders(filter='owner',
                                              folder_id=parent_id,
                                              limit=10000)  # type: FolderOutputListV1
        else:
            folders = folders_api.get_folders(filter='owner',
                                              limit=10000)  # type: FolderOutputListV1

        for content in folders.content:  # type: BaseAclOutput
            if content.type == 'Folder' and content_name == content.name:
                existing_content_id = content.id
                break

        if not existing_content_id:
            folder_input = FolderInputV1()
            folder_input.name = content_name
            folder_input.description = 'Created by Seeq Data Lab'
            folder_input.owner_id = _login.user.id
            folder_input.parent_folder_id = parent_id
            folder_output = folders_api.create_folder(body=folder_input)  # type: FolderOutputV1
            existing_content_id = folder_output.id

        parent_id = existing_content_id
        folder_id = existing_content_id

    return folder_id
