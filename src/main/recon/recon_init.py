
class InitConfigs:
    def __init__(self, config_df):
        self.src_system = config_df['Src_System'].values[0]
        self.tgt_system = config_df['Tgt_System'].values[0]
        self.src_type = config_df['Src_Type'].values[0]
        self.tgt_type = config_df['Tgt_Type'].values[0]
        self.src_detail = config_df['Src_Detail'].values[0]
        self.tgt_detail = config_df['Tgt_Detail'].values[0]
        self.compare_keys = config_df['Compare_Keys'].values[0]
        self.join_col_list = self.compare_keys.split(',')





