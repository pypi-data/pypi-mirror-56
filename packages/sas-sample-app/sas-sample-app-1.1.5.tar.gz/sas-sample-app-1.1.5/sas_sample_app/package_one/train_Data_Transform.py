# coding: utf-8

# In[1]:


#Data Processing

from dateutil.parser import parse
from sklearn.preprocessing import LabelEncoder
import glob
import pickle

#Model
from sklearn import tree
from sklearn.preprocessing import StandardScaler  
from sklearn.model_selection import train_test_split

#Azure

#Statistics
#import statistics
from scipy.stats import zscore
from sklearn.metrics import accuracy_score

#Other
from sklearn.pipeline import Pipeline

#python
import pandas as pd
import numpy as np

class trainDataTransform():
    def __init__(self):
        self.df = None
    
    def getBlob(self, blobName, isDownloadData):
        from azure.storage.blob import BlobClient
        self.blob = BlobClient(account_url="https://sasffpfraud.blob.core.windows.net",
                  container_name = "pai-data",
                  blob_name = blobName,
                  credential="YP7R4YfmFW4uB84ORaAWj4q69fZJytWQulPi8umebDgLvedGaBtClYMHLM7jo7bsskzRjYz0Nl/A22g4bEDZAg==")
#         from azure.storage.blob import BlockBlobService
#         block_blob_service = BlockBlobService(account_name='sasffpfraud', account_key='YP7R4YfmFW4uB84ORaAWj4q69fZJytWQulPi8umebDgLvedGaBtClYMHLM7jo7bsskzRjYz0Nl/A22g4bEDZAg==')
        
        if(isDownloadData):
#           block_blob_service.get_blob_to_path('pai-data', blobName, blobName)
          with open(blobName, "wb") as f:
            data = self.blob.download_blob()
            data.readinto(f)
        else:
#           block_blob_service = BlockBlobService(account_name='sasffpfraud', account_key='YP7R4YfmFW4uB84ORaAWj4q69fZJytWQulPi8umebDgLvedGaBtClYMHLM7jo7bsskzRjYz0Nl/A22g4bEDZAg==')

#           block_blob_service.create_blob_from_path(container_name="pai-data",blob_name=blobName,file_path='./'+blobName+'.pkl')
          with open(blobName, "rb") as data:
            blob.upload_blob(data,overwrite =True)

            
    def pickleData(self, createPickle, pickleName, file):
        import pickle
        if(createPickle):
            #outfile = open('./'+ pickleName+'.pkl','wb')
            outfile = open(pickleName,'wb')
            pickle.dump(file, outfile)
            outfile.close()
        else:
            infile = open(pickleName,'rb')
            #infile = open('./'+ pickleName,'rb')
            data = pickle.load(infile)
            infile.close()
            return data
#           with open('./'+ pickleName+'.pkl', 'rb') as f:
#             data = pickle.load(f)
#             return data
          
        
#     def replaceNumericNAN(self, df):#done
#         if(self.isTrain):
#             df['RETRO_ACRL_AUTH'] = df['RETRO_ACRL_AUTH'].fillna(0)
#             df['MKT_FLTNO'] = df.MKT_FLTNO.fillna(0)
#             df['RETRO_ACRL_AUTH'] = df['RETRO_ACRL_AUTH'].fillna(0)
#             df['MEM_TKTD_NAME_LEN'] = df['MEM_TKTD_NAME_LEN'].fillna(0)
#             df['km_dist'] = df['km_dist'].fillna(0)
#             df['members_withsame_mail'] = df['members_withsame_mail'].fillna(0)
#         else:
#             df.fillna(0, inplace=True)
#         return df
       
#     def replaceCatNAN(self, df):#done
#         df['OP_BKG_CLS'] = df['OP_BKG_CLS'].fillna('Other')
#         df['mail_domain'] = df['mail_domain'].fillna('Other')
#         return self.replaceNumericNAN(df)    

    def prevDayCalc(self, df):#done
        if(self.isTrain):
