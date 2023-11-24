import pandas as pd
from datetime import datetime

class SLSTRFileNameParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_info = self.parse_file_name()

    def parse_file_name(self):
        components = self.file_name.split('_')

        return {
            "filename": file_name,
            "mission_id": components[0],
            "data_source": components[1],
            "processing_level": components[2],
            "data_type_id": components[3],
            "start_time": datetime.strptime(components[4], "%Y%m%dT%H%M%S"),
            "stop_time": datetime.strptime(components[5], "%Y%m%dT%H%M%S"),
            "creation_date": datetime.strptime(components[6], "%Y%m%dT%H%M%S"),
            "instance_id": components[7],
            "center_id": components[8],
            "class_id": components[9].split('.')[0],
            "file_extension": components[9].split('.')[1]
        }

    def get_file_info(self):
        return self.file_info

    @staticmethod
    def generate_dataframe(file_names):
        data = []
        for counter, file_name in enumerate(file_names, start=1):
            parser = SLSTRFileNameParser(file_name)
            file_info = parser.get_file_info()
            file_info['counter'] = counter
            data.append(file_info)

        return pd.DataFrame(data)

    @staticmethod
    def plot_gantt_chart(dataframe):
        # Sort DataFrame by start time for correct Gantt chart representation
        df = dataframe.sort_values(by=['start_time'])

        # Create Gantt chart
        fig = px.timeline(df, 
                          x_start='start_time', 
                          x_end='stop_time', 
                          y='counter', 
                          color='processing_level',
                          labels={'counter':'counter', 
                                  'mission_id': 'Mission ID', 
                                  'start_time': 'Start Time', 
                                  'stop_time': 'Stop Time'},
                          title='SLSTR Products Gantt Chart',
                          )

        # Add counter as the first element in the labels
        fig.update_layout(xaxis_title='Time', 
                          yaxis_title='Mission ID', 
                          showlegend=False)
        fig.update_traces(text=df.apply(lambda row: f"{row['counter']} - {row.name}", axis=1), hoverinfo='text+y')

        # Show the chart
        fig.show()




# Example usage with multiple file names
#file_names = [
#    "S3A_SL_2_LST____20151229T095534_20151229T114422_20160102T150019_6528_064_365______LN2_D_NT_001.SEN3",
#    "S3B_SL_1_RBT_BW_20160101T120000_20160101T130000_20160101T140000_GLOBAL___________LN2_R_NT_002.SEN3",
#    # Add more file names as needed
#]

# Creating a DataFrame using the class method
#df = SLSTRFileNameParser.generate_dataframe(file_names)

# Displaying the DataFrame
#print(df)
