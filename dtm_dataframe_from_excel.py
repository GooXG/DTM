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
        self.calculate_class_task_percentage()
 
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

    def calculate_class_task_percentage(self):
        class_task_list = ['Organização e Logística', 
                           'Transporte e Movimentação',
                           'Preparação e Desmontagem', 
                           'Desinstalação, Instalação e Manutenção',
                           'Montagem Final']
        
        daily_cols = list(self.progress_df['Dia'])
        last_valid_day = 0
        for day in daily_cols[-1::-1]:
            if not self.daily_progress.loc[:,day].isna().all():
                last_valid_day = day
                break
        worked_hours = self.daily_progress.loc[:,last_valid_day]
        worked_hours *= self.daily_progress.loc[:,'Duração Planejada (h)']/100
        self.daily_progress['Duração Executada (h)'] = worked_hours
        hours_class_task = self.daily_progress.groupby('Classe da Tarefa')[['Duração Planejada (h)', 'Duração Executada (h)']].sum()
                
        self.class_task_percentage = {}
        for class_task in class_task_list:
            mask = hours_class_task.index == class_task
            planned_hours = hours_class_task[mask]['Duração Planejada (h)'].iloc[0]
            executed_hours = hours_class_task[mask]['Duração Executada (h)'].iloc[0]
            self.class_task_percentage[class_task] = round(100*executed_hours/planned_hours,2)

#dtm = DTM('DTM_PR-14.xlsx')