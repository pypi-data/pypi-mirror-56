# Modified version of scikit-learn's DictVectorizer
import numbers
from array import array

import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.base import BaseEstimator, TransformerMixin

from brainless.utils import CustomLabelEncoder

bad_values = {
    float('nan'),
    float('inf'),
    float('-inf'), None, np.nan, 'None', 'none', 'NaN', 'NAN', 'nan', 'NULL', 'null', '', 'inf',
    '-inf'
}

class DataFrameVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self,
                 column_descriptions=None,
                 datatype=np.float32,
                 separator="=",
                 sparse=True,
                 keep_cat_features=False):
        self.datatype = datatype
        self.separator = separator
        self.sparse = sparse
        if column_descriptions is None:
            column_descriptions = {}
        self.column_descriptions = column_descriptions
        self.values_to_drop = {'ignore', 'output', 'regressor', 'classifier'}
        self.has_been_restricted = False
        self.keep_cat_features = keep_cat_features
        self.label_encoders = {}
        self.numerical_columns = None
        self.num_numerical_cols = None
        self.categorical_columns = None
        self.numeric_col_types = [
            'int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64'
        ]
        self.additional_numerical_cols = []

    def get(self, prop_name, default=None):
        try:
            return getattr(self, prop_name)
        except AttributeError:
            return default

    # TODO: Simplify
    def fit(self, X, y=None):
        print('Fitting DataFrameVectorizer')

        feature_names = []
        vocab = {}

        # Rearrange X so that all the categorical columns are first
        numerical_columns = []
        categorical_columns = []
        for col in X.columns:
            col_desc = self.column_descriptions.get(col, False)
            if col_desc in [False, 'continuous', 'int', 'float', 'numerical']:
                numerical_columns.append(col)
            elif col_desc in self.values_to_drop:
                continue
            elif col_desc == 'categorical':
                categorical_columns.append(col)
            else:
                print('We are unsure what to do with this column:')
                print(col)
                print(col_desc)

        self.num_numerical_cols = len(numerical_columns)
        self.numerical_columns = numerical_columns
        self.categorical_columns = categorical_columns

        new_cols = numerical_columns + categorical_columns
        X = X[new_cols]

        for col_name in X.columns:

            if self.column_descriptions.get(col_name,
                                            False) == 'categorical' and self.keep_cat_features:
                # All of these values will go in the same column, but they must be turned into
                # ints first
                self.label_encoders[col_name] = CustomLabelEncoder()
                # Then, we will use the same flow below to make sure they appear in the vocab
                # correctly
                self.label_encoders[col_name].fit(X[col_name])

            # We can't do elif here- it has to be inclusive of the logic above
            if self.column_descriptions.get(col_name,
                                            False) == 'categorical' and not self.keep_cat_features:
                # If this is a categorical column, iterate through each row to get all the
                # possible values that we are one-hot-encoding.
                for val in set(X[col_name]):
                    if not isinstance(val, str):
                        if isinstance(val, numbers.Number) or val is None:
                            val = str(val)
                        else:
                            val = val.encode('utf-8').decode('utf-8')

                    feature_name = col_name + self.separator + val

                    if feature_name not in vocab:
                        feature_names.append(feature_name)
                        vocab[feature_name] = len(vocab)

            # If this is a categorical column, do not include the column name itself,
            # just include the feature_names as calculated above
            elif col_name not in vocab:
                feature_names.append(col_name)
                vocab[col_name] = len(vocab)

        self.feature_names_ = feature_names
        self.vocabulary_ = vocab
        return self

    # TODO: Simplify
    def _transform(self, X):

        datatype = self.datatype
        vocab = self.vocabulary_

        if isinstance(X, dict):

            indices = array("i")
            indptr = array("i", [0])
            values = []

            for feature, value in X.items():
                if self.column_descriptions.get(feature, False) == 'categorical':
                    if not self.get('keep_cat_features', False):
                        if not isinstance(value, str):
                            if isinstance(value, numbers.Number) or value is None:
                                value = str(value)
                            else:
                                value = value.encode('utf-8').decode('utf-8')
                        feature = feature + self.separator + value
                        value = 1
                    else:
                        if value in bad_values:
                            value = '_None'
                        value = self.get('label_encoders')[feature].transform([value])

                if feature in vocab and value not in bad_values and (self.get(
                        'keep_cat_features', False) or not np.isnan(value)):
                    indices.append(vocab[feature])
                    # Convert the value to the correct datatype, then append to our values list
                    values.append(datatype(value))

            indptr.append(len(indices))

            if len(indptr) == 1:
                raise ValueError('The dictionary passed into DataFrameVectorizer is empty')

            indices = np.frombuffer(indices, dtype=np.intc)
            indptr = np.frombuffer(indptr, dtype=np.intc)
            shape = (len(indptr) - 1, len(vocab))

            result_matrix = sp.csr_matrix((values, indices, indptr), shape=shape, dtype=datatype)

            if self.sparse:
                result_matrix.sort_indices()

            return result_matrix

        else:

            for col in self.numerical_columns:
                if col not in X.columns:
                    X[col] = 0
            for col in self.categorical_columns:
                if col not in X.columns:
                    X[col] = 0
            for col in self.additional_numerical_cols:
                if col not in X.columns:
                    X[col] = 0

            X.fillna(0, inplace=True)

            for idx, col in enumerate(self.numerical_columns):
                if X[col].dtype not in self.numeric_col_types:
                    X[col] = X[col].astype(np.float32)

            # Running this in parallel can cause memory crashes if the dataset is too large.
            # TODO: With as complex as this lambda is, consider refactoring into an actual function
            categorical_values = list(map(
                lambda col_name: self.transform_categorical_col(col_values=list(X[col_name]),
                                                                col_name=col_name),
                self.categorical_columns))

            X = X[self.numerical_columns]
            # X.drop(self.categorical_columns, inplace=True, axis=1)
            X.reset_index(drop=True, inplace=True)
            for result in categorical_values:
                result.reset_index(drop=True, inplace=True)
                X[result.columns] = result
                del result

        if self.keep_cat_features:
            return X
        else:
            X = sp.csr_matrix(X.values)
            return X

    # We are assuming that each categorical column got a contiguous block of result columns (ie,
    # the 5 categories in City get columns 5-9, not columns 0, 8, 26, 4, and 20)
    # TODO: Simplify
    def transform_categorical_col(self, col_values, col_name):
        if self.get('keep_cat_features', False):
            return_values = self.get('label_encoders')[col_name].transform(col_values)
            result = {col_name: return_values}

            result = pd.DataFrame(result)
            # result[col_name] = pd.to_numeric(result[col_name], downcast='integer')

            return result

        else:

            num_trained_cols = 0
            min_transformed_idx = None
            max_transformed_idx = None
            len_col_name = len(col_name)
            encoded_col_names = []

            for trained_feature, col_idx in self.vocabulary_.items():
                if trained_feature[:len_col_name] == col_name:
                    encoded_col_names.append([trained_feature, col_idx])
                    num_trained_cols += 1
                    if min_transformed_idx is None:
                        min_transformed_idx = col_idx
                        max_transformed_idx = col_idx
                    elif col_idx > max_transformed_idx:
                        max_transformed_idx = col_idx
                    elif col_idx < min_transformed_idx:
                        min_transformed_idx = col_idx

            encoded_col_names = sorted(encoded_col_names, key=lambda tup: tup[1])
            encoded_col_names = [tup[0] for tup in encoded_col_names]

            result = sp.lil_matrix((len(col_values), num_trained_cols))

            if num_trained_cols == 0:
                df_result = pd.DataFrame(result.toarray(), columns=encoded_col_names)
                return df_result

            if num_trained_cols != (max_transformed_idx - min_transformed_idx + 1):
                raise ValueError('We have somehow ended up with categorical column '
                                 'behavior we were not expecting ')

            for row_idx, val in enumerate(col_values):
                if not isinstance(val, str):
                    if isinstance(val, numbers.Number) or val is None:
                        val = str(val)
                    else:
                        val = val.encode('utf-8').decode('utf-8')

                feature_name = col_name + self.separator + val
                if feature_name in self.vocabulary_:
                    col_idx = self.vocabulary_[feature_name]
                    col_idx = col_idx - min_transformed_idx

                    result[row_idx, col_idx] = 1

            df_result = pd.DataFrame(result.toarray(), columns=encoded_col_names)
            return df_result

    def transform(self, X):
        return self._transform(X)

    def get_feature_names(self):
        """Returns a list of feature names, ordered by their indices.
        If one-of-K coding is applied to categorical features, this will
        include the constructed feature names but not the original ones.
        """
        return self.feature_names_

    # This is for cases where we want to add in new features, such as for feature_learning
    def add_new_numerical_cols(self, new_feature_names):
        # add to our vocabulary
        for feature_name in new_feature_names:
            if feature_name not in self.vocabulary_:
                self.feature_names_.append(feature_name)
                self.vocabulary_[feature_name] = len(self.vocabulary_)
                self.additional_numerical_cols.append(feature_name)

        return self

    def restrict(self, support):
        """Restrict the features to those in support using feature selection.
        This function modifies the estimator in-place.
        """
        if self.has_been_restricted:
            return self

        new_numerical_cols = []
        new_categorical_cols = []
        new_additional_numerical_cols = []
        new_feature_names = []
        new_vocab = {}

        for idx, val in enumerate(support):
            if val:
                feature_name = self.feature_names_[idx]
                if self.separator in feature_name:
                    base_feature_name = feature_name[:feature_name.rfind(self.separator)]
                else:
                    base_feature_name = feature_name
                new_feature_names.append(feature_name)
                new_vocab[feature_name] = len(new_vocab)
                if feature_name in self.numerical_columns:
                    new_numerical_cols.append(feature_name)
                elif base_feature_name in self.categorical_columns \
                        and base_feature_name not in new_categorical_cols:
                    new_categorical_cols.append(base_feature_name)
                elif feature_name in self.additional_numerical_cols:
                    new_additional_numerical_cols.append(feature_name)

        self.feature_names_ = new_feature_names
        self.vocabulary_ = new_vocab
        self.numerical_columns = new_numerical_cols
        self.categorical_columns = new_categorical_cols
        self.additional_numerical_cols = new_additional_numerical_cols

        self.has_been_restricted = True
        return self
