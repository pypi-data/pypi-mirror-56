import copy
import pandas as pd
import numpy as np
import logging

log = logging.getLogger(__name__)

FLOAT_TYPES = ["float16", "float32", "float64"]
INT_TYPES = ["int8", "int16", "int32", "int64"]


def df_merge(**kwargs):
    def _df_merge(left_df, right_df, *argsignore, **kwargsignore):
        kwargs.setdefault("suffixes", (False, False))
        return pd.merge(left_df, right_df, **kwargs)

    return _df_merge


def df_concat(new_col_name=None, new_col_values=None, col_id=None, sort=False):
    assert isinstance(new_col_name, (str, type(None)))
    assert isinstance(new_col_values, (list, type(None)))
    assert isinstance(col_id, (str, type(None)))
    kwargs = dict(
        new_col_name=new_col_name,
        new_col_values=new_col_values,
        col_id=col_id,
        sort=sort,
    )

    def _df_concat(*args):
        df_list = [arg for arg in args if isinstance(arg, pd.DataFrame)]
        assert len(df_list) >= 1, "No data frame was fed."

        new_col_name = kwargs.get("new_col_name")
        new_col_values = kwargs.get("new_col_values")
        col_id = kwargs.get("col_id")
        sort = kwargs.get("sort", False)

        if col_id is not None:
            for df in df_list:
                df.set_index(keys=col_id, inplace=True)
        else:
            col_id = df_list[0].index.name

        if (new_col_name is not None) and (new_col_values is None):
            new_col_values = list(range(len(df_list)))

        names = [new_col_name, col_id] if new_col_name else col_id
        df = pd.concat(
            df_list,
            sort=sort,
            verify_integrity=bool(col_id),
            keys=new_col_values,
            names=names,
        )
        if new_col_name:
            df.reset_index(inplace=True, level=new_col_name)
        return df

    return _df_concat


def df_sort_values(**kwargs):
    def _df_sort_values(df, *argsignore, **kwargsignore):
        """ https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html """
        kwargs.update(dict(inplace=True))
        df.sort_values(**kwargs)
        return df

    return _df_sort_values


def df_sample(**kwargs):
    def _df_sample(df, *argsignore, **kwargsignore):
        frac = kwargs.get("frac", 1.0)
        random_state = kwargs.get("random_state")
        col_sample = kwargs.get("col_sample")
        col_assign = kwargs.get("col_assign")

        log.info("DF shape before random sampling: {}".format(df.shape))
        if col_sample:
            population_arr = df[col_sample].unique()
            size = int(len(population_arr) * frac)
            np.random.seed(random_state)
            sample_arr = np.random.choice(population_arr, size=size, replace=False)
            if col_assign:
                assert isinstance(col_assign, str)
                sample_set = set(sample_arr.tolist())
                df[col_assign] = df[col_sample].map(
                    lambda v: np.int8(v in sample_set), na_action="ignore"
                )
            else:
                sample_series = pd.Series(sample_arr, name=col_sample)
                df = pd.merge(df, sample_series, how="right", on=col_sample)
        if not col_sample:
            if col_assign:
                raise NotImplementedError("Specify col_sample to use col_assign.")
            df = df.sample(frac=frac, random_state=random_state)
        log.info("DF shape after random sampling: {}".format(df.shape))
        return df

    return _df_sample


def df_get_cols(**kwargs):
    def _df_get_cols(df, *argsignore, **kwargsignore):
        return df.columns.to_list()

    return _df_get_cols


def df_select_dtypes(**kwargs):
    def _df_select_dtypes(df, *argsignore, **kwargsignore):
        return df.select_dtypes(**kwargs)

    return _df_select_dtypes


def df_select_dtypes_cols(**kwargs):
    def _df_select_dtypes_cols(df, *argsignore, **kwargsignore):
        return df_select_dtypes(**kwargs)(
            df, *argsignore, **kwargsignore
        ).columns.to_list()

    return _df_select_dtypes_cols


