import re

import pandas as pd
import numpy as np

from seeq.sdk43 import *

from . import _common
from . import _login
from . import _push

from ._common import Status

from seeq import spy


def search(query, *, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH, recursive=True, quiet=False,
           status=None):
    """
    Issues a query to the Seeq Server to retrieve metadata for signals,
    conditions, scalars and assets. This metadata can be used to retrieve
    samples, capsules for a particular time range.

    Parameters
    ----------
    query : {dict, pandas.DataFrame}
        A mapping of property / match-criteria pairs. Match criteria uses
        the same syntax as the Data tab in Seeq. Available options are:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        Name                Name of the item
        Path                Asset tree path of the item
        Type                The item type. One of 'Signal', 'Condition',
                              'Scalar', 'Asset', 'Histogram' or 'Metric'
        Description         The description of th item
        Datasource Name     The name of the datasource
        Datasource ID       The datasource ID
        Datasource Class    The datasource class
        Cache Enabled       If data caching is enabled
        Archived            If the item is archived
        Scoped To           The Seeq ID of the scoped workbook. Is overridden
                              by the 'workbook' argument
        =================== ===================================================

    all_properties : bool, default False
        True if all item properties should be retrieved. This currently makes
        the search operation much slower as retrieval of properties for an item
        requires a separate call.

    workbook : {str, None}
        A path string (with ' >> ' delimiters) or an ID to indicate a workbook
        to which the scope of the search should be limited. Note that globally
        scoped items will still be returned. The ID for a workbook is visible
        in the URL of Seeq Workbench, directly after the "workbook/" part.

    recursive : bool, default True
        If True, searches that include a Path entry will include items at and
        below the specified location in an asset tree. If False, the query
        dictionary can only contain a Path entry and only items at the
        specified level will be returned.

    quiet : bool, default False
        If True, suppresses progress output.

    status : spy.Status, optional
        If supplied, this Status object will be updated as the command
        progresses.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with rows for each item found and columns for each
        property.

    Examples
    --------
    Search for signals with the name 'Humid' on the asset tree under
    'Example >> Cooling Tower 1', retrieving all properties on the results:

    >>> spy.search({'Name': 'Humid', 'Path': 'Example >> Cooling Tower 1'}, all_properties=True)

    Using a pandas.DataFrame as the input:

    >>> my_items = pd.DataFrame(
    >>>     {'Name': ['Area A_Temperature', 'Area B_Compressor Power', 'Optimize' ],
    >>>      'Datasource Name': 'Example Data'})
    >>> spy.search(my_items)
    """
    status = Status.validate(status, quiet)
    try:
        return _search(query, all_properties=all_properties, workbook=workbook, recursive=recursive, quiet=quiet,
                       status=status)

    except KeyboardInterrupt:
        status.update('Search canceled', Status.CANCELED)


