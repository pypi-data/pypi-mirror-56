"""
Matplotlib axes customization wrapper.
"""

from collections import Callable, OrderedDict
from functools import partial

import matplotlib.dates
import matplotlib.ticker

from . import client, processing, transforms, utils
from .constants import SUPPORTED_CUSTOMIZERS
from .exceptions import ChartError


def set_axis_locator(axis, params=None, **kwargs):
    """
    Set axis locator.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param params: Axis locator parameters.
    :type params: dict, optional

    Example config:

    .. code-block:: python

        'locator': {
            'x': {
                'major': {
                    'name': 'MaxNLocator',
                    'params': [],
                    'keyword_params': {

                    } 
                }
            }
        }
    """
    config = params or {}
    axis_methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
    }
    formatter_methods = {
        'major': 'set_major_locator',
        'minor': 'set_minor_locator',
    }
    instances = {}

    for key, value in config.items():
        if key not in axis_methods:
            continue
        for which, data in value.items():
            if which not in formatter_methods:
                continue
            name = data.get('name')
            if name is None:
                raise ChartError(
                    'Parameter name is required if using axis locator')

            for attr in [matplotlib.ticker, matplotlib.dates]:
                locator = getattr(attr, name, None)
                if locator:
                    break

            if locator is None:
                raise ChartError('Unsupported locator class {}'.format(name))

            gca = getattr(axis, axis_methods[key])()
            instance = locator(*data.get('params', []),
                               **data.get('keyword_params', {}))
            instances.update({key: {which: instance}})
            getattr(gca, formatter_methods[which])(instance)

    return instances


def set_axis_formatter(axis, params=None, **kwargs):
    """
    Set axis formatter.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param params: Axis formatter parameters.
    :type params: dict, optional

    Example config:

    .. code-block:: python

        'formatter': {
            'x': {
                'major': {
                    'format': '%.3f'
                },
                'minor': {
                    'name': 'PercentFormatter',
                    'params': [],
                    'keyword_params': {

                    }
                }
            }
        }

    Default formatter is FormatStrFormatter and it reads 'format' value. Other
    formatter is specified with params and keyword_params to pass these values
    into formatter class.
    """
    config = params or {}
    axis_methods = {
        'x': 'get_xaxis',
        'y': 'get_yaxis',
    }
    formatter_methods = {
        'major': 'set_major_formatter',
        'minor': 'set_minor_formatter,'
    }
    instances = {}
    need_locator_instances = [
        matplotlib.dates.AutoDateFormatter,
    ]

    try:
        # ConciseDateFormatter is not supported on Python 3.5 and Matplotlib
        # below version 3.1.0. So import it only when it is available.
        from matplotlib.dates import ConciseDateFormatter
        need_locator_instances.append(matplotlib.dates.ConciseDateFormatter)
    except ImportError:
        pass

    locators = kwargs.get('locators', {})

    def get_locator_instance(locators, on, which):
        instance = locators.get(on, {}).get(which)
        if instance is None:
            raise ChartError("Could'nt find locator instance "
                             "required for formatter class")
        return instance

    for key, value in config.items():
        if key not in axis_methods:
            continue
        gca = getattr(axis, axis_methods[key])()

        for which, data in value.items():
            if which in formatter_methods:
                tick_format = data.get('format')
                if tick_format:
                    name = data.get('name', 'FormatStrFormatter')
                    formatter = getattr(matplotlib.ticker, name)
                    getattr(gca, formatter_methods[which])(
                        formatter(data.get('format')))
                else:
                    name = data.get('name')
                    if name is None:
                        raise ChartError(
                            'Parameter name is required '
                            'if using non-default formatter')

                    for attr in [matplotlib.ticker, matplotlib.dates]:
                        formatter = getattr(attr, name, None)
                        if formatter:
                            break

                    if formatter is None:
                        raise ChartError(
                            'Unsupported formatter class {}'.format(name))

                    if formatter in need_locator_instances:
                        locator = get_locator_instance(locators, key, which)
                        instance = formatter(
                            locator,
                            *data.get('params', []),
                            **data.get('keyword_params', {})
                        )
                    else:
                        instance = formatter(*data.get('params', []),
                                             **data.get('keyword_params', {}))

                    instances.update({key: {which: instance}})
                    getattr(gca, formatter_methods[which])(instance)

    return instances


def set_axis_legend(axis, params=None, **kwargs):
    """
    Set axis legend.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param params: Axis legend parameters.
    :type params: dict, optional
    """
    config = params or {}

    if config.pop('show', False):
        axis.legend(**config)


def set_axis_label(axis, params=None, **kwargs):
    """
    Set axis label.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param params: Axis label parameters.
    :type params: dict, optional

    Example config:

    .. code-block:: python

        'labels': {
            'x': {
                'text': 'x'
                'style': {

                }
            }
        }
    """
    config = params or {}

    methods = {
        'x': 'set_xlabel',
        'y': 'set_ylabel',
    }

    for key, value in config.items():
        if key not in methods:
            continue
        method = getattr(axis, methods[key])
        method(value.get('text', ''), **value.get('style', {}))


