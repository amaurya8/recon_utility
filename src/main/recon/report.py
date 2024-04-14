import pandas as pd

class MakeMyReport:
    def __init__(self, comparison,df1,df2,init_configs):
        self.comparison = comparison
        self.df1 = df1
        self.df2 = df2
        self.init_configs = init_configs

    def recon_report(self):
        df_col_stats = self.comparison.column_stats
        src_row_count = self.df1.shape[0]
        src_col_count = len(self.df1.columns)
        tgt_row_count = self.df2.shape[0]
        tgt_col_count = len(self.df2.columns)

        common_rows_count = self.comparison.intersect_rows.shape[0]
        rows_in_src_only = self.comparison.df1_unq_rows.shape[0]
        rows_in_tgt_only = self.comparison.df2_unq_rows.shape[0]
        rows_having_mismatch = self.comparison.all_mismatch().shape[0]
        row_having_no_mismatch = common_rows_count - rows_having_mismatch

        common_cols_count = len(self.comparison.intersect_columns())
        cols_in_src_only_count = len(self.comparison.df1_unq_columns())
        cols_in_tgt_only = len(self.comparison.df2_unq_columns())
        col_stats = self.comparison.column_stats
        cols_having_no_mismatch = 0
        cols_having_mismatch = 0
        for element in col_stats:
            if (element['all_match']):
                cols_having_no_mismatch = cols_having_no_mismatch + 1
            else:
                cols_having_mismatch = cols_having_mismatch + 1

        summary_chart_data = [src_row_count, src_col_count, tgt_row_count, tgt_col_count]
        row_summary_data = [common_rows_count, rows_in_src_only, rows_in_tgt_only, row_having_no_mismatch,
                            rows_having_mismatch]
        col_summary_data = [common_cols_count, cols_in_src_only_count, cols_in_tgt_only, cols_having_no_mismatch,
                            cols_having_mismatch]

        matched_keys = self.comparison.join_columns.__str__()
        absolute_tole = str(self.comparison.abs_tol)
        relative_tole = str(self.comparison.rel_tol)

        dupe_row_in_src = pd.merge(self.comparison.df1_unq_rows, self.comparison.intersect_rows, on='store_id', how='inner')
        dupe_row_in_tgt = pd.merge(self.comparison.df2_unq_rows, self.comparison.intersect_rows, on='store_id', how='inner')
        dupe_row_in_src_count = dupe_row_in_src.shape[0]
        dupe_row_in_tgt = dupe_row_in_tgt.shape[0]
        spaces_ignored = self.comparison.ignore_spaces

        df_col_with_uneq_values_types = pd.DataFrame.from_dict(self.comparison.column_stats)
        all_mismatch = self.comparison.all_mismatch()

        # Apply the custom function to the DataFrame
        styled_df = all_mismatch.style.apply(self.highlight_diff, axis=1)

        styled_df.hide(axis=0)

        # Display the styled DataFrame
        styled_html = styled_df._repr_html_()
        # print(styled_html)

        ########################### generating report ##########################
        recon_report = '../reports/recon_report' + "_" + self.init_configs.src_system + "_" + self.init_configs.tgt_system + ".html"
        with open('../reports/recon_report_tmpl.html', 'r') as input_report_file, open(recon_report,
                                                                               'w') as output_report_file:
            html_report = input_report_file.read()
            html_report = html_report.replace("#absolute_tole#", absolute_tole)
            html_report = html_report.replace("#relative_tole#", relative_tole)
            html_report = html_report.replace("#matched_keys#", matched_keys)
            html_report = html_report.replace("#Columns with un-eq values / types#",
                                              df_col_with_uneq_values_types.to_html().__str__())
            html_report = html_report.replace("#Rows with un-eq values#", styled_html)
            html_report = html_report.replace("#Rows Only In Src#", self.comparison.df1_unq_rows.to_html().__str__())
            html_report = html_report.replace("#Rows Only In Tgt#", self.comparison.df2_unq_rows.to_html().__str__())
            html_report = html_report.replace("#Summary Chart#", summary_chart_data.__str__())
            html_report = html_report.replace("#Row Summary#", row_summary_data.__str__())
            html_report = html_report.replace("#Column Summary#", col_summary_data.__str__())

            output_report_file.write(html_report)


    def highlight_diff(self,x):
        styles = [''] * len(x)
        for i in range(1, len(x), 2):  # Starting from index 1 and comparing alternate adjacent columns
            if x.iloc[i] != x.iloc[i + 1]:
                styles[i] = 'background-color: #FF6347'
                styles[i + 1] = 'background-color: #FF6347'
        return styles

