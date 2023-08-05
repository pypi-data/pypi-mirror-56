from sklearn.base import BaseEstimator, TransformerMixin

from brainless import utils

booleans = {True, False, 'true', 'false', 'True', 'False', 'TRUE', 'FALSE'}


# Used in CustomSparseScaler
def calculate_scaling_ranges(X, col, min_percentile=0.05, max_percentile=0.95):
    series_values = X[col]
    good_values_indexes = series_values.notnull()

    series_values = list(series_values[good_values_indexes])
    series_values = sorted(series_values)

    index_of_max_value = int(max_percentile * len(series_values)) - 1
    index_of_min_value = int(min_percentile * len(series_values))

    if len(series_values) > 0:
        max_value = series_values[index_of_max_value]
        min_value = series_values[index_of_min_value]
    else:
        return 'ignore'

    if max_value in booleans or min_value in booleans:
        return 'pass_on_col'

    inner_range = max_value - min_value

    if inner_range == 0:
        # Used to do recursion here, which is prettier and uses less code, but since we've
        # already got the filtered and sorted series_vals, it makes sense to use those to avoid
        # duplicate computation. Grab the absolute largest max and min vals, and see if there is
        # any difference in them, since our 95th and 5th percentile vals had no difference
        # between them.
        max_value = series_values[len(series_values) - 1]
        min_value = series_values[0]
        inner_range = max_value - min_value

        if inner_range == 0:
            # If this is a binary field, keep all the values in it, just make sure they're scaled
            # to 1 or 0.
            if max_value == 1:
                min_value = 0
                inner_range = 1
            else:
                # If this is just a column that holds all the same values for everything though,
                # delete the column to save some space
                return 'ignore'

    col_summary = {'max_val': max_value, 'min_val': min_value, 'inner_range': inner_range}

    return col_summary


# Scale sparse data to the 95th and 5th percentile. Only do so for values that
# actually exist (do absolutely nothing with rows that do not have this data point)
class CustomSparseScaler(BaseEstimator, TransformerMixin):

    def __init__(self,
                 column_descriptions,
                 truncate_large_values=False,
                 perform_feature_scaling=True,
                 min_percentile=0.05,
                 max_percentile=0.95):
        self.column_descriptions = column_descriptions

        self.numeric_col_descs = {None, 'continuous', 'numerical', 'numeric', 'float', 'int'}
        # Everything in column_descriptions (except numeric_col_descs) is a non-numeric column,
        # and thus, cannot be scaled
        self.cols_to_avoid = set(
            [k for k, v in column_descriptions.items() if v not in self.numeric_col_descs])

        # Setting these here so that they can be grid searchable.

        # Truncating large values is an interesting strategy. It forces all values to fit inside
        # the 5th - 95th percentiles. Essentially, it turns any really large (or small) values
        # into reasonably large (or small) values.
        self.truncate_large_values = truncate_large_values
        self.perform_feature_scaling = perform_feature_scaling
        self.min_percentile = min_percentile
        self.max_percentile = max_percentile

    def get(self, prop_name, default=None):
        try:
            return getattr(self, prop_name)
        except AttributeError:
            return default

    def fit(self, X, y=None):
        print('Performing feature scaling')
        self.column_ranges = {}
        self.cols_to_ignore = []

        if self.perform_feature_scaling:

            for col in X.columns:
                if col not in self.cols_to_avoid:
                    col_summary = calculate_scaling_ranges(
                        X,
                        col,
                        min_percentile=self.min_percentile,
                        max_percentile=self.max_percentile)
                    if col_summary == 'ignore':
                        self.cols_to_ignore.append(col)
                    elif col_summary == 'pass_on_col':
                        pass
                    else:
                        self.column_ranges[col] = col_summary

        return self

    # Perform basic min/max scaling, with the minor caveat that our min and max values are the
    # 10th and 90th percentile values, to avoid outliers.
    def transform(self, X, y=None):

        if isinstance(X, dict):
            for col, col_dict in self.column_ranges.items():
                if col in X:
                    X[col] = scale_val(
                        val=X[col],
                        min_val=col_dict['min_val'],
                        total_range=col_dict['inner_range'],
                        truncate_large_values=self.truncate_large_values)
        else:

            if len(self.cols_to_ignore) > 0:
                X = utils.safely_drop_columns(X, self.cols_to_ignore)

            for col, col_dict in self.column_ranges.items():
                if col in X.columns:
                    min_val = col_dict['min_val']
                    inner_range = col_dict['inner_range']
                    X[col] = X[col].apply(
                        lambda x: scale_val(x, min_val, inner_range, self.truncate_large_values))

        return X


def scale_val(val, min_val, total_range, truncate_large_values=False):
    scaled_value = (val - min_val) / total_range
    if truncate_large_values:
        if scaled_value < 0:
            scaled_value = 0
        elif scaled_value > 1:
            scaled_value = 1

    return scaled_value