def df_get_col_indexes(**kwargs):
    def _df_get_col_indexes(df, *argsignore, **kwargsignore):
        cols = kwargs.get("cols")
        assert cols
        for col in cols:
            if col not in df.columns:
                log.warning("Could not find column: {}".format(col))
        cols = [col for col in cols if col in df.columns.to_list()]
        indices = [df.columns.to_list().index(col) for col in cols]
        return indices

    return _df_get_col_indexes


def df_drop(**kwargs):
    def _df_drop(df, *argsignore, **kwargsignore):
        kwargs.update(dict(inplace=True))
        df.drop(**kwargs)
        return df

    return _df_drop


def df_drop_filter(**kwargs):
    def _df_drop_filter(df, *argsignore, **kwargsignore):
        cols_drop = df_filter(**kwargs)(
            df, *argsignore, **kwargsignore
        ).columns.to_list()
        df.drop(columns=cols_drop, inplace=True)
        return df

    return _df_drop_filter


def df_add_row_stat(**kwargs):
    def _df_add_row_stat(df, *argsignore, **kwargsignore):
        regex = kwargs.get("regex", r".*")
        prefix = kwargs.get("prefix", "stat_all")

        prefix = prefix or regex
        t_df = df.filter(regex=regex, axis=1)
        cols_float = t_df.select_dtypes(include=FLOAT_TYPES).columns.to_list()
        cols_int = t_df.select_dtypes(include=INT_TYPES).columns.to_list()

        if cols_float:
            df["{}_float_na_".format(prefix)] = (
                df[cols_float].isna().astype("int8").sum(axis=1)
            )

            df["{}_float_zero_".format(prefix)] = (
                (df[cols_float] == 0.0).astype("int8").sum(axis=1)
            )
            df["{}_float_pos_".format(prefix)] = (
                (df[cols_float] > 0.0).astype("int8").sum(axis=1)
            )
            df["{}_float_neg_".format(prefix)] = (
                (df[cols_float] < 0.0).astype("int8").sum(axis=1)
            )
            df["{}_float_pos_ones_".format(prefix)] = (
                (df[cols_float] == 1.0).astype("int8").sum(axis=1)
            )
            df["{}_float_neg_ones_".format(prefix)] = (
                (df[cols_float] == -1.0).astype("int8").sum(axis=1)
            )
            df["{}_float_gt_pos_ones_".format(prefix)] = (
                (df[cols_float] > 1.0).astype("int8").sum(axis=1)
            )
            df["{}_float_lt_neg_ones_".format(prefix)] = (
                (df[cols_float] < -1.0).astype("int8").sum(axis=1)
            )
            df["{}_float_max_".format(prefix)] = df[cols_float].max(axis=1)
            df["{}_float_min_".format(prefix)] = df[cols_float].min(axis=1)
            df["{}_float_mean_".format(prefix)] = df[cols_float].mean(axis=1)

        if cols_int:
            df["{}_int_zero_".format(prefix)] = (
                (df[cols_int] == 0).astype("int8").sum(axis=1)
            )
            df["{}_int_pos_".format(prefix)] = (
                (df[cols_int] > 0).astype("int8").sum(axis=1)
            )
            df["{}_int_neg_".format(prefix)] = (
                (df[cols_int] < 0).astype("int8").sum(axis=1)
            )
            df["{}_int_pos_ones_".format(prefix)] = (
                (df[cols_int] == 1).astype("int8").sum(axis=1)
            )
            df["{}_int_neg_ones_".format(prefix)] = (
                (df[cols_int] == -1).astype("int8").sum(axis=1)
            )
            df["{}_int_gt_pos_ones_".format(prefix)] = (
                (df[cols_int] > 1).astype("int8").sum(axis=1)
            )
            df["{}_int_lt_neg_ones_".format(prefix)] = (
                (df[cols_int] < -1).astype("int8").sum(axis=1)
            )
            df["{}_int_max_".format(prefix)] = df[cols_int].max(axis=1)
            df["{}_int_min_".format(prefix)] = df[cols_int].min(axis=1)
            df["{}_int_mean_".format(prefix)] = df[cols_int].mean(axis=1)

        return df

    return _df_add_row_stat


def df_query(**kwargs):
    def _df_query(df, *argsignore, **kwargsignore):
        kwargs.update(dict(inplace=True))
        df.query(**kwargs)
        return df

    return _df_query