#             outfile = open('/databricks/driver/prevday_df','wb')
#             pickle.dump(df, outfile)
#             outfile.close()
            self.pickleData(True, 'prevday_df.pkl', df)
            self.getBlob('prevday_df.pkl', False)
        else:
            prod_df_errandId = df.ACCRUALERRANDID.tolist()
            self.getBlob('prevday_df.pkl', True)
            df1 = self.pickleData(False, 'prevday_df.pkl', None)
#             infile = open('/databricks/driver/prevday_df','rb')
#             df1 = pickle.load(infile)
#             infile.close()
            df = df1.append(df,ignore_index=True)
            if(self.isTrain==False):
                df = df[df['ACCRUALERRANDID'].isin(prod_df_errandId)]
                df.drop_duplicates('ACCRUALERRANDID', keep='first', inplace=True)
        df['FLT_DEP_DATE'] = pd.to_datetime(df['FLT_DEP_DATE'],utc=True) if (df['FLT_DEP_DATE'].dtype == 'O') else df['FLT_DEP_DATE']
        df['PAI_REG_DATE'] = pd.to_datetime(df['PAI_REG_DATE'],utc=True) if (df['PAI_REG_DATE'].dtype == 'O') else df['PAI_REG_DATE']
        df['UPD_TMS'] = pd.to_datetime(df['UPD_TMS'],utc=True) if (df['UPD_TMS'].dtype == 'O') else df['UPD_TMS']
        df['prev_flt_days'] = df.sort_index().sort_values(by=['FFP_MEMNO','FLT_DEP_DATE'])\
                                .groupby('FFP_MEMNO')['FLT_DEP_DATE'].apply(lambda x: x - x.shift(1)).fillna(pd.Timedelta('0 days'))
        df['prev_reg_days'] = df.sort_index().sort_values(by=['FFP_MEMNO','PAI_REG_DATE']).groupby('FFP_MEMNO')['PAI_REG_DATE'].\
                            apply(lambda x: pd.to_timedelta(x - x.shift(1)).dt.total_seconds()).fillna(0)
        df['prev_updTMS_days'] = df.sort_index().sort_values(by=['FFP_MEMNO','UPD_TMS']).groupby('FFP_MEMNO')['UPD_TMS'].\
        apply(lambda x: pd.to_timedelta(x - x.shift(1)).dt.total_seconds()).fillna(0)
        df['prev_flt_days'] = df['prev_flt_days'].apply(lambda x: x/ np.timedelta64(1, 'D'))
        df['prev_flt_days'] = df['prev_flt_days'].astype(int)
        
#         if(self.isTrain==False):
#             df = df[df['ACCRUALERRANDID'].isin(prod_df_errandId)]
            
        df.drop(['org_country','org_cont','dest_country','dest_cont','org_type','dest_type','MKT_AIRL'],axis=1,inplace=True)
        df.drop(['ACCRUALERRANDID','FFP_MEMNO','MEM_TKTD_NAME','MEM_LAST_NAME','MEM_FIRST_NAME','FLT_DEP_DATE','TICKETNO',\
         'PAI_REG_DATE','UPD_TMS','UPD_BY','MEMBER_EMAIL_ADDRESS'],axis=1,inplace=True)
        
        return df
        
    def extraFeat(self, df,cols):#done
        extraFeat = {} if self.isTrain else None
        for col in cols:
            if(self.isTrain):
                commonList = list(list(set(df[df['class']==1][col].unique()).intersection(set(df[df['class']==0][col].unique()))))
                genuineList = list(set(df[df['class']==0]['UPD_BY'].unique()) - set(df[df['class']==1]['UPD_BY'].unique()))
                extraFeat["commonList"+ col] = commonList
                extraFeat["genuineList" + col] = genuineList
                self.pickleData(True, 'extraFeat.pkl', extraFeat)
                self.getBlob('extraFeat.pkl', False)
#                 outfile = open('/databricks/driver/extraFeat','wb')
#                 pickle.dump(extraFeat, outfile)
#                 outfile.close()

            else:
