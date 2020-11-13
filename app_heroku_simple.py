import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


st.write("""
# Simple Boiler data processing   App
""")

st.sidebar.header('upload input data file')
uploaded_file = st.sidebar.file_uploader("Upload your input file",type=["csv","xlsx"])
if uploaded_file is not None:

	# Collects user input features into dataframe
	
	data1 = st.cache(pd.read_csv)(uploaded_file,parse_dates=True,index_col='Timestamp')
	data2=pd.read_csv(uploaded_file,parse_dates=True)
	
else :
	data1 = st.cache(pd.read_csv)('Effimax - Sunidhi - History.csv',parse_dates=True,index_col='Timestamp')
	data1=data1.loc[data1['EFF_Boiler_ON'] == 1]
	data2=pd.read_csv('Effimax - Sunidhi - History.csv',parse_dates=True)
	data2=data2.loc[data2['EFF_Boiler_ON'] == 1]
	


orignaldata=data1.dropna()

is_check = st.checkbox("Display orignal Data")
if is_check:
    st.write("Orignal Data")
    st.write(orignaldata)
    
    
feature= st.sidebar.multiselect("select The feature",orignaldata.columns)

data=pd.DataFrame(orignaldata[feature])
data=data.dropna()
is_check1=st.checkbox("Display selected feature Data")
if is_check1:
    st.write("Selected Feature Data")
    st.write(data)
l=len(feature)
list1=range(0,l)

####################    Plotting correlation Matrix  ##################################
is_check5=st.checkbox("Display selected features correlation matrix with all features")

data3=data2.drop(columns=['Timestamp'])
corr = data3.corr()

if is_check5:
	for i in list1:
		#data1[feature[i]].plot.hist()
		corr1=corr[feature[i]].sort_values(ascending=False)
		df=pd.DataFrame(corr1)
		st.write(df)
		y=[]
		z=[]
		r=corr1.size
		#print(r)
		X=range(0,r)
		for j in X:
    		#print(corr1[i])
    			y.append(corr1[j])
    			z.append(corr1.index[j])
		plt.figure(figsize=(15,10))
		sns.barplot(y,z) 
		
		plt.show()
		plt.title(feature[i]+"_Correlation_Matrix")
		st.pyplot()
     
#####################	Plotting Histograms	#############################################

is_check4=st.checkbox("Display selected feature histograms")

if is_check4:
	for i in list1:
		data1[feature[i]].plot.hist()
		#data1[feature[i]].hist()
		plt.show()
		plt.legend([feature[i]])
		st.pyplot()

####################	 Ploting hourly and daily and weekly available data for selected feature ###############################
   

hourly = data.resample('H').mean() 
hourly=hourly.dropna()
# Converting to daily mean 
daily = data.resample('D').mean() 
daily=daily.dropna()
# Converting to weekly mean 
weekly = data.resample('W').mean() 
weekly=weekly.dropna()
# Converting to monthly mean 
monthly = data.resample('M').mean()
monthly=monthly.dropna()
#Converting to minitly mean
minitly=data.resample('min').mean() 
minitly=minitly.dropna()

plot_timeline = st.sidebar.radio('Plot data Timeline', ['Minitly','Hourly', 'Daily', 'Weekly', 'Monthly','Weekend'])

is_check2=st.checkbox("Display selected feature data timeline plots")

if is_check2:
	if plot_timeline == 'Minitly':
		st.line_chart(minitly)
	
	if plot_timeline == 'Hourly':
		st.line_chart(hourly)
	
	if plot_timeline == 'Weekly':
		st.line_chart(weekly)
	
	if plot_timeline == 'Daily':
		st.line_chart(daily)
	
	if plot_timeline == 'Monthly':
		st.line_chart(monthly)


############################	Plotting Mean timeline data bar chart     ############################
data3=data2
data3['Datetime'] = pd.to_datetime(data2.Timestamp ,format='%Y-%m-%d %H:%M') 
i=data3

i['year']=i.Datetime.dt.year 
i['month']=i.Datetime.dt.month 
i['day']=i.Datetime.dt.day
i['Hour']=i.Datetime.dt.hour 
i["Week"]=i.Datetime.dt.day_name()
data4=i


data4['day of week']=data4['Datetime'].dt.dayofweek 
temp = data4['Datetime']
def applyer(row):
    if row.dayofweek == 5 or row.dayofweek == 6:
        return 1
    else:
        return 0 
temp2 = data4['Datetime'].apply(applyer) 
data4['weekend']=temp2
data4.index = data4['Datetime'] # indexing the Datetime to get the time period on the x-axis. 

is_check3=st.checkbox("Display selected feature Mean value timeline bar plots")


if is_check3:
	for i in list1:
   
		if plot_timeline == 'Minitly':
			st.bar_chart(minitly)
	
		if plot_timeline == 'Hourly':
			#st.line_chart(data4.groupby('Hour')[feature[i]].mean())
	
			st.bar_chart(data4.groupby('Hour')[feature[i]].mean())
	
		if plot_timeline == 'Weekly':
			st.bar_chart(data4.groupby('Week')[feature[i]].mean())
	
		if plot_timeline == 'Daily':
			st.bar_chart(data4.groupby('day')[feature[i]].mean())
	
		if plot_timeline == 'Monthly':
			st.bar_chart(data4.groupby('month')[feature[i]].mean())
		if plot_timeline == 'Weekend':
			st.bar_chart(data4.groupby('weekend')[feature[i]].mean())



		