def build_secondary_axis(axis, on='x', **kwargs):
    """
    Build twin secondary axis.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param on: Name of axis to build secondary axis (x, y).
    :type on: str, default: x
    """
    methods = {
        'x': 'twinx',
        'y': 'twiny',
    }
    method = getattr(axis, methods[on])
    return method()


def build_tertiary_axis(axis, **kwargs):
    """
    Build twin tertiary axis.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    """
    on = kwargs.get('on', 'x')
    side = kwargs.get('side', 'right')
    position = kwargs.get('position', 'zero')

    gca = build_secondary_axis(axis, on=on)
    gca.spines[side].set_position(position)
    return gca


def customize_axis(axis, params, **kwargs):
    """
    Customize axis based-on given params.

    :param axis: Matplotlib axis instance.
    :type axis: :class:`matplotlib.axes.Axes`
    :param params: Axis modifier parameters.
    :type params: dict
    """
    config = params.copy()

    for name in config:
        if name in SUPPORTED_CUSTOMIZERS:
            modifier = config[name]
            if isinstance(modifier, dict):
                value = modifier.pop('value', None)
                if isinstance(value, list):
                    args = [value]
                else:
                    args = []

                kwargs = modifier
            elif isinstance(modifier, list):
                args = list(modifier)
                kwargs = {}
            else:
                args = [modifier]
                kwargs = {}

            method_name = getattr(axis, SUPPORTED_CUSTOMIZERS[name])
            customizer = partial(method_name, *args, **kwargs)
            customizer()


def fetch_resource(series, **kwargs):
    """
    Fetch series resource.

    Series resource is resolved in the following order, CSV, JSON URL, and BMA
    API name. If none of the sources found in the chart series configuration,
    it returns None.

    :param series: KomaPy series config instance.
    :type series: :class:`komapy.series.Series`
    :return: :class:`pandas.DataFrame` object if using CSV, JSON URL, or
             BMA API name. Otherwise, it returns None.
    """
    sources = OrderedDict([
        ('csv', {
            'resolver': processing.read_csv,
            'options': 'csv_params'
        }),
        ('url', {
            'resolver': client.fetch_url_as_dataframe,
            'options': 'query_params'
        }),
        ('name', {
            'resolver': client.fetch_bma_as_dataframe,
            'options': 'query_params'
        }),
    ])

    for name in sources:
        source = getattr(series, name, None)
        if source:
            resolve = sources[name]['resolver']
            options = getattr(series, sources[name]['options'], {})
            break

    if source:
        resource = resolve(source, **options)
    else:
        resource = None

    return resource


def resolve_data(series, **kwargs):
    """
    Resolve plot data.

    Plot data is resolved in the following order, CSV, JSON URL, and BMA API
    name. Each of sources has certain resolver. If none of the sources found
    in the chart series, data source is treated as plain object.

    :param series: KomaPy series config instance.
    :type series: :class:`komapy.series.Series`
    :return: A list of resolved plot data whose type of
             :class:`pandas.DataFrame` if using CSV, JSON URL, or BMA API name.
             Otherwise, it returns native object.
    :rtype: list of :class:`pandas.DataFrame` or native object
    """
    if kwargs.get('resource') is not None:
        resource = kwargs.get('resource')
    else:
        resource = fetch_resource(series, **kwargs)
    if resource is not None:
        func = partial(processing.dataframe_or_empty, resource)
        iterator = map(func, series.fields)
    else:
        iterator = series.fields

    plot_data = []
    for i, field in enumerate(iterator):
        if i == 0 and series.xaxis_date:
            plot_data.append(utils.resolve_timestamp(field))
        elif i == 1 and series.yaxis_date:
            plot_data.append(utils.resolve_timestamp(field))
        else:
            plot_data.append(field)

    if series.aggregations:
        for item in series.aggregations:
            func = item.get('func')
            if func is None:
                raise ChartError(
                    'Function name or callable must be set '
                    'if using data aggregations')

            agg_field = item.get('field')
            if agg_field is None:
                raise ChartError('Field name must be set '
                                 'if using data aggregations')
            if resource is not None:
                index = series.fields.index(agg_field)
            else:
                index = agg_field

            params = item.get('params', {})

            if isinstance(func, str):
                if func not in processing.supported_aggregations:
                    continue

                resolver = processing.supported_aggregations[func]
                if isinstance(resolver, str):
                    callback = getattr(processing, resolver)
                elif isinstance(resolver, Callable):
                    callback = resolver
                plot_data[index] = callback(plot_data[index], params)
            elif isinstance(func, Callable):
                callback = func
                plot_data[index] = callback(plot_data[index], params)

    if series.transforms:
        for name in series.transforms:
            if isinstance(name, str):
                if name not in transforms.transform_registers:
                    continue

                resolver = transforms.transform_registers[name]
                if isinstance(resolver, str):
                    callback = getattr(transforms, resolver)
                elif isinstance(resolver, Callable):
                    callback = resolver
                plot_data = callback(plot_data, series)
            elif isinstance(name, Callable):
                callback = name
                plot_data = callback(plot_data, series)

    return plot_data