def df_eval(expr, parser="pandas", engine=None, truediv=True):
    def _df_eval(df, *argsignore, **kwargsignore):
        df = df.eval(expr=expr, parser=parser, engine=engine, truediv=truediv)
        return df

    return _df_eval


def df_drop_duplicates(**kwargs):
    def _df_drop_duplicates(df, *argsignore, **kwargsignore):
        kwargs.update(dict(inplace=True))
        df.drop_duplicates(**kwargs)
        return df

    return _df_drop_duplicates


def df_groupby(**kwargs):
    def _df_groupby(df, *argsignore, **kwargsignore):
        return df.groupby(**kwargs)

    return _df_groupby


def _groupby(df, groupby, columns):
    if isinstance(columns, dict):
        df = df.rename(columns=columns)
        columns = list(columns.values())
    if groupby is not None:
        if not isinstance(groupby, dict):
            groupby = dict(by=groupby)
        df = df.groupby(**groupby)
    if columns is not None:
        if isinstance(columns, (list, str)):
            df = df[columns]
        else:
            raise ValueError("'{}' must be dict, list, or str.".format(columns))
    return df


def _add_mutated(df, mutated_df, columns, keep_others):
    if keep_others:
        columns_list = list(columns.values()) if isinstance(columns, dict) else columns
        df[columns_list] = mutated_df
    else:
        df = mutated_df
    return df


def _preprocess_columns(columns):
    assert isinstance(columns, (dict, list, str, type(None)))
    columns_dict = None
    if isinstance(columns, dict):
        columns_dict = copy.deepcopy(columns)
        columns = list(columns_dict.values())
    return columns_dict, columns


def df_transform(groupby=None, columns=None, keep_others=False, **kwargs):
    columns_dict, columns = _preprocess_columns(columns)

    def _df_transform(df, *argsignore, **kwargsignore):
        df = df_duplicate(columns=columns_dict)(df)
        mutated_df = _groupby(df, groupby, columns).transform(**kwargs)
        df = _add_mutated(df, mutated_df, columns, keep_others)
        return df

    return _df_transform


def df_apply(groupby=None, columns=None, keep_others=False, **kwargs):
    columns_dict, columns = _preprocess_columns(columns)

    def _df_apply(df, *argsignore, **kwargsignore):
        df = df_duplicate(columns=columns_dict)(df)
        mutated_df = _groupby(df, groupby, columns).apply(**kwargs)
        return _add_mutated(df, mutated_df, columns, keep_others)

    return _df_apply


def df_applymap(groupby=None, columns=None, keep_others=False, **kwargs):
    columns_dict, columns = _preprocess_columns(columns)

    def _df_applymap(df, *argsignore, **kwargsignore):
        df = df_duplicate(columns=columns_dict)(df)
        mutated_df = _groupby(df, groupby, columns).applymap(**kwargs)
        return _add_mutated(df, mutated_df, columns, keep_others)

    return _df_applymap


def df_pipe(groupby=None, columns=None, keep_others=False, **kwargs):
    def _df_pipe(df, *argsignore, **kwargsignore):
        mutated_df = _groupby(df, groupby, columns).pipe(**kwargs)
        return _add_mutated(df, mutated_df, columns, keep_others)

    return _df_pipe


