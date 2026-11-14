import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t
from scipy.stats import norm

"""# Import the dataset and Data cleaning"""

df=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSYH4AtixUO8KyxIVmbFPGtiPkmJ8EiDCHrvhvxOt0sSMildFYftmG09B6gWkj2DsT8tp8BMYGwZrdR/pub?output=csv')

#print(df.info())
#df.head()
#remove duplicates
df.drop_duplicates(inplace=True)
#print(df.info())
#following columns have been removed from the dataframe becuase we don't have the definition on how data is classified into different groups
df.drop(columns=['mature','premie','lowbirthweight'],inplace=True)
#renamne some columns
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

"""# Overview"""

#print('Yougest age for a mother:',df['mom_age'].min(),', Oldest age for a mother:',df['mom_age'].max())
#print('Yougest age for a father:',int(df['dad_age'].min()),', Oldest age for a father:',int(df['dad_age'].max()))

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.scatter(df['mom_age'],df['dad_age'])
plt.xticks([20,25,30,35,40,45,50,55])
plt.yticks([20,25,30,35,40,45,50,55])
plt.title("Parents' Ages")
plt.xlabel('Age (Mother)')
plt.ylabel('Age (Father)')

plt.subplot(1,2,2)
counts,bars,patches=plt.hist(df['mom_weight_gained'])
plt.title("Mother's Weight Gain During Pregnancy")
plt.bar_label(patches,fmt='%.0f',padding=1)
plt.xlabel('Weight (pounds)')
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10,10))

plt.subplot(2,2,1)
#plt.figure(figsize=(12,6))
counts,bins,patches=plt.hist(df['mom_age'],bins=[15,20,25,30,35,40,45,50])
plt.bar_label(patches, fmt='%.0f', padding=1)
plt.title("Mothers' Ages")
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
plt.xlabel('Length (Weeks)')
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
plt.title('Gender')
plt.legend(title='Gender',loc='lower right')

plt.suptitle("Information about 800 Newborns",size=16)
plt.tight_layout()
plt.show()

"""# Analysis

The first two questions focus on two groups of women: those aged 20–29 and those aged 30–39. To improve comparability between the groups, both groups include only women who are nonsmokers, married, and white.

The first analysis investigates whether there is a difference in mean pregnancy duration between the two groups. The second analysis examines whether the proportion of newborns with low birth weight differs between the groups. (A newborn weighing less than 5.5 pounds is classified as having low birth weight.)

To include all eligible records in both groups, no additional filtering criteria are applied based on the number of visits or weight gain for the mothers during pregnancy in the first analysis. Similarly, the second analysis does not apply additional filters based on weight gain for the mothers during pregnancy, pregnancy duration, or the number of visits.

The third analysis investigates whether there is a difference in mean birth weight between male and female newborns. Both groups include only newborns whose mothers are nonsmokers, white, and married. To include all eligible observations, no additional filtering criteria are applied to the other variables.

A significance level of 5% (α = 0.05) is used for all analyses.

# Prepare the Sample for Analysis
"""

# plt.figure(figsize=(10,5))
# plt.subplot(1,2,1)
# plt.scatter(df['visits'],df['weeks'])
# plt.title('Number of Visits vs Length of Pregnancy')
# plt.xlabel('Number of Visits')
# plt.ylabel('Length of Pregnancy')

# plt.subplot(1,2,2)
# plt.scatter(df['mom_weight_gained'],df['weeks'])
# plt.title('Weight Gain during Pregnancy vs Length of Pregnancy')
# plt.xlabel('Weight gain')
# plt.ylabel('Length of Pregnancy')

# plt.tight_layout()
# plt.show()

#print(df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & ((df['mom_age']>=20)& (df['mom_age']<=29))].info())
#print(df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married')& (df['mom_age']<=39) & (df['mom_age']>=30)].info())
Age_20=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & ((df['mom_age']>=20)& (df['mom_age']<=29))]
Age_20.reset_index(drop=True,inplace=True)
Age_30_raw=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married')& (df['mom_age']<=39) & (df['mom_age']>=30)]
Age_30=Age_30_raw.sample(n=198,random_state=42)
Age_30.reset_index(drop=True,inplace=True)

Age_20['low_birth_weight']=np.where(Age_20['weight']<5.5,1,0)
Age_30['low_birth_weight']=np.where(Age_30['weight']<5.5,1,0)

"""According to the dataset documentation, the original 1,000 observations were obtained through random sampling. After applying the eligibility criteria, a random sample was drawn from the 30–39 age group to ensure that both age groups contained the same number of observations. Based on the original sampling method, the observations are assumed to be independent.

Each group contains 198 observations, providing a relatively large sample size. According to the Central Limit Theorem, when the sample size is sufficiently large, the sampling distribution of the sample mean is approximately normal, even if the underlying population is not normally distributed. Similarly, the sampling distribution of the sample proportion can be approximated by a normal distribution when the required conditions are satisfied.
"""

