import os
import sys
import pandas as pd
sys.path.append('.')
from common.loss_functions import pinball_loss


def read_test_files(benchmark_dir):
    
    test_data_dir = os.path.join(benchmark_dir, "data", "test")
    for rnd in range(1, 7):
        test_file = 'test_round_'+str(rnd)+'.csv'
        test_round = pd.read_csv(os.path.join(test_data_dir, test_file), parse_dates=['Datetime'])
        test_round['Round'] = rnd
        test_round = test_round[['Round', 'Datetime', 'Zone', 'DEMAND']]
        if rnd > 1:
            test = test.append(test_round)
        else:
            test = test_round.copy()
    return test



def evaluate(submission_file):
    
    benchmark_dir = os.path.join("energy_load", "GEFCom2017-D_Prob_MT_hourly")

    test = read_test_files(benchmark_dir)

    submission = pd.read_csv(os.path.join(submission_file), parse_dates=['Datetime'])

    evaluation = pd.merge(submission, test, on=['Round', 'Datetime', 'Zone'], how='left')

    evaluation['pinball'] = pinball_loss(evaluation['Prediction'], evaluation['DEMAND'], evaluation['q'])

    print("Mean pinball loss: ", evaluation['pinball'].mean())

    print(evaluation.groupby('Zone').apply(lambda x: x.mean())[['pinball']].rename(columns={'pinball':'mean pinball loss'}))
    

if __name__=="__main__":
    
    submission_file = sys.argv[1]
    evaluate(submission_file)