#                 infile = open('/databricks/driver/extraFeat','rb')
#                 extraFeat = pickle.load(infile)
#                 infile.close()
                self.getBlob('extraFeat.pkl', True)
                extraFeat = self.pickleData(False, 'extraFeat.pkl', None)
                commonList = extraFeat["commonList"+ col]
                genuineList = extraFeat["genuineList" + col]
            
            df.loc[df[col].isin(commonList), 'is_common_'+ col] = 1
            df.loc[~df[col].isin(commonList), 'is_common_'+ col] = 0
            df.loc[df[col].isin(genuineList), 'is_only_genuine_' + col] = 1
            df.loc[~df[col].isin(genuineList), 'is_only_genuine_' + col] = 0
        return self.prevDayCalc(df)
        
    def respCodeFeat(self, df, cols):#done
        
        respCodeFeat = {} if self.isTrain else None
        for col in cols:
            if(self.isTrain):
                commonList = list(list(set(df[df['class']==1][col].unique()).intersection(set(df[df['class']==0][col].unique()))))
                genuineList = list(set(df[df['class']==0][col].unique()) - set(df[df['class']==1][col].unique()))
                respCodeFeat["commonList"+ col] = commonList
                respCodeFeat["genuineList" + col] = genuineList
                self.pickleData(True, 'respCodeFeat.pkl', respCodeFeat)
                self.getBlob('respCodeFeat.pkl', False)
#                 outfile = open('/databricks/driver/respCodeFeat','wb')
#                 pickle.dump(respCodeFeat, outfile)
#                 outfile.close()
            else:
#                 infile = open('/databricks/driver/respCodeFeat','rb')
#                 respCodeFeat = pickle.load(infile)
#                 infile.close()
                self.getBlob('respCodeFeat.pkl', True)
                respCodeFeat = self.pickleData(False, 'respCodeFeat.pkl', None)
                commonList = respCodeFeat["commonList"+ col]
                genuineList = respCodeFeat["genuineList" + col]
            
            df.loc[df[col].isin(commonList), 'is_common_'+ col] = 1
            df.loc[~df[col].isin(commonList), 'is_common_'+ col] = 0
            df.loc[df[col].isin(genuineList), 'is_only_genuine_' + col] = 1
            df.loc[~df[col].isin(genuineList), 'is_only_genuine_' + col] = 0
            if col == 'RESP_CD1':
                if(self.isTrain):
                    fraudList = list(set(df[df['class']==1][col].unique()) - set(df[df['class']==0][col].unique()))
                    self.pickleData(True, 'RESP_CD1_fraudList.pkl', fraudList)
                    self.getBlob('RESP_CD1_fraudList.pkl', False)
#                     outfile = open('/databricks/driver/RESP_CD1_fraudList','wb')
#                     pickle.dump(fraudList, outfile)
#                     outfile.close()
                else:
                    self.getBlob('RESP_CD1_fraudList.pkl', True)
                    fraudList = self.pickleData(False, 'RESP_CD1_fraudList.pkl', None)
#                     infile = open('/databricks/driver/RESP_CD1_fraudList','rb')
#                     fraudList = pickle.load(infile)
#                     infile.close()
                df.loc[df[col].isin(fraudList), 'is_only_fraud_' + col] = 1
                df.loc[~df[col].isin(fraudList), 'is_only_fraud_' + col] = 0
                
        return self.extraFeat(df, ['UPD_BY','PAI_STATUS','ACRL_POST_STA'])
        
    def bkgClassFeat(self, df):#todo
        if(self.isTrain):
            common_OP_BKG_CLS = \
            list(list(set(df[df['class']==1].OP_BKG_CLS.unique()).intersection(set(df[df['class']==0].OP_BKG_CLS.unique()))))
            only_genuine_OP_BKG_CLS = list(set(df[df['class']==0].OP_BKG_CLS.unique()) - set(df[df['class']==1].OP_BKG_CLS.unique()))
            bkgClassFeat = {}
            bkgClassFeat["common_OP_BKG_CLS"] = common_OP_BKG_CLS
            bkgClassFeat["only_genuine_OP_BKG_CLS"] = only_genuine_OP_BKG_CLS
            self.pickleData(True, 'bkgClassFeat.pkl', bkgClassFeat)
            self.getBlob('bkgClassFeat.pkl', False)
