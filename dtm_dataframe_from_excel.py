#dtm_dataframe_from_excel.py
import pandas as pd
import numpy as np

class DTM:
    def __init__(self, excel_file):
        self.dtm = pd.read_excel(excel_file, sheet_name='Plano', index_col='id')
        self.total_amount_of_work = self.dtm['Duração Planejada (h)'].sum()
        self.critical_path_amount_of_work = self.dtm['End Time (h)'].max()
        self.parallel_work = self.total_amount_of_work - self.critical_path_amount_of_work
        self.calculate_planned_progress()
        self.calculate_daily_progress(excel_file)
 
    def calculate_planned_progress(self):
        # Converter "End Time (h)" para dias e arredondar para cima para obter o número total de dias do projeto
        total_days = int(np.ceil(self.critical_path_amount_of_work/24))
        
        # Criar um DataFrame para armazenar os percentuais
        progress_data = {'Dia': [], 'Planejado - % Completo': []}
        
        # Total de trabalho em horas
        total_work = self.total_amount_of_work
    
        for day in range(1, total_days + 1):
            # Calcular o total de horas concluídas até o final do dia atual
            completed_hours = self.dtm[self.dtm['End Time (h)'] <= day*24]['Duração Planejada (h)'].sum()
            
            # Calcular o percentual de conclusão
            percent_complete = round((completed_hours / total_work) * 100,1)
            
            # Adicionar os valores ao progresso
            progress_data['Dia'].append(day)
            progress_data['Planejado - % Completo'].append(percent_complete)
        
        # Converter para DataFrame
        self.progress_df = pd.DataFrame(progress_data)
    
    def calculate_daily_progress(self, excel_file):
        self.daily_progress = pd.read_excel(excel_file, sheet_name='Progresso', index_col='id')
        daily_cols = list(self.progress_df['Dia'])
        filled_days = self.daily_progress[daily_cols].sum()!=0
        filled_days = filled_days[filled_days].index
        
        indices = self.daily_progress.index
        for idx in indices:
            carry_on_val = np.nan
            for day in filled_days:
                if (not pd.isna(self.daily_progress.loc[idx,day])):
                    carry_on_val = self.daily_progress.loc[idx,day]
                elif pd.isna(self.daily_progress.loc[idx,day]) and carry_on_val>0:
                    self.daily_progress.loc[idx,day]=carry_on_val
                
        planned_duration_col = self.daily_progress.loc[:,'Duração Planejada (h)']
        self.progress_df['Executado - % Completo'] = np.nan
        for day in filled_days:
            daily_sum = planned_duration_col*self.daily_progress.loc[:,day]/100
            daily_percentage = 100*daily_sum.sum()/self.total_amount_of_work
            daily_percentage = round(daily_percentage,2)
            mask = self.progress_df['Dia']==day
            self.progress_df.loc[mask,'Executado - % Completo'] = daily_percentage

# dtm = DTM('DTM_PR-14.xlsx')