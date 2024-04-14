import pandas as pd
import os
import datacompy
import report
import recon_init

print('## Starting Recon Engine...! ##')
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
file_path = '../../resources/Driver_Config.csv'
src_input_base_path = '../../resources/src_input_files/'
tgt_input_base_path = '../../resources/tgt_input_files/'


# Loading Driver Config file
config_df = pd.read_csv(file_path)
init_configs = recon_init.InitConfigs(config_df)

# Read the CSV file into a DataFrame
input_src_df = pd.read_csv(src_input_base_path + "/" + config_df['Src_Detail'].values[0])
input_tgt_df = pd.read_csv(tgt_input_base_path + '/' + config_df['Tgt_Detail'].values[0])

comparison = datacompy.Compare(input_src_df, input_tgt_df, join_columns =  ['Store_ID'])
report_obj = report.MakeMyReport(comparison, input_src_df, input_tgt_df, init_configs)
report_obj.recon_report()
print('## Recon Completed ...! ##')