def df_agg(groupby=None, columns=None, **kwargs):
    def _df_agg(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.agg(**kwargs)

    return _df_agg


def df_aggregate(groupby=None, columns=None, **kwargs):
    def _df_aggregate(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.aggregate(**kwargs)

    return _df_aggregate


def df_rolling(groupby=None, columns=None, **kwargs):
    def _df_rolling(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.rolling(**kwargs)

    return _df_rolling


def df_expanding(groupby=None, columns=None, **kwargs):
    def _df_expanding(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.expanding(**kwargs)

    return _df_expanding


def df_ewm(groupby=None, columns=None, **kwargs):
    def _df_ewm(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.ewm(**kwargs)

    return _df_ewm


def df_filter(groupby=None, columns=None, **kwargs):
    def _df_filter(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        items = kwargs.get("items")
        if items:
            if isinstance(items, str):
                items = [items]
            assert isinstance(items, list), "'items' should be a list or string"
            missing = [item for item in items if item not in df.columns]
            if missing:
                log.warning("filter could not find columns: {}".format(missing))
            items = [item for item in items if item in df.columns]
            kwargs.update(dict(items=items))
        return df.filter(**kwargs)

    return _df_filter


def df_filter_cols(**kwargs):
    def _df_filter_cols(df, *argsignore, **kwargsignore):
        return df_filter(**kwargs)(df, *argsignore, **kwargsignore).columns.to_list()

    return _df_filter_cols


def df_fillna(groupby=None, columns=None, **kwargs):
    def _df_fillna(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.fillna(**kwargs)

    return _df_fillna


def df_head(groupby=None, columns=None, **kwargs):
    def _df_head(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.head(**kwargs)

    return _df_head


def df_tail(groupby=None, columns=None, **kwargs):
    def _df_tail(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.tail(**kwargs)

    return _df_tail


def df_shift(groupby=None, columns=None, **kwargs):
    def _df_shift(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.shift(**kwargs)

    return _df_shift


def df_resample(groupby=None, columns=None, **kwargs):
    def _df_resample(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.resample(**kwargs)

    return _df_resample


def df_ngroup(groupby=None, columns=None, **kwargs):
    def _df_ngroup(df, *argsignore, **kwargsignore):
        df = _groupby(df, groupby, columns)
        return df.ngroup(**kwargs)

    return _df_ngroup


def df_cond_replace(flag, columns, value=np.nan, replace_if_flag=True, **kwargs):
    columns_dict, columns = _preprocess_columns(columns)
    if not isinstance(flag, dict):
        flag = dict(expr=flag)

    def _df_cond_replace(df, *argsignore, **kwargsignore):
        df = df_duplicate(columns=columns_dict)(df)
        cond = df.eval(**flag)
        if not replace_if_flag:
            cond = np.invert(cond)
        df.loc[cond, columns] = value
        return df

    return _df_cond_replace


def df_rename(index=None, columns=None, copy=True, level=None):
    def _df_rename(df, *argsignore, **kwargsignore):
        if not (index is None and columns is None and level is None):
            df = df.rename(index=index, columns=columns, copy=copy, level=level)
        return df

    return _df_rename


def df_duplicate(columns):
    assert isinstance(columns, (dict, type(None)))
    columns_dict, columns = _preprocess_columns(columns)

    def _df_duplicate(df, *argsignore, **kwargsignore):
        if isinstance(columns_dict, dict):
            new_df = df_rename(columns=columns_dict)(df[columns_dict.keys()])
            df = pd.concat([df, new_df], axis=1, sort=False)
        return df

    return _df_duplicate


def df_map(arg, prefix="", suffix="", **kwargs):
    assert isinstance(arg, dict)

    def _df_map(df, *argsignore, **kwargsignore):
        for col, m in arg.items():
            if col in df.columns:
                new_col = prefix + col + suffix
                if isinstance(m, pd.Series):
                    m = m.to_dict()
                if isinstance(m, dict):
                    df.loc[:, new_col] = df[col].map(m, **kwargs)
                elif callable(m):
                    df.loc[:, new_col] = df[col].apply(m, **kwargs)
                elif m is not None:
                    df.loc[:, new_col] = m
            else:
                log.warning("'{}' not in the DataFrame".format(col))
        return df

    return _df_map


def sr_map(**kwargs):
    def _sr_map(sr, *argsignore, **kwargsignore):
        sr.map(**kwargs)

    return _sr_map


def df_get_dummies(**kwargs):
    def _df_get_dummies(df, *argsignore, **kwargsignore):
        return pd.get_dummies(df, **kwargs)

    return _df_get_dummies


def df_col_apply(func, **kwargs):
    def _df_col_apply(df, *argsignore, **kwargsignore):
        func_params = kwargs.pop("func_params", dict())
        cols = kwargs.pop("cols", None)
        cols = cols or df.columns
        df.loc[:, cols] = func(df.loc[:, cols], **func_params)
        return df

    return _df_col_apply


def df_dtypes_apply(func, **kwargs):
    def _df_dtypes_apply(df, *argsignore, **kwargsignore):
        func_params = kwargs.pop("func_params", dict())
        cols = df.select_dtypes(**kwargs).columns.to_list()
        df.loc[:, cols] = func(df.loc[:, cols], **func_params)
        return df

    return _df_dtypes_apply


def df_row_apply(func, **kwargs):
    def _df_row_apply(df, *argsignore, **kwargsignore):
        func_params = kwargs.pop("func_params", dict())
        rows = kwargs.pop("rows", None)
        rows = rows or df.index
        df.loc[rows, :] = func(df.loc[rows, :], **func_params)
        return df

    return _df_row_apply


def _cols_apply(df, func, cols, kwargs):
    assert callable(func)
    assert isinstance(kwargs, dict)
    if isinstance(cols, tuple):
        cols = list(cols)
    if not isinstance(cols, list):
        cols = [cols]
    for col in cols:
        assert isinstance(col, str), "'{}' is not str.".format(col)
        if col in df.columns:
            df.loc[:, col] = func(df.loc[:, col], **kwargs)
        else:
            log.warning("'{}' not in the data frame.".format(col))
    return df


def df_to_datetime(cols=None, **kwargs):
    def _df_to_datetime(df, *argsignore, **kwargsignore):
        if cols:
            df = _cols_apply(df, func=pd.to_datetime, cols=cols, kwargs=kwargs)
        else:
            df = pd.to_datetime(df, **kwargs)
        return df

    return _df_to_datetime


def df_total_seconds(cols=None, **kwargs):
    def _df_total_seconds(df, *argsignore, **kwargsignore):
        assert cols
        df = _cols_apply(df, func=pd.Series.dt.total_seconds, cols=cols, kwargs=kwargs)
        return df

    return _df_total_seconds


def df_to_timedelta(cols=None, **kwargs):
    def _df_to_timedelta(df, *argsignore, **kwargsignore):
        assert cols
        df = _cols_apply(df, func=pd.to_timedelta, cols=cols, kwargs=kwargs)
        return df

    return _df_to_timedelta


def df_strftime(cols=None, **kwargs):
    kwargs.setdefault("date_format", "%Y-%m-%dT%H:%M:%S")

    def _df_strftime(df, *argsignore, **kwargsignore):
        assert cols
        df = _cols_apply(df, func=pd.Series.dt.strftime, cols=cols, kwargs=kwargs)
        return df

    return _df_strftime


def df_slice(**kwargs):
    def _df_slice(df, *argsignore, **kwargsignore):
        start = kwargs.get("start", 0)
        end = kwargs.get("end", df.shape[0])
        step = kwargs.get("step", 1)
        return df.loc[start:end:step, :]

    return _df_slice


def df_focus_transform(
    focus, columns, groupby=None, keep_others=False, func="max", **kwargs
):
    assert isinstance(focus, (dict, str))
    assert isinstance(columns, (dict, list, str))
    columns_dict, columns = _preprocess_columns(columns)

    def _df_focus_transform(df):
        df = df_cond_replace(
            replace_if_flag=False, flag=focus, columns=columns_dict, value=np.nan
        )(df)
        df = df_transform(
            groupby=groupby,
            columns=columns,
            keep_others=keep_others,
            func=func,
            **kwargs
        )(df)
        return df

    return _df_focus_transform


def df_relative(focus, columns, groupby=None):
    assert isinstance(focus, (dict, str))
    assert isinstance(columns, dict)

    def _df_relative(df):
        df = df_focus_transform(focus=focus, columns=columns, groupby=groupby)(df)
        for col, new_col in columns.items():
            df[new_col] = df[col] - df[new_col]
        return df

    return _df_relative


def distance_matrix(coo_2darr, ord=None):
    coo_3darr = np.expand_dims(coo_2darr, axis=1)
    dist_2darr = np.linalg.norm(coo_3darr - coo_2darr, axis=2, ord=ord)
    return dist_2darr


def distance_to_affinity(
    dist_2darr,
    unit_distance=1.0,
    affinity_scale=1.0,
    binary_affinity=False,
    min_affinity=1.0e-6,
):
    if binary_affinity:
        affinity_2darr = dist_2darr <= unit_distance
    else:
        affinity_2darr = np.exp(-0.5 * np.square(dist_2darr / unit_distance))
    if affinity_scale is not None:
        affinity_2darr = affinity_2darr * affinity_scale
    if min_affinity is not None:
        affinity_2darr[affinity_2darr < min_affinity] = 0
    return affinity_2darr


def affinity_matrix(
    coo_2darr,
    ord=None,
    unit_distance=1.0,
    affinity_scale=1.0,
    binary_affinity=False,
    min_affinity=1.0e-6,
    zero_diag=True,
):
    dist_2darr = distance_matrix(coo_2darr, ord=ord)
    affinity_2darr = distance_to_affinity(
        dist_2darr,
        unit_distance=unit_distance,
        affinity_scale=affinity_scale,
        binary_affinity=binary_affinity,
        min_affinity=min_affinity,
    )
    if zero_diag:
        size = affinity_2darr.shape[1]
        affinity_2darr = affinity_2darr * (np.ones((size, size)) - np.eye(size))
    return affinity_2darr


def degree_matrix(affinity_2darr):
    return np.diagflat(affinity_2darr.sum(axis=1))


def laplacian_matrix(
    coo_2darr,
    ord=None,
    unit_distance=1.0,
    affinity_scale=1.0,
    binary_affinity=False,
    min_affinity=1.0e-6,
):
    affinity_2darr = affinity_matrix(
        coo_2darr=coo_2darr,
        ord=ord,
        unit_distance=unit_distance,
        affinity_scale=affinity_scale,
        binary_affinity=binary_affinity,
        min_affinity=min_affinity,
        zero_diag=True,
    )
    laplacian_2darr = degree_matrix(affinity_2darr) - affinity_2darr
    return laplacian_2darr


def row_vector_to_square_matrix(a):
    return np.tile(a, (a.shape[0], 1))


def eigen(
    a,
    return_values=True,
    values_as_square_matrix=False,
    return_vectors=False,
    sort=False,
):
    if return_vectors:
        w, v = np.linalg.eigh(a)

        if v.dtype == np.complex128:
            log.warning("Complex eigenvectors. The imaginary parts are discarded.")
            v = np.real(v)

        if sort:
            idx = np.argsort(w)
            v = v[:, idx]

        if return_values:
            w = w[idx]
            if values_as_square_matrix:
                w = row_vector_to_square_matrix(w)
            return w, v

        return v

    else:
        w = np.linalg.eigvalsh(a)

        if sort:
            idx = np.argsort(w)
            w = w[idx]

        if values_as_square_matrix:
            w = row_vector_to_square_matrix(w)

        return w


def laplacian_eigen(
    coo_2darr,
    return_values=True,
    return_vectors=False,
    ord=None,
    unit_distance=1.0,
    affinity_scale=1.0,
    binary_affinity=False,
    min_affinity=1.0e-6,
    sort=False,
):
    a = laplacian_matrix(
        coo_2darr,
        ord=ord,
        unit_distance=unit_distance,
        affinity_scale=affinity_scale,
        binary_affinity=binary_affinity,
        min_affinity=min_affinity,
    )
    ev = eigen(
        a,
        return_values=return_values,
        values_as_square_matrix=True,
        return_vectors=return_vectors,
        sort=sort,
    )
    return ev


def df_assign_columns(names=None, name_fmt="{:03d}"):
    if names is None:
        assert isinstance(name_fmt, str)
    _names = names
    _name_fmt = name_fmt

    def _df_assign_columns(df, values):
        names = _names or [_name_fmt.format(i) for i in range(values.shape[1])]
        values_df = pd.DataFrame(values, columns=names)
        out_df = pd.concat([df.reset_index(drop=True), values_df], axis=1, sort=False)
        return out_df.set_index(df.index)

    return _df_assign_columns


def df_spatial_features(
    output="distance",
    coo_cols=["X", "Y"],
    groupby=None,
    ord=None,
    unit_distance=1.0,
    affinity_scale=1.0,
    binary_affinity=False,
    min_affinity=1.0e-6,
    col_name_fmt="feat_{:03d}",
    keep_others=True,
    sort=True,
):
    """
    Available values for output:
     distance
     affinity
     laplacian
     eigenvalues
     eigenvectors
     n_connected
    """

    kwargs = dict(
        output=output,
        coo_cols=coo_cols,
        groupby=groupby,
        ord=ord,
        unit_distance=unit_distance,
        affinity_scale=affinity_scale,
        binary_affinity=binary_affinity,
        min_affinity=min_affinity,
        col_name_fmt=col_name_fmt,
        keep_others=keep_others,
        sort=sort,
    )

    def _df_spatial_features(df):
        output = kwargs.get("output")
        coo_cols = kwargs.get("coo_cols")
        groupby = kwargs.get("groupby")
        ord = kwargs.get("ord")
        unit_distance = kwargs.get("unit_distance")
        affinity_scale = kwargs.get("affinity_scale")
        binary_affinity = kwargs.get("binary_affinity")
        min_affinity = kwargs.get("min_affinity")
        col_name_fmt = kwargs.get("col_name_fmt")
        keep_others = kwargs.get("keep_others")
        sort = kwargs.get("sort")

        for coo_col in coo_cols:
            assert coo_col in df.columns

        if isinstance(affinity_scale, str):
            affinity_scale = dict(expr=affinity_scale)

        if groupby is not None:
            if not isinstance(groupby, dict):
                groupby = dict(by=groupby)
            g_df_iter = df.groupby(**groupby)
        else:
            g_df_iter = [("", df)]

        output_2darr_list = []
        for g_name, g_df in g_df_iter:
            if isinstance(affinity_scale, dict):
                affinity_scale_1darr = g_df.eval(**affinity_scale).values
                affinity_scale = np.expand_dims(
                    affinity_scale_1darr, axis=0
                ) * np.expand_dims(affinity_scale_1darr, axis=1)

            coo_2darr = g_df[coo_cols].values
            if output in ["distance"]:
                output_2darr = distance_matrix(coo_2darr, ord=ord)
            elif output in ["affinity"]:
                output_2darr = affinity_matrix(
                    coo_2darr=coo_2darr,
                    ord=ord,
                    unit_distance=unit_distance,
                    affinity_scale=affinity_scale,
                    binary_affinity=binary_affinity,
                    min_affinity=min_affinity,
                    zero_diag=True,
                )
            elif output in ["laplacian"]:
                output_2darr = laplacian_matrix(
                    coo_2darr,
                    ord=ord,
                    unit_distance=unit_distance,
                    affinity_scale=affinity_scale,
                    binary_affinity=binary_affinity,
                    min_affinity=min_affinity,
                )
            elif output in ["eigenvalues", "eigenvectors", "n_connected"]:
                if output in ["eigenvectors"]:
                    return_values = False
                    return_vectors = True
                else:
                    return_values = True
                    return_vectors = False

                output_2darr = laplacian_eigen(
                    coo_2darr,
                    return_values=return_values,
                    return_vectors=return_vectors,
                    ord=ord,
                    unit_distance=unit_distance,
                    affinity_scale=affinity_scale,
                    binary_affinity=binary_affinity,
                    min_affinity=min_affinity,
                    sort=sort,
                )
                if output in ["n_connected"]:
                    output_2darr = np.sum(
                        (output_2darr < 1.0e-8).astype(np.uint64), axis=1, keepdims=True
                    )
            else:
                raise NotImplementedError(output)
            output_2darr_list.append(output_2darr)

        output_2darr = np.concatenate(output_2darr_list, axis=0)

        if col_name_fmt is None:
            return output_2darr

        else:
            assert isinstance(col_name_fmt, str)
            if keep_others:
                return df_assign_columns(name_fmt=col_name_fmt)(df, output_2darr)
            else:
                output_col_names = [
                    col_name_fmt.format(i) for i in range(output_2darr.shape[1])
                ]
                return pd.DataFrame(
                    output_2darr, columns=output_col_names, index=df.index
                )

    return _df_spatial_features
