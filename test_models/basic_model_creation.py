# create basic random forest model
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from preprocessing import Preprocessing
from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score
import traceback
import pickle
import os

class BasicModelCreation(Preprocessing):

    pre_processed_CSV_FILE = 'post_preprocessing_concise_tshark_1_2_125000.csv'
    RSEED = 50

    def __init__(self):
        try:
            csv_file = ''
            # csv_file = input('[PRESS ENTER TO CHOOSE DEFAULT] - enter name if u have different post_preprocessing_concise csv file - ')
            if len(csv_file) < 1:
                try:
                    self.pre_processed_df = pd.read_csv(self.pre_processed_CSV_FILE)
                    start_from_scratch = input(self.pre_processed_CSV_FILE + ' already exists. Press ENTER to continue, else ENTER any key to start from scratch.')
                    if len(start_from_scratch) < 1:
                        pass
                    else:
                        invoke_except_block = 1/0
                        invoke_except_block += 1
                    print('[INFO] ' + self.pre_processed_CSV_FILE + ' already exists, using that.')
                except:
                    super(BasicModelCreation, self).__init__()
                    concise_df = self.df.drop(['frame.number', '_ws.col.Info'], axis=1)
                    self.pre_processed_df = concise_df
            else:
                try:
                    self.pre_processed_df = pd.read_csv(csv_file)
                    print('[INFO] using ' + csv_file)
                except:
                    print('[FAIL] using ' + csv_file)
            
            # removing unnamed column
            self.pre_processed_df = self.pre_processed_df.iloc[:, 1:]

            print('[DONE] basic_model_creation initialisation')
        except Exception as e:
            print('[FAIL] basic_model_creation initialisation - ', e)

        try:
            self.train_test_split()
            self.create_model()
            self.tree_stats()
            self.training_predictions()
            self.testing_predictions()
            self.evaluate_model(self.test_rf_predictions, self.test_rf_probs, self.train_rf_predictions, self.train_rf_probs)
            self.feature_importance()
            print('[DONE] basic_model_creation further processes.')
        except:
            print('[FAIL] basic_model_creation further processes.')

    def train_test_split(self):
        try:
            # Extract the labels
            self.labels = np.array(self.pre_processed_df.pop('normality'))

            # 30% examples in test data
            self.train, self.test, self.train_labels, self.test_labels = train_test_split(self.pre_processed_df,
                                                    self.labels, 
                                                    stratify = self.labels,
                                                    test_size = 0.3, 
                                                    random_state = self.RSEED)

            # Imputation of missing values
            self.train = self.train.fillna(self.train.mean())
            self.test = self.test.fillna(self.test.mean())

            # Features for feature importances
            self.features = list(self.train.columns)

            # print('self.features')
            # print(self.features)
            # print('self.train.describe()')
            # print(self.train.describe())
            # print('self.train.head()')
            # print(self.train.head())
            # print('self.test.describe()')
            # print(self.test.describe())
            # print('self.test.head()')
            # print(self.test.head())
            # print('self.labels[:10]')
            # print(self.labels[:10])

            print('[DONE] train test split')
        except:
            print('[FAIL] train test split')

    def create_model(self):
        try:
            # Create the model with 100 trees
            self.model = RandomForestClassifier(n_estimators=100, 
                                        random_state=self.RSEED, 
                                        max_features = 'sqrt',
                                        n_jobs=-1, verbose = 1)

            # Fit on training data
            self.model.fit(self.train, self.train_labels)

            print('[DONE] create model')
        except Exception as e:
            print('[FAIL] create model - ', e)

    def tree_stats(self):
        try:
            n_nodes = []
            max_depths = []

            # Stats about the trees in random forest
            for ind_tree in self.model.estimators_:
                n_nodes.append(ind_tree.tree_.node_count)
                max_depths.append(ind_tree.tree_.max_depth)
            
            print(f'Average number of nodes {int(np.mean(n_nodes))}')
            print(f'Average maximum depth {int(np.mean(max_depths))}')
            
            print('[DONE] tree stats')
        except:
            print('[FAIL] tree stats')
    
    def training_predictions(self):
        try:
            # Training predictions (to demonstrate overfitting)
            self.train_rf_predictions = self.model.predict(self.train)
            self.train_rf_probs = self.model.predict_proba(self.train)[:, 1]
            print('Accuracy on training data - ' + str(accuracy_score(self.train_labels, self.train_rf_predictions)))

            print('[DONE] training predictions')
        except:
            print('[FAIL] training predictions')

    
    def testing_predictions(self):
        try:
            # Testing predictions (to determine performance)
            self.test_rf_predictions = self.model.predict(self.test)
            self.test_rf_probs = self.model.predict_proba(self.test)[:, 1]
            print('Accuracy on testing data - ' + str(accuracy_score(self.test_labels, self.test_rf_predictions)))

            print('[DONE] testing predictions')
        except:
            print('[FAIL] testing predictions')
                

    def evaluate_model(self, predictions, probs, train_predictions, train_probs):
        try:
            # Print the confusion matrix
            print('---------------------------------------------------------------')
            print('confusion matrix - for test data')
            print('---------------------------------------------------------------')
            print(confusion_matrix(self.test_labels, self.test_rf_predictions))

            print('---------------------------------------------------------------')
            print('confusion matrix - for train data')
            print('---------------------------------------------------------------')
            print(confusion_matrix(self.train_labels, self.train_rf_predictions))

            # Print the precision and recall, among other metrics
            print('---------------------------------------------------------------')
            print('classification report - for test data')
            print('---------------------------------------------------------------')
            print(classification_report(self.test_labels, self.test_rf_predictions, digits=3))

            print('---------------------------------------------------------------')
            print('classification report - for train data')
            print('---------------------------------------------------------------')
            print(classification_report(self.train_labels, self.train_rf_predictions, digits=3))

            print('[DONE] model evaluation')
        except Exception as e:
            print('[FAIL] model evaluation - ', e)
            print(traceback.format_exc())
    
    def feature_importance(self):
        try:
            # Extract feature importances
            fi = pd.DataFrame({'feature': list(self.train.columns),
                            'importance': self.model.feature_importances_}).\
                                sort_values('importance', ascending = False)

            # Display
            print(fi.head(12))

            print('[DONE] feature importance')
        except:
            print('[FAIL] feature importance')
    
    def create_model_pickle(self):
        try:
            filename = 'model'
            
            # create unique model name that doesn't exist in current directory
            if os.path.isfile(filename):
                version = 1
                filename = 'model_1'
                while os.path.isfile(filename):
                    version += 1
                    filename = filename.split('_')[0] + str(version)

            outfile = open(filename,'wb')
            pickle.dump(self.model, outfile)
            outfile.close()
        
            print('[DONE] pickle of model created - ' + filename)
        except:
            print('[FAIL] pickle of model created - ' + filename)


if __name__ == '__main__':
    oBasicModelCreation = BasicModelCreation()
    oBasicModelCreation.create_csv_post_preprocessing_concise()
    oBasicModelCreation.create_model_pickle()
    # oBasicModelCreation.create_csv_post_preprocessing_with_info()