# Analysis 1
# Null Hypothesis, the mean pregnancy duration between the two groups is same
# Alternative Hypothesis, the mean pregnancy duration between the two groups is different

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
print('t_statistics',t_statistics)
# calculate the degree of freedom
degree_of_freedom=np.square(Age_20_var/sample_size+Age_30_var/sample_size)/(np.square(Age_20_var/sample_size)/(sample_size-1)+np.square(Age_30_var/sample_size)/(sample_size-1))
print('degree_of_freedom',degree_of_freedom)
# determine the rejection region
#left tail
#print(t.ppf(0.025,degree_of_freedom))
#right tail
#print(t.ppf(0.975,degree_of_freedom))

print('When the t statistics is less than',round(t.ppf(0.025,degree_of_freedom),2), 'or when the t statistics is bigger than',round(t.ppf(0.975,degree_of_freedom),2),'we reject null hypothesis')
print('Becuase t statistics is',round(t_statistics,2), 'therefore we reject null hypothesis')
print('Conclusion: At the significant level of 5%, there is sufficient evidence that the mean of pregnancy length between women in age 20-29 and in age 30-39 is different')
print((Age_20_mean,Age_30_mean))
print('Age group 20',np.floor(Age_20_mean),'weeks',round((Age_20_mean-np.floor(Age_20_mean))*7,2),'days,',
      'Age group 30',np.floor(Age_30_mean),'weeks',round((Age_30_mean-np.floor(Age_30_mean))*7,2),'days,',
      'Difference',round((Age_20_mean-Age_30_mean)*7,2),'days')
print('According to CDC, a term pregnancy was defined as 37–41 completed weeks of gestation.')

# Analysis 2
#calculated the pooled sample proportition
p_hat=(Age_20['low_birth_weight'].sum()+Age_30['low_birth_weight'].sum())/(Age_20['weight'].count()+Age_30['weight'].count())
#verify the assumption about normality
if p_hat*Age_20['weight'].count()>=10 and Age_20['weight'].count()*(1-p_hat)>=10 and p_hat*Age_30['weight'].count()>=10 and Age_30['weight'].count()*(1-p_hat)>=10:
  print('Assumption is meet')
# Null Hypothesis: The proportion of newborns with low birth weight is same in both groups.
# Alternative Hypothesis: The proportion of newborns with low birth weight is different in both groups.
# calculate the proportion of newborns with low birth weight in both group
Age_20_porportion=Age_20['low_birth_weight'].sum()/Age_20['weight'].count()
Age_30_porportion=Age_30['low_birth_weight'].sum()/Age_30['weight'].count()
print(Age_20_porportion)
print(Age_30_porportion)
#calculate the z statistics
z_statistics=(Age_20_porportion-Age_30_porportion)/np.sqrt(p_hat*(1-p_hat)*(1/Age_20['weight'].count()+1/Age_30['weight'].count()))
print('z_statistics',z_statistics)
# determine the rejection region
#left tail
#print(norm.ppf(0.025))
#right tail
#print(norm.ppf(0.975))
print('If the z statistics is less than',round(norm.ppf(0.025),2),'or larger than',round(norm.ppf(0.975),2), 'we reject null hypothesis')
print('Becuase z statistics is', round(z_statistics,2),'we failed to reject null hypothesis')
print('Conclusion: At the significance level of 5%, there isn\'t sufficient evidence that the porportion of newborns with low birth weight is different in both groups.' )

"""## Prepare the Sample for analysis"""

baby_male=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & (df['gender']=='male')]
baby_female_raw=df[(df['habit']=='nonsmoker') & (df['whitemom']=='white') & (df['marital']=='married') & (df['gender']=='female')]
baby_male.reset_index(drop=True,inplace=True)
baby_female=baby_female_raw.sample(n=208,random_state=42)
baby_female.reset_index(drop=True,inplace=True)

# Analysis 3
# Null Hypothesis: the weight between male and femal baby is the same
# Alternative Hypothesis: the weight between male and femal baby is the different
#calculate the mean for each group
baby_male_mean=baby_male['weight'].mean()
baby_female_mean=baby_female['weight'].mean()
# calculate the standard deviation for both group
baby_male_variance=baby_male['weight'].var()
baby_female_variance=baby_female['weight'].var()
# calculate the t statistics
sample_size=208
t_statistics=(baby_male_mean-baby_female_mean)/np.sqrt(baby_male_variance/sample_size+baby_female_variance/sample_size)
print('t_statistics',t_statistics)
degree_of_freedom=np.square(baby_male_variance/sample_size+baby_female_variance/sample_size)/(np.square(baby_male_variance/sample_size)/(sample_size-1)+np.square(baby_female_variance/sample_size)/(sample_size-1))
#determine the rejection region
#left tail
print(t.ppf(0.025,degree_of_freedom))
#right tail
print(t.ppf(0.975,degree_of_freedom))
print('We reject null hypothesis if the t statistics is less than', round(t.ppf(0.025,degree_of_freedom),2),'or bigger than',round(t.ppf(0.975,degree_of_freedom),2))
print('The t statistics is ', round(t_statistics,2),'therefore we reject null hypothesis')
print('Mean weight for male baby (pounds)',round(baby_male_mean,2),'Mean weight for female baby (pounds)',round(baby_female_mean,2),'difference (pounds)',round(baby_male_mean-baby_female_mean,2))
print('A baby with weight between 5.5 pounds and 8.8 pounds considered as typical range')