#             outfile = open('/databricks/driver/bkgClassFeat','wb')
#             pickle.dump(bkgClassFeat, outfile)
#             outfile.close()
        else:
            self.getBlob('bkgClassFeat.pkl', True)
            bkgClassFeat = self.pickleData(False, 'bkgClassFeat.pkl', None)
#             infile = open('/databricks/driver/bkgClassFeat','rb')
#             bkgClassFeat = pickle.load(infile)
#             infile.close()
            common_OP_BKG_CLS = bkgClassFeat["common_OP_BKG_CLS"]
            only_genuine_OP_BKG_CLS = bkgClassFeat["only_genuine_OP_BKG_CLS"]
        df.loc[df.OP_BKG_CLS.isin(common_OP_BKG_CLS), 'is_common_OP_BKG_CLS'] = 1
        df.loc[~df.OP_BKG_CLS.isin(common_OP_BKG_CLS), 'is_common_OP_BKG_CLS'] = 0
        df.loc[df.OP_BKG_CLS.isin(only_genuine_OP_BKG_CLS), 'is_only_genuine_OP_BKG_CLS'] = 1
        df.loc[~df.OP_BKG_CLS.isin(only_genuine_OP_BKG_CLS), 'is_only_genuine_OP_BKG_CLS'] = 0
         
        return self.respCodeFeat(df, ['RESP_CD1','RESP_CD2','RESP_CD3','RESP_CD4','RESP_CD5','RESP_CD6','OP_AIRL'])
        
    def ticketFeat(self, df):#done
        df['TICKETNO_DIGITS'] = df['TICKETNO'].astype(str).apply(len)
        df['First_TICKETNO_Digit'] = df['TICKETNO'].astype(str).apply(lambda x: float(x[:1]))
        return self.bkgClassFeat(df)
    
    def udf1(self, df): #done
        if(self.isTrain):
            mail_mem_cnt = df.groupby('MEMBER_EMAIL_ADDRESS').FFP_MEMNO.nunique().reset_index().\
            rename(columns={'FFP_MEMNO':'members_withsame_mail'})
            self.pickleData(True, 'mail_mem_cnt.pkl', mail_mem_cnt)
            self.getBlob('mail_mem_cnt.pkl', False)
#             outfile = open('/databricks/driver/mail_mem_cnt','wb')
#             pickle.dump(mail_mem_cnt, outfile)
#             outfile.close()
        else:
