from sklearn.naive_bayes import GaussianNB

def run_naive_bayes():
    
    train_data = pd.read_csv('restaurant_train(1).csv')
    valid_data = pd.read_csv('restaurant_valid(1).csv')

    
    cat_columns = train_data.columns.tolist()
    train_data[cat_columns] = train_data[cat_columns].astype("category")
    valid_data[cat_columns] = valid_data[cat_columns].astype("category")


    X_train = train_data[cat_columns[:-1]]
    y_train = train_data[cat_columns[-1]]

    
    X_valid = valid_data[cat_columns[:-1]]
    y_valid = valid_data[cat_columns[-1]]

    # Set up the imputer and ordinal encoder for categorical variables
    ordinal_encoder = make_column_transformer(
        (
            make_pipeline(SimpleImputer(strategy='most_frequent'),
                          OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)),
            make_column_selector(dtype_include="category"),
        ),
        remainder="passthrough",
        verbose_feature_names_out=False,
    )

    # Create a pipeline with the ordinal encoder and Gaussian Naive Bayes classifier
    nb_ordinal = make_pipeline(
        ordinal_encoder,
        GaussianNB()
    )

    
    nb_ordinal.fit(X_train, y_train)


    print("Naive Bayes - Training Data Classification Report:")
    print(classification_report(y_train, nb_ordinal.predict(X_train)))

    
    print("Naive Bayes - Validation Data Classification Report:")
    print(classification_report(y_valid, nb_ordinal.predict(X_valid)))


if __name__ == "__main__":
    run_naive_bayes()
