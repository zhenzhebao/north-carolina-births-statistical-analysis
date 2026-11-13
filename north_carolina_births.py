import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t

"""# Import the dataset"""

df=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSYH4AtixUO8KyxIVmbFPGtiPkmJ8EiDCHrvhvxOt0sSMildFYftmG09B6gWkj2DsT8tp8BMYGwZrdR/pub?output=csv')

#print(df.info())
#df.head()
#remove duplicates
df.drop_duplicates(inplace=True)
#print(df.info())
#following columns have been removed from the dataframe becuase we don't have the definition on how data is classified into different groups
#renamne some columns
df.drop(columns=['mature','premie','lowbirthweight'],inplace=True)
df=df.rename(columns={'fage': 'dad_age','mage':'mom_age','gained':'mom_weight_gained'})
#print(df.info())

# remove the null value from the dataset
df.drop(index=df[df['habit'].isnull()==True].index,inplace=True)
df.drop(index=df[df['whitemom'].isnull()==True].index,inplace=True)
df.drop(index=df[df['visits'].isnull()==True].index,inplace=True)
df.drop(index=df[df['weeks'].isnull()==True].index,inplace=True)
df.drop(index=df[df['dad_age'].isnull()==True].index,inplace=True)
df.drop(index=df[df['mom_weight_gained'].isnull()==True].index,inplace=True)

df.reset_index(drop=True,inplace=True)
#df.info()

#convert the data type
if len(df['dad_age'][df['dad_age']-np.floor(df['dad_age'])>0].index)==0:
       df['dad_age']=df['dad_age'].astype(int)
if len(df['weeks'][df['weeks']-np.floor(df['weeks'])>0].index)==0:
       df['weeks']=df['weeks'].astype(int)
if len(df['visits'][df['visits']-np.floor(df['visits'])>0].index)==0:
       df['visits']=df['visits'].astype(int)
if len(df['mom_weight_gained'][df['mom_weight_gained']-np.floor(df['mom_weight_gained'])>0].index)==0:
       df['mom_weight_gained']=df['mom_weight_gained'].astype(int)

df.info()

#print('Yougest age for a monther:',df['mom_age'].min(),', Oldest age for a monther:',df['mom_age'].max())
#print('Yougest age for a father:',int(df['dad_age'].min()),', Oldest age for a father:',int(df['dad_age'].max()))

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.scatter(df['mom_age'],df['dad_age'])
plt.xticks([20,25,30,35,40,45,50,55])
plt.yticks([20,25,30,35,40,45,50,55])
plt.title("Distribution of Parent's Age")
plt.xlabel('Age (Monther)')
plt.ylabel('Age (Father)')

plt.subplot(1,2,2)
plt.hist(df['mom_weight_gained'])
plt.title("Distribution of the weight gained during Pregnancy")
plt.xlabel('Weight')
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10,10))

plt.subplot(2,2,1)
#plt.figure(figsize=(12,6))
counts,bins,patches=plt.hist(df['mom_age'],bins=[15,20,25,30,35,40,45,50])
plt.bar_label(patches, fmt='%.0f', padding=1)
plt.title("Distribution of Age")
plt.xlabel('Age')
plt.ylabel("Frequency")
#plt.show()

plt.subplot(2,2,2)
#plt.figure(figsize=(12,6))
bars=plt.bar(df['habit'].value_counts().rename(index={'nonsmoker':'Non Smoker','smoker':'Smoker'}).index,
             df['habit'].value_counts().rename(index={'nonsmoker':'Non Smoker','smoker':'Smoker'}))
plt.bar_label(bars,fmt='%.0f', padding=1)
plt.title("Smoking Status")
plt.xlabel('Status')
plt.ylabel("Counts")
#plt.show()

plt.subplot(2,2,3)
#plt.figure(figsize=(12,6))
plt.pie(df['marital'].value_counts().rename({'married':'Married','not married':'Not Married'}),
        labels=df['marital'].value_counts().rename({'married':'Married','not married':'Not Married'}).index,
        wedgeprops={'width': 0.4},autopct='%.2f%%',pctdistance=0.8)
plt.title("Marital Status")
plt.legend(loc='lower left')
#plt.tight_layout()
#plt.show()

plt.subplot(2,2,4)
#plt.figure(figsize=(12,6))
plt.pie(df['whitemom'].value_counts().rename(index={'white':'White','not white':'Not White'}),
        labels=df['whitemom'].value_counts().rename(index={'white':'White','not white':'Not White'}).index,autopct='%.02f%%')
plt.legend(loc='lower left')
plt.title('Demographic Distribution')
#plt.tight_layout()
#plt.show()

plt.suptitle('Demographic information of 800 Mothers', fontsize=16)
plt.tight_layout()
plt.show()

#print('Minimum length of Pregnancy', df['weeks'].min(),', Maximum length of Pregnancy',df['weeks'].max())
#print('Minimum amount of visits',df['visits'].min(),', Maximum amount of visits',df['visits'].max())
conditions=[df['visits']==0,df['visits']<10,df['visits']<=15,df['visits']<=20,df['visits']<=30]
choices=['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20']
df['visits_groupped']=np.select(conditions,choices,default='N/A')
#df['visits_groupped'].value_counts().reindex(['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20'])