#             infile = open('/databricks/driver/mail_mem_cnt','rb')
#             mail_mem_cnt = pickle.load(infile)
#             infile.close()
            self.getBlob('mail_mem_cnt.pkl', True)
            mail_mem_cnt = self.pickleData(False, 'mail_mem_cnt.pkl', None)
        df = pd.merge(df,mail_mem_cnt,on='MEMBER_EMAIL_ADDRESS',how='left')
        return self.ticketFeat(df)
    
    def calc_acr_days_after_flt(self, df): #done
        df['FLT_DEP_DATE'] = pd.to_datetime(df['FLT_DEP_DATE']) if (df['FLT_DEP_DATE'].dtype == 'O') else df['FLT_DEP_DATE']
        df['PAI_REG_DATE'] = pd.to_datetime(df['PAI_REG_DATE']) if (df['PAI_REG_DATE'].dtype == 'O') else df['PAI_REG_DATE']
        df['UPD_TMS'] = pd.to_datetime(df['UPD_TMS']) if (df['UPD_TMS'].dtype == 'O') else df['UPD_TMS']
        df['days_after_flt1'] = df['PAI_REG_DATE'] - df['FLT_DEP_DATE']
        df['acr_days_after_flt'] = df['days_after_flt1'].apply(lambda x: x/ np.timedelta64(1, 'D'))
        df['acr_days_after_flt'] = df['acr_days_after_flt'].astype(int)
        df.drop('days_after_flt1', axis=1, inplace=True)
        return self.udf1(df)
        
    def airl_fltno_features(self, df): #done
        df['diff_op_mkt_airl'] = np.where(df['OP_AIRL'] == df['MKT_AIRL'], 0, 1)
        df['diff_op_mkt_fltno'] = np.where(df['OP_FLTNO'] == df['MKT_FLTNO'], 0, 1)
        
        if(self.isTrain):
            
            common_op_airl = list(list(set(df[df['class']==1].OP_AIRL.unique()).intersection(set(df[df['class']==0].OP_AIRL.unique()))))
            only_genuine_op_airl = (set(df[df['class']==0].OP_AIRL.unique()) - set(df[df['class']==1].OP_AIRL.unique()))
            
            common_MKT_AIRL = list(list(set(df[df['class']==1].MKT_AIRL.unique()).intersection(set(df[df['class']==0].MKT_AIRL.unique()))))
            only_genuine_MKT_AIRL = list(set(df[df['class']==0].MKT_AIRL.unique()) - set(df[df['class']==1].MKT_AIRL.unique()))
            
            common_OP_FLTNO = list(list(set(df[df['class']==1].OP_FLTNO.unique()).intersection(set(df[df['class']==0].OP_FLTNO.unique()))))
            only_genuine_OP_FLTNO = list(set(df[df['class']==0].OP_FLTNO.unique()) - set(df[df['class']==1].OP_FLTNO.unique()))
            
            common_MKT_FLTNO = \
            list(list(set(df[df['class']==1].MKT_FLTNO.unique()).intersection(set(df[df['class']==0].MKT_FLTNO.unique()))))
            only_genuine_MKT_FLTNO = list(set(df[df['class']==0].MKT_FLTNO.unique()) - set(df[df['class']==1].MKT_FLTNO.unique()))
            
            airl_fltno = {}
            airl_fltno["common_op_airl"] = common_op_airl
            airl_fltno["only_genuine_op_airl"] = only_genuine_op_airl
            airl_fltno["common_MKT_AIRL"] = common_MKT_AIRL
            airl_fltno["only_genuine_MKT_AIRL"] = only_genuine_MKT_AIRL
            airl_fltno["common_OP_FLTNO"] = common_OP_FLTNO
            airl_fltno["only_genuine_OP_FLTNO"] = only_genuine_OP_FLTNO
            airl_fltno["common_MKT_FLTNO"] = common_MKT_FLTNO
            airl_fltno["only_genuine_MKT_FLTNO"] = only_genuine_MKT_FLTNO
            self.pickleData(True, 'airl_fltno.pkl', airl_fltno)
            self.getBlob('airl_fltno.pkl', False)
#             outfile = open('/databricks/driver/airl_fltno','wb')
#             pickle.dump(airl_fltno, outfile)
#             outfile.close()
        else:
            self.getBlob('airl_fltno.pkl', True)
            airl_fltno = self.pickleData(False, 'airl_fltno.pkl', None)