# code for export graphs
#plt.figure(figsize=(10,10))
# counts,bins,patches=plt.hist(df['mom_age'],bins=[15,20,25,30,35,40,45,50])
# plt.bar_label(patches, fmt='%.0f', padding=1,fontsize=14)
# plt.title("Mothers' Ages",fontsize=25,pad=15)
# plt.xlabel('Age',fontsize=18,labelpad=10)
# plt.ylabel("Frequency",fontsize=18,labelpad=10)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)



#plt.figure(figsize=(12,6))
# bars=plt.bar(df['habit'].value_counts().rename(index={'nonsmoker':'Non Smoker','smoker':'Smoker'}).index,
#              df['habit'].value_counts().rename(index={'nonsmoker':'Non Smoker','smoker':'Smoker'}))
# plt.bar_label(bars,fmt='%.0f', padding=1,fontsize=14)
# plt.title("Smoking Status",fontsize=25,pad=15)
# plt.xlabel('Status',fontsize=18,labelpad=10)
# plt.ylabel("Counts",fontsize=18,labelpad=10)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# plt.scatter(df['mom_age'],df['dad_age'])
# plt.xticks([20,25,30,35,40,45,50,55],fontsize=14)
# plt.yticks([20,25,30,35,40,45,50,55],fontsize=14)
# plt.title("Parents' Ages",fontsize=25,pad=15)
# plt.xlabel('Age (Mother)',fontsize=18,labelpad=10)
# plt.ylabel('Age (Father)',fontsize=18,labelpad=10)

# counts,bars,patches=plt.hist(df['mom_weight_gained'])
# plt.title("Mother's Weight Gain During Pregnancy",fontsize=25,pad=15)
# plt.bar_label(patches,fmt='%.0f',padding=1,fontsize=14)
# plt.xlabel('Weight (pounds)',fontsize=18,labelpad=10)
# plt.ylabel("Frequency",fontsize=18,labelpad=10)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# plt.pie(df['marital'].value_counts().rename({'married':'Married','not married':'Not Married'}),
#         labels=df['marital'].value_counts().rename({'married':'Married','not married':'Not Married'}).index,
#         wedgeprops={'width': 0.4},autopct='%.2f%%',pctdistance=0.8,textprops={'fontsize': 18},colors=['#1F77B4', '#369E96'])
# plt.title("Marital Status",fontsize=25,pad=15)
# plt.legend(loc='lower left',fontsize=18,frameon=False)

# plt.pie(df['whitemom'].value_counts().rename(index={'white':'White','not white':'Not White'}),
#         labels=df['whitemom'].value_counts().rename(index={'white':'White','not white':'Not White'}).index,autopct='%.02f%%',textprops={'fontsize': 18},colors=['#1F77B4', '#DE858B'])
# plt.legend(loc='lower left',fontsize=18,frameon=False)
# plt.title('Demographic Distribution',fontsize=25,pad=15)


# counts,bars,patches=plt.hist(df['weeks'],bins=[20,25,30,35,40,45])
# plt.bar_label(patches,fmt='%.0f',padding=1,fontsize=14)
# plt.title("Length of Pregnancy",fontsize=25,pad=15)
# plt.xlabel('Length (Weeks)',fontsize=18,labelpad=10)
# plt.ylabel('Frequency',fontsize=18,labelpad=10)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# bars=plt.bar(df['visits_groupped'].value_counts().reindex(['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20']).index,
#         df['visits_groupped'].value_counts().reindex(['No Visits','Less Than 10','10 to 15','16 to 20','More Than 20']))
# plt.xticks(rotation=45)
# plt.title('Number of Hospital Visits during Pregnancy',fontsize=25,pad=15)
# plt.xlabel("Category",fontsize=18,labelpad=10)
# plt.ylabel('Counts',fontsize=18,labelpad=10)
# plt.bar_label(bars,fmt='%.0f',padding=1,fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)


# bars=plt.bar(df['weight_groupped'].value_counts().reindex(['Extremely Low','Very Low','Low','Typical Range','High']).index,
#         df['weight_groupped'].value_counts().reindex(['Extremely Low','Very Low','Low','Typical Range','High']))
# plt.title('Distribution of the Weight',fontsize=25,pad=15)
# plt.bar_label(bars,fmt='%.0f',padding=1,fontsize=14)
# plt.xlabel('Category',fontsize=18,labelpad=10)
# plt.ylabel('Counts',fontsize=18,labelpad=10)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# plt.pie(df['gender'].value_counts().rename(index={'female':'Female','male':'Male'}),
#         labels=df['gender'].value_counts().rename(index={'female':'Female','male':'Male'}).index,autopct='%.2f%%',textprops={'fontsize': 18},colors=['#1F77B4', '#369E96'])
# plt.title('Gender',fontsize=25,pad=15)
# plt.legend(loc='lower right',fontsize=18,frameon=False)

# plt.savefig("chart.png", transparent=True, dpi=300)
# plt.show()