#print('Minimum baby weight',df['weight'].min(),', Maximum baby weight',df['weight'].max())
conditions=[df['weight']<2.2,df['weight']<3.3,df['weight']<5.5,df['weight']<8.8,df['weight']<=11.63]
choices=['Extremely Low','Very Low','Low','Typical Range','High']
df['weight_groupped']=np.select(conditions,choices,default='N/A')
#df['weight_groupped'].value_counts().reindex(['Extremely Low','Very Low','Low','Typical Range','High'])



plt.figure(figsize=(11,11))
plt.subplot(2,2,1)
counts,bars,patches=plt.hist(df['weeks'],bins=[20,25,30,35,40,45])
plt.bar_label(patches,fmt='%.0f',padding=1)
plt.title("Length of Pregnancy")
plt.xlabel('Length')
plt.ylabel('Frequency')

plt.subplot(2,2,2)
bars=plt.bar(df['visits_groupped'].value_counts().reindex(['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20']).index,
        df['visits_groupped'].value_counts().reindex(['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20']))
plt.xticks(rotation=45)
plt.title('Number of Hospital Visits during Pregnancy')
plt.xlabel("Category")
plt.ylabel('Counts')
plt.bar_label(bars,fmt='%.0f',padding=1)

plt.subplot(2,2,3)
bars=plt.bar(df['weight_groupped'].value_counts().reindex(['Extremely Low','Very Low','Low','Typical Range','High']).index,
        df['weight_groupped'].value_counts().reindex(['Extremely Low','Very Low','Low','Typical Range','High']))
plt.title('Distribution of the Weight')
plt.bar_label(bars,fmt='%.0f',padding=1)
plt.xlabel('Category')
plt.ylabel('Counts')

plt.subplot(2,2,4)
plt.pie(df['gender'].value_counts().rename(index={'female':'Female','male':'Male'}),
        labels=df['gender'].value_counts().rename(index={'female':'Female','male':'Male'}).index,autopct='%.2f%%')
plt.title('Geneder')
plt.legend(title='Gender',loc='lower right')

plt.suptitle("Information about 800 Newborns",size=16)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.scatter(df['visits'],df['weeks'])
plt.title('Number of Visits vs Length of Pregnancy')
plt.xlabel('Number of Visits')
plt.ylabel('Length of Pregnancy')

plt.subplot(1,2,2)
plt.scatter(df['mom_weight_gained'],df['weeks'])
plt.title('Weight Gain during Pregnancy vs Length of Pregnancy')
plt.xlabel('Weight gain')
plt.ylabel('Length of Pregnancy')

plt.tight_layout()
plt.show()

"""# Prepare the Sample for Analysis

We want to evaluate that is there a difference for the mean of the pregnancy length between women in age 20-29 and women in age 30-39. All women in both groups are non-smoker, white female and married.
"""

#print(df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & ((df['mom_age']>=20)& (df['mom_age']<=29))].info())
#print(df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married')& (df['mom_age']<=39) & (df['mom_age']>=30)].info())
Age_20=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & ((df['mom_age']>=20)& (df['mom_age']<=29))]
Age_20.reset_index(drop=True,inplace=True)
Age_30_raw=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married')& (df['mom_age']<=39) & (df['mom_age']>=30)]
Age_30=Age_30_raw.sample(n=198,random_state=42)
Age_30.reset_index(drop=True,inplace=True)

"""The data source documented that the original 1000 cases are randomly selected, therefore I assume each record is independent. Based on central limit theorem, even if the true population are not normally distributed, when the sample size is large enough (our sample size is 198), the sampling distribution of the sampling mean is also approximately, therefore the distribution of the difference between these two sampling mean is also approximately normal.

The null Hypothesis is that the mean of the pregnancy length between these group is the same.
The alternative Hypothesis is that the mean of the pregnancy length between these two group is difference.
Therefore, this is a two-tail test. The significant level we use is 0.05.
"""

# calculate the variance for each sample
Age_20_var=Age_20['weeks'].var()
Age_30_var=Age_30['weeks'].var()
#calculate the mean for each group
Age_20_mean=Age_20['weeks'].mean()
Age_30_mean=Age_30['weeks'].mean()
sample_size=198
# calculate the standard deviation
standard_deviation=np.sqrt(Age_20_var/sample_size+Age_30_var/sample_size)
#calculate the t statistics
t_statistics=(Age_20_mean-Age_30_mean)/standard_deviation
print(t_statistics)
# calculate the degree of freedom
degree_of_freedom=np.square(Age_20_var/sample_size+Age_30_var/sample_size)/(np.square(Age_20_var/sample_size)/(sample_size-1)+np.square(Age_30_var/sample_size)/(sample_size-1))
print(degree_of_freedom)
# determine the rejection region
#left tail
print(t.ppf(0.025,degree_of_freedom))
#right tail
print(t.ppf(0.975,degree_of_freedom))

print('When the t statistics is less than',round(t.ppf(0.025,degree_of_freedom),2), 'or when the t statistics is bigger than',round(t.ppf(0.975,degree_of_freedom),2),'we reject null hypothesis')
print('Becuase t statistics is',round(t_statistics,2), 'therefore we reject null hypothesis')
print('Conclusion: At the significant level of 5%, there is sufficient evidence that the mean of pregnancy length between women in age 20-29 and in age 30-39 is different')