#             infile = open('/databricks/driver/airl_fltno','rb')
#             airl_fltno = pickle.load(infile)
#             infile.close()
            common_op_airl = airl_fltno['common_op_airl']
            only_genuine_op_airl = airl_fltno['only_genuine_op_airl']
            common_MKT_AIRL = airl_fltno['common_MKT_AIRL']
            only_genuine_MKT_AIRL = airl_fltno['only_genuine_MKT_AIRL']
            common_OP_FLTNO = airl_fltno['common_OP_FLTNO']
            only_genuine_OP_FLTNO = airl_fltno['only_genuine_OP_FLTNO']
            common_MKT_FLTNO = airl_fltno['common_MKT_FLTNO']
            only_genuine_MKT_FLTNO = airl_fltno['only_genuine_MKT_FLTNO']
        
        df.loc[df.OP_AIRL.isin(common_op_airl), 'is_common_op_airl'] = 1
        df.loc[~df.OP_AIRL.isin(common_op_airl), 'is_common_op_airl'] = 0
        df.loc[df.OP_AIRL.isin(only_genuine_op_airl), 'is_only_genuine_op_airl'] = 1
        df.loc[~df.OP_AIRL.isin(only_genuine_op_airl), 'is_only_genuine_op_airl'] = 0

        
        df.loc[df.MKT_AIRL.isin(common_MKT_AIRL), 'is_common_MKT_AIRL'] = 1
        df.loc[~df.MKT_AIRL.isin(common_MKT_AIRL), 'is_common_MKT_AIRL'] = 0
        df.loc[df.MKT_AIRL.isin(only_genuine_MKT_AIRL), 'is_only_genuine_MKT_AIRL'] = 1
        df.loc[~df.MKT_AIRL.isin(only_genuine_MKT_AIRL), 'is_only_genuine_MKT_AIRL'] = 0

        
        df.loc[df.OP_FLTNO.isin(common_OP_FLTNO), 'is_common_OP_FLTNO'] = 1
        df.loc[~df.OP_FLTNO.isin(common_OP_FLTNO), 'is_common_OP_FLTNO'] = 0
        df.loc[df.OP_FLTNO.isin(only_genuine_OP_FLTNO), 'is_only_genuine_OP_FLTNO'] = 1
        df.loc[~df.OP_FLTNO.isin(only_genuine_OP_FLTNO), 'is_only_genuine_OP_FLTNO'] = 0

        
        df.loc[df.MKT_FLTNO.isin(common_MKT_FLTNO), 'is_common_MKT_FLTNO'] = 1
        df.loc[~df.MKT_FLTNO.isin(common_MKT_FLTNO), 'is_common_MKT_FLTNO'] = 0
        df.loc[df.MKT_FLTNO.isin(only_genuine_MKT_FLTNO), 'is_only_genuine_MKT_FLTNO'] = 1
        df.loc[~df.MKT_FLTNO.isin(only_genuine_MKT_FLTNO), 'is_only_genuine_MKT_FLTNO'] = 0
        return self.calc_acr_days_after_flt(df)
    
    def detailTripGroups(self, df):
        if(self.isTrain):
            detTrips = df.groupby(['ORG_AIRP','DEST_AIRP']).size().reset_index().rename(columns={0:'count'})
            detTrips['trip_det_id'] = (detTrips.index + 1)
            detTrips.drop('count',axis=1,inplace=True)
            self.pickleData(True, 'detTrips.pkl', detTrips)
            self.getBlob('detTrips.pkl', False)
#             outfile = open('/databricks/driver/detTrips','wb')
#             pickle.dump(detTrips, outfile)
#             outfile.close()
        else:
            self.getBlob('detTrips.pkl', True)
            detTrips = self.pickleData(False, 'detTrips.pkl', None)
#             infile = open('/databricks/driver/detTrips','rb')
#             detTrips = pickle.load(infile)
#             infile.close()    
        df = pd.merge(df, detTrips, on=['ORG_AIRP','DEST_AIRP'], how='left')
        return self.airl_fltno_features(df)
        
    def trip_segments(self, df):
        if(self.isTrain):
            common_tripids = list(list(set(df[df['class']==1].trip_id.unique()).intersection(set(df[df['class']==0].trip_id.unique()))))
            only_genuine_tripids = (set(df[df['class']==0].trip_id.unique()) - set(df[df['class']==1].trip_id.unique()))
            trip_segments = {}
            trip_segments["common_tripids"] = common_tripids
            trip_segments["only_genuine_tripids"] = only_genuine_tripids
            self.pickleData(True, 'trip_segments.pkl', trip_segments)
            self.getBlob('trip_segments.pkl', False)
        else:
#             infile = open('/databricks/driver/trip_segments','rb')
#             trip_segments = pickle.load(infile)
#             infile.close()
            self.getBlob('trip_segments.pkl', True)
            trip_segments = self.pickleData(False, 'trip_segments.pkl', None)
            common_tripids = trip_segments['common_tripids']
            only_genuine_tripids = trip_segments['only_genuine_tripids']
        df.loc[df.trip_id.isin(common_tripids), 'is_common_trip'] = 1
        df.loc[~df.trip_id.isin(common_tripids), 'is_common_trip'] = 0
        df.loc[df.trip_id.isin(only_genuine_tripids), 'is_only_genuine_trip'] = 1
        df.loc[~df.trip_id.isin(only_genuine_tripids), 'is_only_genuine_trip'] = 0
        return self.detailTripGroups(df)
        
    def tripGroups(self, df):
        if(self.isTrain):
            trips = df.groupby(['org_cont','dest_cont']).size().reset_index().rename(columns={0:'count'})
            trips['trip_id'] = (trips.index + 1)
            trips.drop('count',axis=1,inplace=True)
            self.pickleData(True, 'trips.pkl', trips)
            self.getBlob('trips.pkl', False)