def _search(query, *, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH, recursive=True, quiet=False,
            status=None):
    status = Status.validate(status, quiet)

    items_api = ItemsApi(_login.client)
    trees_api = TreesApi(_login.client)

    if isinstance(query, pd.DataFrame):
        queries = query.to_dict(orient='records')
        comparison = '=='
    else:
        queries = [query]
        comparison = '~='

    metadata = list()
    columns = list()
    warnings = list()

    status.metrics({
        'Results': {
            'Time': 0,
            'Count': 0
        }
    })
    status.update('Initializing', Status.RUNNING)

    timer = _common.timer_start()

    def _add_to_dict(d, _key, val):
        d[_key] = _common.none_to_nan(val)

        # We want the columns to appear in a certain order (the order we added them in) for readability
        if _key not in columns:
            columns.append(_key)

    def _get_warning_string():
        if len(warnings) == 0:
            return ''

        return '<em><br>Warning:<br>%s</em>' + '<br>'.join(warnings)

    def _add_all_properties(_id, _prop_dict):
        _item = items_api.get_item_and_all_properties(id=_id)  # type: ItemOutputV1
        for prop in _item.properties:  # type: PropertyOutputV1
            _add_to_dict(_prop_dict, prop.name, prop.value)

        # Name and Type don't seem to appear in additional properties
        _add_to_dict(_prop_dict, 'Name', _item.name)
        _add_to_dict(_prop_dict, 'Type', _item.type)

        if _item.type == 'CalculatedSignal':
            signals_api = SignalsApi(_login.client)
            signal_output = signals_api.get_signal(id=_item.id)  # type: SignalOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (fpo.name, fpo.item.id if fpo.item else fpo.formula) for fpo in signal_output.parameters
            ])

        if _item.type == 'CalculatedCondition':
            conditions_api = ConditionsApi(_login.client)
            condition_output = conditions_api.get_condition(id=_item.id)  # type: ConditionOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (fpo.name, fpo.item.id if fpo.item else fpo.formula) for fpo in condition_output.parameters
            ])

        if _item.type == 'CalculatedScalar':
            scalars_api = ScalarsApi(_login.client)
            scalar_output = scalars_api.get_scalar(id=_item.id)  # type: CalculatedItemOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (fpo.name, fpo.item.id if fpo.item else fpo.formula) for fpo in scalar_output.parameters
            ])

        return _prop_dict

    for _query in queries:
        if 'ID' in _query:
            # If ID is specified, short-circuit everything and just get the item directly
            metadata.append(_add_all_properties(_query['ID'], dict()))
            continue

        if not recursive:
            if len(_query) != 1 or 'Path' not in _query:
                raise RuntimeError(
                    'When recursive=False, query dictionary must contain only a Path entry. Use Pandas operations to '
                    'on the returned DataFrame to pare down results.')

        allowed_properties = ['Type', 'Name', 'Description', 'Path', 'Asset', 'Datasource Class', 'Datasource ID',
                              'Datasource Name', 'Cache Enabled', 'Archived', 'Scoped To']

        for key, value in _query.items():
            if key not in allowed_properties:
                warnings.append('Property "%s" is not an indexed property and will be ignored. Use any of the '
                                'following searchable properties and then filter further using DataFrame '
                                'operations:\n"%s"' % (key, '", "'.join(allowed_properties)))

        item_types = list()
        clauses = list()

        if _common.present(_query, 'Type'):
            item_type_specs = list()
            if isinstance(_query['Type'], list):
                item_type_specs.extend(_query['Type'])
            else:
                item_type_specs.append(_query['Type'])

            for item_type_spec in item_type_specs:
                if item_type_spec == 'Signal':
                    item_types.extend(['StoredSignal', 'CalculatedSignal'])
                elif item_type_spec == 'Condition':
                    item_types.extend(['StoredCondition', 'CalculatedCondition'])
                elif item_type_spec == 'Scalar':
                    item_types.extend(['StoredScalar', 'CalculatedScalar'])
                else:
                    item_types.append(item_type_spec)

            del _query['Type']

        if _common.present(_query, 'Datasource Name'):
            _filters = ['Name == %s' % _common.get(_query, 'Datasource Name')]
            if _common.present(_query, 'Datasource ID'):
                _filters.append('Datasource ID == %s' % _common.get(_query, 'Datasource ID'))
            if _common.present(_query, 'Datasource Class'):
                _filters.append('Datasource Class == %s' % _common.get(_query, 'Datasource Class'))

            datasource_results = items_api.search_items(filters=[' && '.join(_filters)],
                                                        types=['Datasource'],
                                                        limit=100000)  # type: ItemSearchPreviewPaginatedListV1

            if len(datasource_results.items) > 1:
                raise RuntimeError(
                    'Multiple datasources found that match "%s"' % _common.get(_query, 'Datasource Name'))
            elif len(datasource_results.items) == 0:
                raise RuntimeError('No datasource found that matches "%s"' % _common.get(_query, 'Datasource Name'))
            else:
                datasource = datasource_results.items[0]  # type: ItemSearchPreviewV1
                _query['Datasource ID'] = items_api.get_property(id=datasource.id, property_name='Datasource ID').value
                _query['Datasource Class'] = items_api.get_property(id=datasource.id,
                                                                    property_name='Datasource Class').value

            del _query['Datasource Name']

        # Store these off for use during Path filtering
        datasource_dict = {key: value for key, value in _query.items() if key in ['Datasource Class', 'Datasource ID']}

        for prop_name in ['Name', 'Description', 'Datasource Class', 'Datasource ID', 'Data ID']:
            if prop_name in _query and _query[prop_name] is not None:
                clauses.append(prop_name + comparison + _query[prop_name])
                del _query[prop_name]

        filters = [' && '.join(clauses)] if len(clauses) > 0 else []

        kwargs = {
            'filters': filters,
            'types': item_types,
            'limit': _common.DEFAULT_SEARCH_PAGE_SIZE
        }

        if workbook:
            if _common.is_guid(workbook):
                workbook_id = _common.sanitize_guid(workbook)
            else:
                workbook_id = _push.reify_workbook(workbook, create=False)

            if workbook_id:
                kwargs['scope'] = workbook_id
            elif workbook != _common.DEFAULT_WORKBOOK_PATH:
                raise RuntimeError('Workbook "%s" not found, or is not accessible by you' % workbook)

        if 'Scoped To' in _query and _query['Scoped To'] is not None:
            kwargs['scope'] = _query['Scoped To']
            kwargs['filters'].append('@excludeGloballyScoped')

        if _common.present(_query, 'Asset') and not _common.present(_query, 'Path'):
            raise RuntimeError('"Path" query parameter must be present when "Asset" parameter present')

        path_to_query = None
        if 'Path' in _query:
            path_to_query = _query['Path']
            if 'Asset' in _query:
                path_to_query = path_to_query + ' >> ' + _query['Asset']

        def _do_search(offset):
            kwargs['offset'] = offset
            status.metrics({
                'Results': {
                    'Time': _common.timer_elapsed(timer),
                    'Count': len(metadata)
                }
            })
            status.update('Querying Seeq Server for items' + _get_warning_string(), Status.RUNNING)

            if recursive:
                return items_api.search_items(**kwargs)
            else:
                kwargs2 = {
                    'id': kwargs['asset'],
                    'offset': kwargs['offset'],
                    'limit': kwargs['limit']
                }

                if 'scope' in kwargs:
                    kwargs2['scoped_to'] = kwargs['scope']

                return trees_api.get_tree(**kwargs2)

        def _gather_results_item_search(result):
            item_search_preview = result  # type: ItemSearchPreviewV1
            prop_dict = dict()

            _add_to_dict(prop_dict, 'ID', item_search_preview.id)
            if len(item_search_preview.ancestors) > 1:
                _add_to_dict(prop_dict, 'Path', ' >> '.join([a.name for a in item_search_preview.ancestors[0:-1]]))
                _add_to_dict(prop_dict, 'Asset', item_search_preview.ancestors[-1].name)
            elif len(item_search_preview.ancestors) == 1:
                _add_to_dict(prop_dict, 'Path', np.nan)
                _add_to_dict(prop_dict, 'Asset', item_search_preview.ancestors[0].name)

            _add_to_dict(prop_dict, 'Name', item_search_preview.name)
            _add_to_dict(prop_dict, 'Description', item_search_preview.description)
            _add_to_dict(prop_dict, 'Type', item_search_preview.type)
            uom = item_search_preview.value_unit_of_measure if item_search_preview.value_unit_of_measure \
                else item_search_preview.source_value_unit_of_measure
            _add_to_dict(prop_dict, 'Value Unit Of Measure', uom)
            datasource_item_preview = item_search_preview.datasource  # type: ItemPreviewV1
            _add_to_dict(prop_dict, 'Datasource Name',
                         datasource_item_preview.name if datasource_item_preview else None)
            if all_properties:
                _add_all_properties(item_search_preview.id, prop_dict)

            metadata.append(prop_dict)

        def _gather_results_get_tree(result):
            tree_item_output = result  # type: TreeItemOutputV1
            prop_dict = dict()

            _add_to_dict(prop_dict, 'ID', tree_item_output.id)
            path_parts = re.split(r'\s*>>\s*', path_to_query)
            if len(path_parts) > 1:
                _add_to_dict(prop_dict, 'Path', ' >> '.join(path_parts[0:-1]))
                _add_to_dict(prop_dict, 'Asset', path_parts[-1])
            elif len(path_parts) == 1:
                _add_to_dict(prop_dict, 'Path', np.nan)
                _add_to_dict(prop_dict, 'Asset', path_parts[0])

            _add_to_dict(prop_dict, 'Name', tree_item_output.name)
            _add_to_dict(prop_dict, 'Description', tree_item_output.description)
            _add_to_dict(prop_dict, 'Type', tree_item_output.type)
            _add_to_dict(prop_dict, 'Value Unit Of Measure', tree_item_output.value_unit_of_measure)
            if all_properties:
                _add_all_properties(tree_item_output.id, prop_dict)

            metadata.append(prop_dict)

        def _go():
            if recursive:
                _iterate_over_output(_do_search, 'items', _gather_results_item_search)
            else:
                _iterate_over_output(_do_search, 'children', _gather_results_get_tree)

        if not _common.present(_query, 'Path'):
            _go()
        else:
            def _process_path_part(_path, asset_id=None):
                path_parts = re.split(r'\s*>>\s*', _path)

                path_part = path_parts[0]

                tree_kwargs = dict()
                tree_kwargs['limit'] = kwargs['limit']
                tree_kwargs['offset'] = 0

                if 'scope' in kwargs:
                    tree_kwargs['scoped_to'] = kwargs['scope']

                while True:
                    if not asset_id:
                        tree_output = trees_api.get_tree_root_nodes(**tree_kwargs)  # type: AssetTreeOutputV1
                    else:
                        tree_kwargs['id'] = asset_id
                        tree_output = trees_api.get_tree(**tree_kwargs)  # type: AssetTreeOutputV1

                    for child in tree_output.children:  # type: TreeItemOutputV1
                        if not asset_id:
                            # We only filter out datasource at the top level, in case the tree is mixed
                            datasource_ok = True
                            child_item_output = items_api.get_item_and_all_properties(id=child.id)  # type: ItemOutputV1
                            for _prop in ['Datasource Class', 'Datasource ID']:
                                if _prop in datasource_dict and datasource_dict[_prop]:
                                    _p_list = [_p.value for _p in child_item_output.properties if
                                               _p.name == _prop]
                                    if len(_p_list) == 0 or _p_list[0] != datasource_dict[_prop]:
                                        datasource_ok = False

                            if not datasource_ok:
                                continue

                        if _common.does_query_fragment_match(path_part, child.name):
                            if len(path_parts) == 1:
                                kwargs['asset'] = child.id
                                _go()
                            else:
                                _process_path_part(' >> '.join(path_parts[1:]), child.id)

                    if len(tree_output.children) < tree_kwargs['limit']:
                        break

                    tree_kwargs['offset'] += tree_kwargs['limit']

            _process_path_part(path_to_query)

    status.metrics({
        'Results': {
            'Time': _common.timer_elapsed(timer),
            'Count': len(metadata)
        }
    })
    status.update('Query successful' + _get_warning_string(), Status.SUCCESS)

    return pd.DataFrame(data=metadata, columns=columns)


def _iterate_over_output(output_func, collection_name, action_func):
    offset = 0
    while True:
        output = output_func(offset)

        collection = getattr(output, collection_name)

        for item in collection:
            action_func(item)

        if len(collection) != output.limit:
            break

        offset += output.limit
