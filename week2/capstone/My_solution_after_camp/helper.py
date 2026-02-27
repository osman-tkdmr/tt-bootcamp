import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor


def analyze_data(dataframe, cat_th=10, car_th=20):
    """
    It gives the names of categorical, numerical and categorical but cardinal variables in the data set. It also performs incomplete data analysis.
    Parameters
    ------
        dataframe: dataframe
            The dataframe from which variable names are to be retrieved
        cat_th: int, optional
            Class threshold value for numeric but categorical variables
        car_th: int, optional
            Class threshold for categorical but cardinal variables

    Returns
    ------
        cat_cols: list
            Categorical variable list
        cat_cols: list
            Numerik değişken listesi
        cat_but_car: list
            Categorical view cardinal variable list
    """
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtype == "O"]
    num_cols = [col for col in dataframe.columns if dataframe[col].dtype != "O"]

    num_but_cat = [col for col in num_cols if dataframe[col].nunique() < cat_th]
    cat_but_car = [col for col in cat_cols if dataframe[col].nunique() > car_th]

    cat_cols = [col for col in cat_cols if col not in cat_but_car]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    cat_cols = cat_cols + num_but_cat
    
    print(f"Number of Observations: {dataframe.shape[0]}")
    print(f"Number of Variables: {dataframe.shape[1]}")
    print(f'Cat cols: {len(cat_cols)}, Num cols: {len(num_cols)}, Cat but car cols: {len(cat_but_car)}')

    return cat_cols, num_cols, cat_but_car

def knn_imputation(df, categorical_columns=None, numerical_columns=None, k=5):
    """
    Fills missing data using K-Nearest Neighbors (KNN) imputation. 
    For categorical columns, KNN Classifier is used. For numerical columns, KNN Regressor is used.

    Parameters:
    df (pd.DataFrame): Input dataframe with missing values.
    categorical_columns (list): List of categorical column names to impute. Default is None.
    numerical_columns (list): List of numerical column names to impute. Default is None.
    k (int): Number of neighbors to consider for KNN. Default is 5.

    Returns:
    pd.DataFrame: Dataframe with missing values filled.
    """
    df_filled = df.copy()
    categorical_columns = categorical_columns or []
    numerical_columns = numerical_columns or []

    def get_preprocessor(X):
        numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
        categorical_features = X.select_dtypes(include=['object', 'category']).columns

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])

        return ColumnTransformer(transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    for col in categorical_columns:
        if df_filled[col].isnull().sum() == 0:
            continue
        train_data = df_filled.dropna(subset=[col])
        test_data = df_filled[df_filled[col].isnull()]
        if test_data.empty:
            continue

        features = df_filled.columns.drop(col)
        X_train = train_data[features]
        y_train = train_data[col]
        X_test = test_data[features]

        preprocessor = get_preprocessor(X_train)
        knn_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', KNeighborsClassifier(n_neighbors=k))
        ])
        knn_pipeline.fit(X_train, y_train)
        df_filled.loc[df_filled[col].isnull(), col] = knn_pipeline.predict(X_test)

    for col in numerical_columns:
        if df_filled[col].isnull().sum() == 0:
            continue
        train_data = df_filled.dropna(subset=[col])
        test_data = df_filled[df_filled[col].isnull()]
        if test_data.empty:
            continue

        features = df_filled.columns.drop(col)
        X_train = train_data[features]
        y_train = train_data[col]
        X_test = test_data[features]

        preprocessor = get_preprocessor(X_train)
        knn_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', KNeighborsRegressor(n_neighbors=k))
        ])
        knn_pipeline.fit(X_train, y_train)
        df_filled.loc[df_filled[col].isnull(), col] = knn_pipeline.predict(X_test)

    return df_filled

def visual_miss(df):
    plt.figure(figsize=(18, 6))
    sns.set_style('whitegrid')

    ax = sns.heatmap(
        df.isna().T,
        cmap='YlOrRd',
        cbar_kws={'label': 'Missing Values'},
        xticklabels=False
    )

    plt.title('Missing Values in Dataset', fontsize=16, pad=20)
    plt.ylabel('Features', fontsize=12)  
    plt.xlabel('Observations', fontsize=12) 

    plt.tight_layout()

    plt.show()