#             outfile = open('/databricks/driver/trips','wb')
#             pickle.dump(trips, outfile)
#             outfile.close()

        else:
#             infile = open('/databricks/driver/trips','rb')
#             trips = pickle.load(infile)
#             infile.close()
              self.getBlob('trips.pkl', True)
              trips = self.pickleData(False, 'trips.pkl', None)
        df = pd.merge(df, trips, on=['org_cont','dest_cont'], how='left')
        return self.trip_segments(df)
         
    def haversine_np(self, lon1, lat1, lon2, lat2):
        
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

        c = 2 * np.arcsin(np.sqrt(a))
        km = 6367 * c
        return km
    
    def extractAirpFeat(self, df):
        #all_aircode = spark.sql("select _c3,_c4,_c11 from default.aircodes")
        #self.block_blob_service.get_blob_to_path('pai-data', 'aircodes.csv', 'aircodes.csv')
        self.getBlob('aircodes.csv', True)
        all_aircode = pd.read_csv('aircodes.csv',header=None,usecols=[3,4,11])
        #all_aircode = all_aircode.toPandas()
        all_aircode.columns = ['org_country','ORG_AIRP', 'org_cont']
        all_aircode['org_cont'] = all_aircode.org_cont.str.split('/',expand=True)[0]
        df = pd.merge(df, all_aircode, how='left', on='ORG_AIRP')

        all_aircode.columns = ['dest_country','DEST_AIRP', 'dest_cont']
        df = pd.merge(df, all_aircode, how='left', on='DEST_AIRP')

        df['Intl_trip'] = (df['org_country']!=df['dest_country']).astype(int)
        df['cont_trip'] = (df['org_cont']!=df['dest_cont']).astype(int)

        #airports_df = spark.sql("select * from default.airports_csv")
        #self.block_blob_service.get_blob_to_path('pai-data', 'airports.csv', 'airports.csv')
        self.getBlob('airports.csv', True)
        airports_df = pd.read_csv('airports.csv')
        #airports_df = airports_df.toPandas()
        airports_df = airports_df[pd.notnull(airports_df['iata_code'])].drop_duplicates('iata_code')
        airports_df.rename(columns={'iata_code':'ORG_AIRP','type':'org_type','latitude_deg': 'org_lat', 'longitude_deg': \
                                    'org_long'},inplace=True)
        x = pd.merge(df, airports_df[['ORG_AIRP','org_lat','org_long']], how='left', on='ORG_AIRP')

        airports_df.rename(columns={'ORG_AIRP':'DEST_AIRP','org_lat': 'dest_lat', 'org_long': 'dest_long'},inplace=True)
        y = pd.merge(df, airports_df[['DEST_AIRP','dest_lat','dest_long']], how='left', on='DEST_AIRP')

        x[['dest_lat','dest_long']] = y[['dest_lat','dest_long']]
        x['km_dist'] = self.haversine_np(x.org_long, x.org_lat, x.dest_long, x.dest_lat)
        df['km_dist'] = x['km_dist']

        airports_df.rename(columns={'DEST_AIRP':'ORG_AIRP','type':'org_type','dest_lat': 'org_lat', 'dest_long': 'org_long'},inplace=True)
        df = pd.merge(df, airports_df[['org_type','ORG_AIRP']], how='left', on='ORG_AIRP')
        airports_df.rename(columns={'ORG_AIRP':'DEST_AIRP','org_type':'dest_type'},inplace=True)
        df = pd.merge(df, airports_df[['dest_type','DEST_AIRP']], how='left', on='DEST_AIRP')

        df.org_cont.replace(['\\N'], 'Other',inplace=True)
        df.org_cont.fillna('Other',inplace=True)
        df.dest_cont.replace(['\\N'], 'Other',inplace=True)
        df.dest_cont.fillna('Other',inplace=True)

        return self.tripGroups(df)
        
    def calcFFPDigitsPrefix(self, df):
        df['FFP_MEMNO_DIGITS'] = df['FFP_MEMNO'].astype(str).apply(len)
        df['First_FFP_Digit'] = df['FFP_MEMNO'].astype(str).apply(lambda x: float(x[:1]))
        return self.extractAirpFeat(df)
        
    def calcNameLen(self, cols,df):
        for col in cols:
            df[col] = df[col].fillna('')
            df[col + '_LEN'] = df[col].str.lower().replace(['mr','ms'], '',regex=True).replace(' ', '', regex=True)\
                               .str.replace('[^A-Za-z\s]+', '').str.split(expand=False).str[0].str.len()
        return self.calcFFPDigitsPrefix(df)
        
    def domain_segments(self, df):
        if(self.isTrain):
            fraud_domains = (set(df[df['class']==1].mail_domain.unique()) - set(df[df['class']==0].mail_domain.unique()))
            common_mail_domains = list(set(df[df['class']==1].mail_domain.unique()).\
                                       intersection(set(df[df['class']==0].mail_domain.unique())))
            genuine_mem_domains = (set(df[df['class']==0].mail_domain.unique()) - set(df[df['class']==1].mail_domain.unique()))
            mail_dom_pick = {}
            mail_dom_pick["fraud_domains"] = fraud_domains
            mail_dom_pick["common_mail_domains"] = common_mail_domains
            mail_dom_pick["genuine_mem_domains"] = genuine_mem_domains
#             outfile = open('./mail_dom_pick','wb')
#             pickle.dump(mail_dom_pick, outfile)
#             outfile.close()
            self.pickleData(True, 'mail_dom_pick.pkl', mail_dom_pick)
            self.getBlob('mail_dom_pick.pkl', False)
            #block_blob_service.create_blob_from_path(container_name="pai-data",blob_name="mail_dom_pick.pkl",file_path='./mail_dom_pick.pkl')
            
            
        else:
#             infile = open('/databricks/driver/mail_dom_pick','rb')
#             mail_dom_pick = pickle.load(infile)
#             infile.close()
            self.getBlob('mail_dom_pick.pkl', True)
            mail_dom_pick = self.pickleData(False, 'mail_dom_pick.pkl', None)
            fraud_domains = mail_dom_pick['fraud_domains']
            common_mail_domains = mail_dom_pick['common_mail_domains']
            genuine_mem_domains = mail_dom_pick['genuine_mem_domains']
        df.loc[df.mail_domain.isin(common_mail_domains), 'is_common_mail_domains'] = 1
        df.loc[~df.mail_domain.isin(common_mail_domains), 'is_common_mail_domains'] = 0
        df.loc[df.mail_domain.isin(fraud_domains), 'is_fraud_domains'] = 1
        df.loc[~df.mail_domain.isin(fraud_domains), 'is_fraud_domains'] = 0
        df.loc[df.mail_domain.isin(genuine_mem_domains), 'is_genuine_mem_domains'] = 1
        df.loc[~df.mail_domain.isin(genuine_mem_domains), 'is_genuine_mem_domains'] = 0
        return self.calcNameLen(['MEM_TKTD_NAME','MEM_LAST_NAME','MEM_FIRST_NAME'], df)

    def mail_group(self,  df):
        df['mail_domain'] = df['MEMBER_EMAIL_ADDRESS'].str.split("@").str[1].str.lower()
        self.getBlob('validated_domains.csv', True)
        valid_dom_df = pd.read_csv('validated_domains.csv')
        df = pd.merge(df,valid_dom_df,on='mail_domain',how='left')
        return self.domain_segments(df)

    def transformData(self, df, isTrain):
        self.isTrain = isTrain
        return self.mail_group(df)