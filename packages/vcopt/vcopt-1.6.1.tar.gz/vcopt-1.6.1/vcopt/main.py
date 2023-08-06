import math ,time ,os #line:1
import numpy as np #line:2
import numpy .random as nr #line:3
from copy import deepcopy #line:4
import matplotlib .pyplot as plt #line:5
from joblib import Parallel ,delayed #line:6
import hashlib #line:7
md5_s =['6c11f117a84c860c4044f8a1a45a0e67','cb51d4bbfdf4cc67e8bec57bc57e21c8','28f9afcaa52714aa964e215b7247a691','57f92316a9e611dd97c1528694ff6f9f','fd3dbb083970d4ba54ff6d067ab0c320','57c3d88ebf6777016c1429d25f283052','5f12a9899da112ee22a9a3ca7286b75b','9c84d4d198be8a5ef0dd96a8df934a80','df9c3ded3fe362c4c513a2bb3b28383f','12536e9b1dad1aabd97139327a115cc4','2a282b5b4649959c8a37c38e333789ad','0946a6c2e833058ced3d4798ba7ed903','432b8b1a39018c5b423f618c825a170c','46332f4160a17a9cb13fe5a559a66004','53630aba1c1685f49a216d70eb6bb7e0','acd9e269de3dcf51a4090cc907ae6ca9','affe60d5c024c79e77e7723bbca9608d','985b95f3aa925b05f3ac50561bab5dc2','2b7b9589e306a4419a7b259a1a7f1127','f9ac39e0da75c423a92003125f573429','0a988276a12594b79f9d79457371a1ad','ff4808135d6784b9a849f650cf579a46','91f88b573ccf4e2cc31da287baaff287','660440c7e709d6d3cd86293bd8ef1368','d552702c3e333e8c8e0d766c9b2c2b1c','31cd4b4c4b6964a1d4b1f78e8d2b213e','03a6a04c30c6d5b2041671c39eeec57e','503b8c8889c87da762be47d452d9fe12','146aec80f4ccdd435a2aaf7339e598e8','a02c5ad1046ed530f5e96c317300f312']#line:43
class vcopt :#line:62
    def __init__ (O00OOOOOO0O0OOO0O ):#line:63
        pass #line:64
    def __del__ (O0OOO000O0OO00O0O ):#line:65
        pass #line:66
    def setting_1 (OO000O0O0OO000O00 ,O0O0000OO0000000O ,O00O000OOO00OOOO0 ,O0O0OO00OOOO0OO00 ,OOOO000OO0OOO00O0 ,O0O00O00000O000O0 ,O00OO000000O0O000 ,OOO0OO0O00O0OO00O ,O0OO00OO00OOOOO0O ):#line:70
        OO000O0O0OO000O00 .para_range =O0O0000OO0000000O #line:71
        OO000O0O0OO000O00 .para_num =len (O0O0000OO0000000O )#line:72
        OO000O0O0OO000O00 .score_func =O00O000OOO00OOOO0 #line:73
        OO000O0O0OO000O00 .aim =float (O0O0OO00OOOO0OO00 )#line:74
        OO000O0O0OO000O00 .show_pool_func =OOOO000OO0OOO00O0 #line:75
        if OO000O0O0OO000O00 .show_pool_func ==None :pass #line:77
        elif OO000O0O0OO000O00 .show_pool_func in ['bar','print','plot']:pass #line:78
        elif callable (OO000O0O0OO000O00 .show_pool_func ):pass #line:79
        elif type (OOOO000OO0OOO00O0 )==str :#line:80
            if len (OOOO000OO0OOO00O0 )==0 or OOOO000OO0OOO00O0 [-1 ]!='/':#line:81
                OO000O0O0OO000O00 .show_pool_func ='bar'#line:82
        if type (O0O00O00000O000O0 )in [int ,float ]:#line:84
            OO000O0O0OO000O00 .seed =int (O0O00O00000O000O0 )#line:85
        else :#line:86
            OO000O0O0OO000O00 .seed =None #line:87
        nr .seed (OO000O0O0OO000O00 .seed )#line:88
        O00OO0OOOO00000O0 =1577804400.0 #line:89
        if type (O00OO000000O0O000 )in [int ,float ]:#line:91
            OO000O0O0OO000O00 .pool_num =int (O00OO000000O0O000 )#line:92
            if OO000O0O0OO000O00 .pool_num %2 !=0 :#line:94
                OO000O0O0OO000O00 .pool_num +=1 #line:95
        else :#line:96
            OO000O0O0OO000O00 .pool_num =None #line:97
        if type (OOO0OO0O00O0OO00O )in [int ,float ]:#line:99
            OO000O0O0OO000O00 .max_gen =int (OOO0OO0O00O0OO00O )#line:100
        else :#line:101
            OO000O0O0OO000O00 .max_gen =None #line:102
        OO000O0O0OO000O00 .core_num =9 -8 #line:105
        if type (O0OO00OO00OOOOO0O )in [int ,float ]:#line:106
            OO0O0OOO0OOO0OOOO =hashlib .md5 (str (O0O00O00000O000O0 ).encode ()).hexdigest ()#line:108
            if OO0O0OOO0OOO0OOOO in md5_s and time .time ()<O00OO0OOOO00000O0 :#line:109
                OO000O0O0OO000O00 .core_num =int (O0OO00OO00OOOOO0O )#line:110
        OO000O0O0OO000O00 .start =time .time ()#line:111
    def setting_2 (OO00O00O000O0O000 ,O00O0O0OO0OO0OOO0 ,OOOOO0O00O00O000O ,O0O0O00000000OOO0 ):#line:115
        if OO00O00O000O0O000 .pool_num is None :#line:117
            OO00O00O000O0O000 .pool_num =O00O0O0OO0OO0OOO0 #line:118
        OO00O00O000O0O000 .parent_num =OOOOO0O00O00O000O #line:119
        OO00O00O000O0O000 .child_num =O0O0O00000000OOO0 #line:120
        OO00O00O000O0O000 .family_num =OOOOO0O00O00O000O +O0O0O00000000OOO0 #line:121
        if OO00O00O000O0O000 .max_gen is None :#line:123
            OO00O00O000O0O000 .max_n =1000000 #line:124
        else :#line:125
            OO00O00O000O0O000 .max_n =OO00O00O000O0O000 .max_gen //OO00O00O000O0O000 .pool_num +1 #line:126
    def setting_3 (OOOOO0OO00OO0O00O ,O00O0O0O00OO00O00 ):#line:130
        OOOOO0OO00OO0O00O .pool ,OOOOO0OO00OO0O00O .pool_score =np .zeros ((OOOOO0OO00OO0O00O .pool_num ,OOOOO0OO00OO0O00O .para_num ),dtype =O00O0O0O00OO00O00 ),np .zeros (OOOOO0OO00OO0O00O .pool_num )#line:131
        OOOOO0OO00OO0O00O .parent ,OOOOO0OO00OO0O00O .parent_score =np .zeros ((OOOOO0OO00OO0O00O .parent_num ,OOOOO0OO00OO0O00O .para_num ),dtype =O00O0O0O00OO00O00 ),np .zeros (OOOOO0OO00OO0O00O .parent_num )#line:132
        OOOOO0OO00OO0O00O .child ,OOOOO0OO00OO0O00O .child_score =np .zeros ((OOOOO0OO00OO0O00O .child_num ,OOOOO0OO00OO0O00O .para_num ),dtype =O00O0O0O00OO00O00 ),np .zeros (OOOOO0OO00OO0O00O .child_num )#line:133
        OOOOO0OO00OO0O00O .family ,OOOOO0OO00OO0O00O .family_score =np .zeros ((OOOOO0OO00OO0O00O .family_num ,OOOOO0OO00OO0O00O .para_num ),dtype =O00O0O0O00OO00O00 ),np .zeros (OOOOO0OO00OO0O00O .family_num )#line:134
    def print_info (OO0OO0O0O000OO0OO ):#line:138
        if OO0OO0O0O000OO0OO .show_pool_func is not None :#line:139
            print ('___________________ info ___________________')#line:140
            print ('para_range : n={}'.format (OO0OO0O0O000OO0OO .para_num ))#line:141
            print ('score_func : {}'.format (type (OO0OO0O0O000OO0OO .score_func )))#line:142
            print ('aim : {}'.format (OO0OO0O0O000OO0OO .aim ))#line:143
            print ('show_pool_func : \'{}\''.format (OO0OO0O0O000OO0OO .show_pool_func ))#line:145
            print ('seed : {}'.format (OO0OO0O0O000OO0OO .seed ))#line:146
            print ('pool_num : {}'.format (OO0OO0O0O000OO0OO .pool_num ))#line:147
            print ('max_gen : {}'.format (OO0OO0O0O000OO0OO .max_gen ))#line:148
            if OO0OO0O0O000OO0OO .core_num ==1 :#line:149
                print ('core_num : {} (*vcopt, vc-grendel)'.format (OO0OO0O0O000OO0OO .core_num ))#line:150
            else :#line:151
                print ('core_num : {} (vcopt, *vc-grendel)'.format (OO0OO0O0O000OO0OO .core_num ))#line:152
            print ('___________________ start __________________')#line:153
    def score_pool_multi (OO0O000O0O0O000O0 ,OO00O00O00OOO0OO0 ):#line:157
        OO0OOO0000000O00O =OO0O000O0O0O000O0 .para_range [OO0O000O0O0O000O0 .pool [OO00O00O00OOO0OO0 ]]#line:158
        OO0O000O0O0O000O0 .pool_score [OO00O00O00OOO0OO0 ]=OO0O000O0O0O000O0 .score_func (OO0OOO0000000O00O )#line:159
        OO0O000O0O0O000O0 .aaa +=1 #line:160
        if OO0O000O0O0O000O0 .show_pool_func !=None :#line:161
            OOOOOOOO0O0000O00 ='\rScoring first gen {}/{}        '.format (OO00O00O00OOO0OO0 +1 ,OO0O000O0O0O000O0 .pool_num )#line:162
            print (OOOOOOOO0O0000O00 ,end ='')#line:163
    def score_pool (O0OOO000O0O00O00O ):#line:164
        O0OOO000O0O00O00O .aaa =0 #line:165
        Parallel (n_jobs =O0OOO000O0O00O00O .core_num ,require ='sharedmem')([delayed (O0OOO000O0O00O00O .score_pool_multi )(O0000O000O0O0O000 )for O0000O000O0O0O000 in range (O0OOO000O0O00O00O .pool_num )])#line:166
        if O0OOO000O0O00O00O .show_pool_func !=None :#line:167
            O0OO00O0O00O00O00 ='\rScoring first gen {}/{}        '.format (O0OOO000O0O00O00O .pool_num ,O0OOO000O0O00O00O .pool_num )#line:168
            print (O0OO00O0O00O00O00 )#line:169
    def score_pool_dc_multi (O0O0000O00OOO0O0O ,OOO0OO00O00000OO0 ):#line:180
        OOOOOO00OO00O00OO =[]#line:181
        for O0O00000000OO0O0O in range (O0O0000O00OOO0O0O .para_num ):#line:182
            OOOOOO00OO00O00OO .append (O0O0000O00OOO0O0O .para_range [O0O00000000OO0O0O ][O0O0000O00OOO0O0O .pool [OOO0OO00O00000OO0 ,O0O00000000OO0O0O ]])#line:183
        OOOOOO00OO00O00OO =np .array (OOOOOO00OO00O00OO )#line:184
        O0O0000O00OOO0O0O .pool_score [OOO0OO00O00000OO0 ]=O0O0000O00OOO0O0O .score_func (OOOOOO00OO00O00OO )#line:185
        O0O0000O00OOO0O0O .aaa +=1 #line:186
        if O0O0000O00OOO0O0O .show_pool_func !=None :#line:187
            O00O000O0O00O0OO0 ='\rScoring first gen {}/{}        '.format (OOO0OO00O00000OO0 +1 ,O0O0000O00OOO0O0O .pool_num )#line:188
            print (O00O000O0O00O0OO0 ,end ='')#line:189
    def score_pool_dc (O00O0O00O00000O00 ):#line:190
        O00O0O00O00000O00 .aaa =0 #line:191
        Parallel (n_jobs =O00O0O00O00000O00 .core_num ,require ='sharedmem')([delayed (O00O0O00O00000O00 .score_pool_dc_multi )(O0OO0000O00O00OOO )for O0OO0000O00O00OOO in range (O00O0O00O00000O00 .pool_num )])#line:192
        if O00O0O00O00000O00 .show_pool_func !=None :#line:193
            OOOO00O0OO000OO0O ='\rScoring first gen {}/{}        '.format (O00O0O00O00000O00 .pool_num ,O00O0O00O00000O00 .pool_num )#line:194
            print (OOOO00O0OO000OO0O )#line:195
    def score_pool_rc_multi (OO000O0OOO000O0O0 ,O00O000OOOO0000O0 ):#line:209
        OO00O0OO0O0000O00 =OO000O0OOO000O0O0 .pool [O00O000OOOO0000O0 ]*(OO000O0OOO000O0O0 .para_range [:,1 ]-OO000O0OOO000O0O0 .para_range [:,0 ])+OO000O0OOO000O0O0 .para_range [:,0 ]#line:210
        OO000O0OOO000O0O0 .pool_score [O00O000OOOO0000O0 ]=OO000O0OOO000O0O0 .score_func (OO00O0OO0O0000O00 )#line:211
        OO000O0OOO000O0O0 .aaa +=1 #line:212
        if OO000O0OOO000O0O0 .show_pool_func !=None :#line:213
            OO0OO0000OO0O0O0O ='\rScoring first gen {}/{}        '.format (O00O000OOOO0000O0 +1 ,OO000O0OOO000O0O0 .pool_num )#line:214
            print (OO0OO0000OO0O0O0O ,end ='')#line:215
    def score_pool_rc (O0OOOO0000OOOOOO0 ):#line:216
        O0OOOO0000OOOOOO0 .aaa =0 #line:217
        Parallel (n_jobs =O0OOOO0000OOOOOO0 .core_num ,require ='sharedmem')([delayed (O0OOOO0000OOOOOO0 .score_pool_rc_multi )(OO0O00OOOOO0OOO0O )for OO0O00OOOOO0OOO0O in range (O0OOOO0000OOOOOO0 .pool_num )])#line:218
        if O0OOOO0000OOOOOO0 .show_pool_func !=None :#line:219
            OOO00O0O0OO0OO0O0 ='\rScoring first gen {}/{}        '.format (O0OOOO0000OOOOOO0 .pool_num ,O0OOOO0000OOOOOO0 .pool_num )#line:220
            print (OOO00O0O0OO0OO0O0 )#line:221
    def save_best_mean (O0O000O0OO0O00OOO ):#line:255
        O0O000O0OO0O00OOO .best_index =np .argmin (np .abs (O0O000O0OO0O00OOO .aim -O0O000O0OO0O00OOO .pool_score ))#line:257
        O0O000O0OO0O00OOO .pool_best =deepcopy (O0O000O0OO0O00OOO .pool [O0O000O0OO0O00OOO .best_index ])#line:259
        O0O000O0OO0O00OOO .score_best =deepcopy (O0O000O0OO0O00OOO .pool_score [O0O000O0OO0O00OOO .best_index ])#line:260
        O0O000O0OO0O00OOO .score_mean =np .mean (O0O000O0OO0O00OOO .pool_score )#line:263
        O0O000O0OO0O00OOO .gap_mean =np .mean (np .abs (O0O000O0OO0O00OOO .aim -O0O000O0OO0O00OOO .pool_score ))#line:264
        O0O000O0OO0O00OOO .score_mean_save =deepcopy (O0O000O0OO0O00OOO .score_mean )#line:266
        O0O000O0OO0O00OOO .gap_mean_save =deepcopy (O0O000O0OO0O00OOO .gap_mean )#line:267
    def make_parent (OOO000O00OO000000 ,O0O000OO0OO0000OO ):#line:271
        OOO000O00OO000000 .pool_select =O0O000OO0OO0000OO #line:272
        OOO000O00OO000000 .parent =OOO000O00OO000000 .pool [OOO000O00OO000000 .pool_select ]#line:273
        OOO000O00OO000000 .parent_score =OOO000O00OO000000 .pool_score [OOO000O00OO000000 .pool_select ]#line:274
    def make_family (O0O00O0O0O0000O00 ):#line:278
        O0O00O0O0O0000O00 .family =np .vstack ((O0O00O0O0O0000O00 .child ,O0O00O0O0O0000O00 .parent ))#line:279
        O0O00O0O0O0000O00 .family_score =np .hstack ((O0O00O0O0O0000O00 .child_score ,O0O00O0O0O0000O00 .parent_score ))#line:280
    def JGG (O0000OO0O0OOOOO0O ):#line:284
        O0000OO0O0OOOOO0O .family_select =np .argpartition (np .abs (O0000OO0O0OOOOO0O .aim -O0000OO0O0OOOOO0O .family_score ),O0000OO0O0OOOOO0O .parent_num )[:O0000OO0O0OOOOO0O .parent_num ]#line:287
        O0000OO0O0OOOOO0O .pool [O0000OO0O0OOOOO0O .pool_select ]=O0000OO0O0OOOOO0O .family [O0000OO0O0OOOOO0O .family_select ]#line:289
        O0000OO0O0OOOOO0O .pool_score [O0000OO0O0OOOOO0O .pool_select ]=O0000OO0O0OOOOO0O .family_score [O0000OO0O0OOOOO0O .family_select ]#line:290
    def end_check (O0O00O0OOOO0OO0O0 ):#line:294
        O0O00O0OOOO0OO0O0 .best_index =np .argmin (np .abs (O0O00O0OOOO0OO0O0 .aim -O0O00O0OOOO0OO0O0 .pool_score ))#line:296
        O0O00O0OOOO0OO0O0 .score_best =deepcopy (O0O00O0OOOO0OO0O0 .pool_score [O0O00O0OOOO0OO0O0 .best_index ])#line:297
        O0O00O0OOOO0OO0O0 .gap_mean =np .mean (np .abs (O0O00O0OOOO0OO0O0 .aim -O0O00O0OOOO0OO0O0 .pool_score ))#line:299
        if O0O00O0OOOO0OO0O0 .score_best ==O0O00O0OOOO0OO0O0 .aim :#line:301
            return 10 #line:302
        if O0O00O0OOOO0OO0O0 .gap_mean >=O0O00O0OOOO0OO0O0 .gap_mean_save :#line:304
            return 1 #line:305
        return 0 #line:306
    def make_info (O0OOOOOOO000O0O0O ,OO00O000OO0O0O0OO ):#line:324
        O0O00O000000OO0O0 ={'gen':OO00O000OO0O0O0OO ,'best_index':O0OOOOOOO000O0O0O .best_index ,'best_score':round (O0OOOOOOO000O0O0O .score_best ,4 ),'mean_score':round (O0OOOOOOO000O0O0O .score_mean ,4 ),'mean_gap':round (O0OOOOOOO000O0O0O .gap_mean ,4 ),'time':round (time .time ()-O0OOOOOOO000O0O0O .start ,1 )}#line:329
        return O0O00O000000OO0O0 #line:330
    def show_pool (O00OOOOOOOOOOO00O ,O00O0OO00O0O0O0OO ):#line:334
        O00O0OOOOOO000O0O =O00OOOOOOOOOOO00O .make_info (O00O0OO00O0O0O0OO )#line:335
        O00OOOOOOOOOOO00O .show_pool_func (O00OOOOOOOOOOO00O .para_range [O00OOOOOOOOOOO00O .pool ],**O00O0OOOOOO000O0O )#line:336
    def show_pool_dc (OOOOOO00OOO00O000 ,OO0O0O00OO00OOO00 ):#line:337
        O00O0O0O00O00O0OO =OOOOOO00OOO00O000 .make_info (OO0O0O00OO00OOO00 )#line:338
        O00O00OO0OOO00OO0 =[]#line:339
        for O00OOOOOO0000OO00 in range (OOOOOO00OOO00O000 .pool_num ):#line:340
            O0000OO000OO0OOO0 =[]#line:341
            for O000O0O00OOOOOOOO in range (OOOOOO00OOO00O000 .para_num ):#line:342
                O0000OO000OO0OOO0 .append (OOOOOO00OOO00O000 .para_range [O000O0O00OOOOOOOO ][OOOOOO00OOO00O000 .pool [O00OOOOOO0000OO00 ,O000O0O00OOOOOOOO ]])#line:343
            O00O00OO0OOO00OO0 .append (O0000OO000OO0OOO0 )#line:344
        O00O00OO0OOO00OO0 =np .array (O00O00OO0OOO00OO0 )#line:345
        OOOOOO00OOO00O000 .show_pool_func (O00O00OO0OOO00OO0 ,**O00O0O0O00O00O0OO )#line:346
    def show_pool_rc (O0OOO0OO000OO0O0O ,OOOOOO0OOOOO0OO00 ):#line:347
        OO0OOOO0OOOO0OO00 =O0OOO0OO000OO0O0O .make_info (OOOOOO0OOOOO0OO00 )#line:348
        O00O000OO0OOOOOO0 =np .array (list (map (lambda O0O0OOO0000000000 :O0OOO0OO000OO0O0O .pool [O0O0OOO0000000000 ]*(O0OOO0OO000OO0O0O .para_range [:,1 ]-O0OOO0OO000OO0O0O .para_range [:,0 ])+O0OOO0OO000OO0O0O .para_range [:,0 ],range (O0OOO0OO000OO0O0O .pool_num ))))#line:351
        O0OOO0OO000OO0O0O .show_pool_func (O00O000OO0OOOOOO0 ,**OO0OOOO0OOOO0OO00 )#line:352
    def make_round (OO0OOOOOO00OO00O0 ):#line:356
        O0O0O000OOOOOOO00 =round (OO0OOOOOO00OO00O0 .score_best ,4 )#line:357
        OO00O0OO00000O00O =round (OO0OOOOOO00OO00O0 .score_mean ,4 )#line:358
        OOOOO00O000O00O0O =round (OO0OOOOOO00OO00O0 .gap_mean ,4 )#line:359
        O0O0O0O0O0O00O0OO =round (time .time ()-OO0OOOOOO00OO00O0 .start ,1 )#line:360
        return O0O0O000OOOOOOO00 ,OO00O0OO00000O00O ,OOOOO00O000O00O0O ,O0O0O0O0O0O00O0OO #line:361
    def show_pool_bar (O0O0OO0OO0OOOOOO0 ,OOO000O0O00OO0O0O ):#line:366
        OOOOOOO0OO0000OO0 =round (O0O0OO0OO0OOOOOO0 .score_best ,4 )#line:368
        O0OO00O000O0OO000 =min (abs (O0O0OO0OO0OOOOOO0 .aim -O0O0OO0OO0OOOOOO0 .init_score_range [0 ]),abs (O0O0OO0OO0OOOOOO0 .aim -O0O0OO0OO0OOOOOO0 .init_score_range [1 ]))#line:370
        O0O0O00OO00O0000O =abs (O0O0OO0OO0OOOOOO0 .aim -O0O0OO0OO0OOOOOO0 .score_best )#line:371
        O0OOOO00O00O0O000 =min (abs (O0O0OO0OO0OOOOOO0 .aim -O0O0OO0OO0OOOOOO0 .gap_mean ),O0OO00O000O0OO000 )#line:372
        if O0OO00O000O0OO000 ==0 :#line:374
            O0OO00O000O0OO000 =0.001 #line:375
        O0000OO00OO0O00O0 =int (O0O0O00OO00O0000O /O0OO00O000O0OO000 *40 )#line:376
        OO0O0O0000O0OOOOO =int ((O0OOOO00O00O0O000 -O0O0O00OO00O0000O )/O0OO00O000O0OO000 *40 )#line:377
        OO0OO0OO000OO0OO0 =40 -O0000OO00OO0O00O0 -OO0O0O0000O0OOOOO #line:378
        OOO0000000O00OOO0 ='\r|{}+{}<{}| gen={}, best_score={}'.format (' '*O0000OO00OO0O00O0 ,' '*OO0O0O0000O0OOOOO ,' '*OO0OO0OO000OO0OO0 ,OOO000O0O00OO0O0O ,OOOOOOO0OO0000OO0 )#line:380
        print (OOO0000000O00OOO0 ,end ='')#line:381
        if OOO000O0O00OO0O0O ==0 :#line:383
            time .sleep (0.2 )#line:384
    def show_pool_print (O0O00OO000OO000OO ,OO0O000O00OOO00OO ):#line:386
        O00O0000O00O00O00 ,OOOOO0OOO00O00O00 ,OOOO0O0OOO00000O0 ,O00OOOOO000000O0O =O0O00OO000OO000OO .make_round ()#line:387
        print ('gen={}, best_score={}, mean_score={}, mean_gap={}, time={}'.format (OO0O000O00OOO00OO ,O00O0000O00O00O00 ,OOOOO0OOO00O00O00 ,OOOO0O0OOO00000O0 ,O00OOOOO000000O0O ))#line:388
    def show_pool_plot (O00O000O0OO00OOO0 ,O000O00O0OOOOO00O ):#line:391
        OOOO0O0O0OO0O0OO0 ,O00000OO0O000O00O ,OOOO0O0OOO00O0000 ,OOO0O00OOOO00OO00 =O00O000O0OO00OOO0 .make_round ()#line:392
        plt .bar (range (len (O00O000O0OO00OOO0 .pool_score [:100 ])),O00O000O0OO00OOO0 .pool_score [:100 ])#line:394
        plt .ylim ([min (O00O000O0OO00OOO0 .aim ,O00O000O0OO00OOO0 .init_score_range [0 ]),max (O00O000O0OO00OOO0 .aim ,O00O000O0OO00OOO0 .init_score_range [1 ])])#line:395
        plt .title ('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format (O000O00O0OOOOO00O ,'\n',OOOO0O0O0OO0O0OO0 ,'\n',O00000OO0O000O00O ,'\n',OOOO0O0OOO00O0000 ,'\n',OOO0O00OOOO00OO00 ),loc ='left')#line:396
        plt .show ();plt .close ();print ()#line:397
    def show_pool_save (O000O0OOO0O00OOO0 ,OO00OO0OOOO0OO000 ):#line:400
        O000O0OOO0O00OOO0 .show_pool_bar (OO00OO0OOOO0OO000 )#line:402
        O0O0OOOOOOOOOO0OO ,O00OO00OO0OO0OOO0 ,O000OOO0OOO0O0OOO ,O00OOOO0O0000OO00 =O000O0OOO0O00OOO0 .make_round ()#line:404
        plt .bar (range (len (O000O0OOO0O00OOO0 .pool_score [:100 ])),O000O0OOO0O00OOO0 .pool_score [:100 ])#line:406
        plt .ylim ([min (O000O0OOO0O00OOO0 .aim ,O000O0OOO0O00OOO0 .init_score_range [0 ]),max (O000O0OOO0O00OOO0 .aim ,O000O0OOO0O00OOO0 .init_score_range [1 ])])#line:407
        plt .title ('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format (OO00OO0OOOO0OO000 ,'\n',O0O0OOOOOOOOOO0OO ,'\n',O00OO00OO0OO0OOO0 ,'\n',O000OOO0OOO0O0OOO ,'\n',O00OOOO0O0000OO00 ),loc ='left')#line:408
        plt .subplots_adjust (left =0.1 ,right =0.95 ,bottom =0.1 ,top =0.70 )#line:409
        plt .savefig (O000O0OOO0O00OOO0 .show_pool_func +'round_{}.png'.format (str (OO00OO0OOOO0OO000 ).zfill (4 )));plt .close ()#line:410
    def opt2 (OO0000O00OOO00O0O ,O0OO0O0OOO0O0OOOO ,O0O0O00OO0OOOOO00 ,O000OO000O0O00000 ,show_para_func =None ,seed =None ,step_max =float ('inf')):#line:416
        O0OO0O0OOO0O0OOOO ,O0O0O0O0OO0OO0OO0 =np .array (O0OO0O0OOO0O0OOOO ),O0O0O00OO0OOOOO00 (O0OO0O0OOO0O0OOOO )#line:418
        OOO000000OO000O00 ={}#line:419
        if seed !='pass':nr .seed (seed )#line:420
        O0OO0O0OO0OO0O00O =0 #line:421
        if show_para_func !=None :#line:423
            OOO000000OO000O00 .update ({'step_num':O0OO0O0OO0OO0O00O ,'score':round (O0O0O0O0OO0OO0OO0 ,3 )})#line:424
            show_para_func (O0OO0O0OOO0O0OOOO ,**OOO000000OO000O00 )#line:425
        while 1 :#line:427
            OOO0OOO0O0000OOOO =False #line:428
            if O0OO0O0OO0OO0O00O >=step_max :#line:429
                break #line:431
            OO0O000OO0O000000 =np .arange (0 ,len (O0OO0O0OOO0O0OOOO )-1 )#line:433
            nr .shuffle (OO0O000OO0O000000 )#line:434
            for O00O000OOO00OO00O in OO0O000OO0O000000 :#line:435
                if OOO0OOO0O0000OOOO ==True :break #line:437
                O000000O0O0O0O0O0 =np .arange (O00O000OOO00OO00O +1 ,len (O0OO0O0OOO0O0OOOO ))#line:439
                nr .shuffle (O000000O0O0O0O0O0 )#line:440
                for O0000000000OO0OO0 in O000000O0O0O0O0O0 :#line:441
                    if OOO0OOO0O0000OOOO ==True :break #line:443
                    O0OOOOOOO0000O0O0 =np .hstack ((O0OO0O0OOO0O0OOOO [:O00O000OOO00OO00O ],O0OO0O0OOO0O0OOOO [O00O000OOO00OO00O :O0000000000OO0OO0 +1 ][::-1 ],O0OO0O0OOO0O0OOOO [O0000000000OO0OO0 +1 :]))#line:446
                    O0O0OOO0O00OO0O00 =O0O0O00OO0OOOOO00 (O0OOOOOOO0000O0O0 )#line:447
                    if np .abs (O000OO000O0O00000 -O0O0OOO0O00OO0O00 )<np .abs (O000OO000O0O00000 -O0O0O0O0OO0OO0OO0 ):#line:450
                        O0OO0O0OOO0O0OOOO ,O0O0O0O0OO0OO0OO0 =O0OOOOOOO0000O0O0 ,O0O0OOO0O00OO0O00 #line:451
                        O0OO0O0OO0OO0O00O +=1 #line:452
                        if show_para_func !=None :#line:453
                            OOO000000OO000O00 .update ({'step_num':O0OO0O0OO0OO0O00O ,'score':round (O0O0O0O0OO0OO0OO0 ,3 )})#line:454
                            show_para_func (O0OO0O0OOO0O0OOOO ,**OOO000000OO000O00 )#line:455
                        OOO0OOO0O0000OOOO =True #line:456
            if OOO0OOO0O0000OOOO ==False :#line:457
                break #line:459
        return O0OO0O0OOO0O0OOOO ,O0O0O0O0OO0OO0OO0 #line:460
    def opt2_tspGA (OOO0000000OO0O00O ,OO0000000O00O00O0 ,O00O0OOOOO0OOOO00 ,step_max =float ('inf')):#line:464
        OO0000000O00O00O0 ,O00O0OOOOO0OOOO00 =OO0000000O00O00O0 ,O00O0OOOOO0OOOO00 #line:466
        OOO000O00OO00O000 =0 #line:467
        while 1 :#line:469
            O000O00O0O0O0O0OO =False #line:470
            if OOO000O00OO00O000 >=step_max :#line:471
                break #line:472
            O00O00O000OOOOO0O =np .arange (0 ,OOO0000000OO0O00O .para_num -1 )#line:474
            nr .shuffle (O00O00O000OOOOO0O )#line:476
            for OO00OOO0O000OOOOO in O00O00O000OOOOO0O :#line:477
                if O000O00O0O0O0O0OO ==True :break #line:479
                OO0O000OOO0OOO0OO =np .arange (OO00OOO0O000OOOOO +1 ,OOO0000000OO0O00O .para_num )#line:481
                nr .shuffle (OO0O000OOO0OOO0OO )#line:482
                for O0000O0O000000OO0 in OO0O000OOO0OOO0OO :#line:483
                    if O000O00O0O0O0O0OO ==True :break #line:485
                    OOO00O000O0O0OOOO =np .hstack ((OO0000000O00O00O0 [:OO00OOO0O000OOOOO ],OO0000000O00O00O0 [OO00OOO0O000OOOOO :O0000O0O000000OO0 +1 ][::-1 ],OO0000000O00O00O0 [O0000O0O000000OO0 +1 :]))#line:488
                    OOO00000OO00O0O00 =OOO0000000OO0O00O .score_func (OOO0000000OO0O00O .para_range [OOO00O000O0O0OOOO ])#line:489
                    if np .abs (OOO0000000OO0O00O .aim -OOO00000OO00O0O00 )<np .abs (OOO0000000OO0O00O .aim -O00O0OOOOO0OOOO00 ):#line:492
                        OO0000000O00O00O0 ,O00O0OOOOO0OOOO00 =OOO00O000O0O0OOOO ,OOO00000OO00O0O00 #line:493
                        OOO000O00OO00O000 +=1 #line:494
                        O000O00O0O0O0O0OO =True #line:495
            if O000O00O0O0O0O0OO ==False :#line:496
                break #line:498
        return OO0000000O00O00O0 ,O00O0OOOOO0OOOO00 #line:499
    def tspGA_multi (O000O000OO0OO000O ,O0OO000000000O0OO ):#line:528
        OO00O0000O0O0O000 =O000O000OO0OO000O .pool [O0OO000000000O0OO ]#line:530
        O0O0000000O0OOO0O =O000O000OO0OO000O .pool_score [O0OO000000000O0OO ]#line:531
        OO0O0O000O00000O0 =np .ones ((O000O000OO0OO000O .child_num ,O000O000OO0OO000O .para_num ),dtype =int )#line:532
        O0O0O0O000O00O00O =np .zeros (O000O000OO0OO000O .child_num )#line:533
        O0OO0OOOOOO0OOO0O =np .hstack ((OO00O0000O0O0O000 [:,-2 :].reshape (O000O000OO0OO000O .parent_num ,2 ),OO00O0000O0O0O000 ,OO00O0000O0O0O000 [:,:2 ].reshape (O000O000OO0OO000O .parent_num ,2 )))#line:538
        for OO000OOOOOO00O0O0 in range (O000O000OO0OO000O .child_num ):#line:541
            OOOO00O00O0000OOO =OO00O0000O0O0O000 [nr .randint (O000O000OO0OO000O .parent_num ),0 ]#line:543
            if nr .rand ()<(1.0 /O000O000OO0OO000O .para_num ):#line:544
                OOOO00O00O0000OOO =nr .choice (O000O000OO0OO000O .para_index )#line:545
            OO0O0O000O00000O0 [OO000OOOOOO00O0O0 ,0 ]=OOOO00O00O0000OOO #line:546
            for O000O00OO00000OOO in range (1 ,O000O000OO0OO000O .para_num ):#line:548
                O0OO0OOOO0O000OOO =np .zeros ((O000O000OO0OO000O .parent_num ,O000O000OO0OO000O .para_num +4 ),dtype =bool )#line:550
                O00OO00OO0000OO0O =np .zeros ((O000O000OO0OO000O .parent_num ,O000O000OO0OO000O .para_num +4 ),dtype =bool )#line:551
                O0OO0OOOO0O000OOO [:,1 :-3 ]+=(O000O000OO0OO000O .parent ==OOOO00O00O0000OOO )#line:553
                O0OO0OOOO0O000OOO [:,3 :-1 ]+=(O000O000OO0OO000O .parent ==OOOO00O00O0000OOO )#line:554
                O00OO00OO0000OO0O [:,0 :-4 ]+=(O000O000OO0OO000O .parent ==OOOO00O00O0000OOO )#line:555
                O00OO00OO0000OO0O [:,4 :]+=(O000O000OO0OO000O .parent ==OOOO00O00O0000OOO )#line:556
                O0OOO00O0O00O0OOO =np .ones (O000O000OO0OO000O .para_num )*(1.0 /O000O000OO0OO000O .para_num )#line:559
                for OO000OO0OO0OO0OO0 in O0OO0OOOOOO0OOO0O [O0OO0OOOO0O000OOO ]:#line:560
                    O0OOO00O0O00O0OOO [np .where (O000O000OO0OO000O .para_index ==OO000OO0OO0OO0OO0 )[0 ]]+=1.0 /O000O000OO0OO000O .parent_num #line:561
                for OO000OO0OO0OO0OO0 in O0OO0OOOOOO0OOO0O [O00OO00OO0000OO0O ]:#line:562
                    O0OOO00O0O00O0OOO [np .where (O000O000OO0OO000O .para_index ==OO000OO0OO0OO0OO0 )[0 ]]+=0.1 /O000O000OO0OO000O .parent_num #line:563
                for OO000OO0OO0OO0OO0 in OO0O0O000O00000O0 [OO000OOOOOO00O0O0 ,0 :O000O00OO00000OOO ]:#line:566
                    O0OOO00O0O00O0OOO [np .where (O000O000OO0OO000O .para_index ==OO000OO0OO0OO0OO0 )[0 ]]=0.0 #line:567
                O0OOO00O0O00O0OOO *=1.0 /np .sum (O0OOO00O0O00O0OOO )#line:570
                OOOO00O00O0000OOO =nr .choice (O000O000OO0OO000O .para_index ,p =O0OOO00O0O00O0OOO )#line:571
                OO0O0O000O00000O0 [OO000OOOOOO00O0O0 ,O000O00OO00000OOO ]=OOOO00O00O0000OOO #line:573
        for OO000OOOOOO00O0O0 in range (O000O000OO0OO000O .child_num ):#line:577
            O00OO00OOO0O0OOO0 =O000O000OO0OO000O .para_range [OO0O0O000O00000O0 [OO000OOOOOO00O0O0 ]]#line:578
            O0O0O0O000O00O00O [OO000OOOOOO00O0O0 ]=O000O000OO0OO000O .score_func (O00OO00OOO0O0OOO0 )#line:579
        O00OOOO0O0OO0OO0O =np .vstack ((OO0O0O000O00000O0 ,OO00O0000O0O0O000 ))#line:581
        OO00OOOO000OOOOO0 =np .hstack ((O0O0O0O000O00O00O ,O0O0000000O0OOO0O ))#line:582
        for OO000OOOOOO00O0O0 in range (O000O000OO0OO000O .family_num ):#line:584
            O00OOOO0O0OO0OO0O [OO000OOOOOO00O0O0 ],OO00OOOO000OOOOO0 [OO000OOOOOO00O0O0 ]=O000O000OO0OO000O .opt2_tspGA (O00OOOO0O0OO0OO0O [OO000OOOOOO00O0O0 ],OO00OOOO000OOOOO0 [OO000OOOOOO00O0O0 ],step_max =O000O000OO0OO000O .opt2_num )#line:585
        OO00O00O0OOO000OO =np .argpartition (np .abs (O000O000OO0OO000O .aim -OO00OOOO000OOOOO0 ),O000O000OO0OO000O .parent_num )[:O000O000OO0OO000O .parent_num ]#line:587
        O000O000OO0OO000O .pool [O0OO000000000O0OO ]=O00OOOO0O0OO0OO0O [OO00O00O0OOO000OO ]#line:588
        O000O000OO0OO000O .pool_score [O0OO000000000O0OO ]=OO00OOOO000OOOOO0 [OO00O00O0OOO000OO ]#line:589
    def tspGA (OO00OO000O0000O0O ,O0O00OOO0OOOO000O ,OO00O0O0O00000000 ,OOOO0OO0O00O0O0OO ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:591
        O0O00OOO0OOOO000O =np .array (O0O00OOO0OOOO000O )#line:596
        OO00OO000O0000O0O .setting_1 (O0O00OOO0OOOO000O ,OO00O0O0O00000000 ,OOOO0OO0O00O0O0OO ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:599
        OO00OO000O0000O0O .setting_2 (OO00OO000O0000O0O .para_num *10 ,2 ,4 )#line:600
        OO00OO000O0000O0O .setting_3 (int )#line:601
        OO00OO000O0000O0O .print_info ()#line:602
        OO00OO000O0000O0O .para_index =np .arange (OO00OO000O0000O0O .para_num )#line:605
        OO00OO000O0000O0O .opt2_num =1 #line:606
        for O0OO0O0O0O0O000O0 in range (OO00OO000O0000O0O .pool_num ):#line:609
            OO00OO000O0000O0O .pool [O0OO0O0O0O0O000O0 ]=deepcopy (OO00OO000O0000O0O .para_index )#line:610
            nr .shuffle (OO00OO000O0000O0O .pool [O0OO0O0O0O0O000O0 ])#line:611
        OO00OO000O0000O0O .score_pool ()#line:614
        for O0OO0O0O0O0O000O0 in range (OO00OO000O0000O0O .pool_num ):#line:617
            OO00OO000O0000O0O .pool [O0OO0O0O0O0O000O0 ],OO00OO000O0000O0O .pool_score [O0OO0O0O0O0O000O0 ]=OO00OO000O0000O0O .opt2_tspGA (OO00OO000O0000O0O .pool [O0OO0O0O0O0O000O0 ],OO00OO000O0000O0O .pool_score [O0OO0O0O0O0O000O0 ],step_max =OO00OO000O0000O0O .opt2_num )#line:618
            if OO00OO000O0000O0O .show_pool_func !=None :#line:619
                O0O00OO00O000O0O0 ='\rMini 2-opting first gen {}/{}        '.format (O0OO0O0O0O0O000O0 +1 ,OO00OO000O0000O0O .pool_num )#line:620
                print (O0O00OO00O000O0O0 ,end ='')#line:621
        if OO00OO000O0000O0O .show_pool_func !=None :print ()#line:622
        OO00OO000O0000O0O .save_best_mean ()#line:625
        OO00OO000O0000O0O .init_score_range =(np .min (OO00OO000O0000O0O .pool_score ),np .max (OO00OO000O0000O0O .pool_score ))#line:627
        OO00OO000O0000O0O .init_gap_mean =deepcopy (OO00OO000O0000O0O .gap_mean )#line:628
        if OO00OO000O0000O0O .show_pool_func ==None :pass #line:631
        elif OO00OO000O0000O0O .show_pool_func =='bar':OO00OO000O0000O0O .show_pool_bar (0 )#line:632
        elif OO00OO000O0000O0O .show_pool_func =='print':OO00OO000O0000O0O .show_pool_print (0 )#line:633
        elif OO00OO000O0000O0O .show_pool_func =='plot':OO00OO000O0000O0O .show_pool_plot (0 )#line:634
        elif callable (OO00OO000O0000O0O .show_pool_func ):OO00OO000O0000O0O .show_pool (0 )#line:635
        elif type (show_pool_func )==str :#line:636
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:637
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:638
                OO00OO000O0000O0O .show_pool_save (0 )#line:639
        O0OO00OOO0000OOO0 =0 #line:642
        for OOOOO0000000000OO in range (1 ,OO00OO000O0000O0O .max_n +1 ):#line:643
            OOOOOOO00O0OOO00O =np .arange (OO00OO000O0000O0O .pool_num )#line:648
            nr .shuffle (OOOOOOO00O0OOO00O )#line:649
            OOOOOOO00O0OOO00O =OOOOOOO00O0OOO00O .reshape ((OO00OO000O0000O0O .pool_num //OO00OO000O0000O0O .parent_num ),OO00OO000O0000O0O .parent_num )#line:650
            Parallel (n_jobs =OO00OO000O0000O0O .core_num ,require ='sharedmem')([delayed (OO00OO000O0000O0O .tspGA_multi )(OO00O00O0O0OO0O0O )for OO00O00O0O0OO0O0O in OOOOOOO00O0OOO00O ])#line:653
            O0OO00OOO0000OOO0 +=OO00OO000O0000O0O .end_check ()#line:710
            OO00OO000O0000O0O .save_best_mean ()#line:713
            if OO00OO000O0000O0O .show_pool_func ==None :pass #line:716
            elif OO00OO000O0000O0O .show_pool_func =='bar':OO00OO000O0000O0O .show_pool_bar (OOOOO0000000000OO *OO00OO000O0000O0O .pool_num )#line:717
            elif OO00OO000O0000O0O .show_pool_func =='print':OO00OO000O0000O0O .show_pool_print (OOOOO0000000000OO *OO00OO000O0000O0O .pool_num )#line:718
            elif OO00OO000O0000O0O .show_pool_func =='plot':OO00OO000O0000O0O .show_pool_plot (OOOOO0000000000OO *OO00OO000O0000O0O .pool_num )#line:719
            elif callable (OO00OO000O0000O0O .show_pool_func ):OO00OO000O0000O0O .show_pool (OOOOO0000000000OO *OO00OO000O0000O0O .pool_num )#line:720
            elif type (show_pool_func )==str :#line:721
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:722
                    OO00OO000O0000O0O .show_pool_save (OOOOO0000000000OO )#line:723
            if O0OO00OOO0000OOO0 >=1 :#line:726
                break #line:727
        OOOO00000O00O0000 =OO00OO000O0000O0O .para_range [OO00OO000O0000O0O .pool_best ]#line:730
        if OO00OO000O0000O0O .show_pool_func =='bar':print ()#line:733
        elif type (show_pool_func )==str :#line:734
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:735
                print ()#line:736
        if OO00OO000O0000O0O .show_pool_func !=None :#line:739
            print ('__________________ results _________________')#line:740
            print ('para : {}'.format (OOOO00000O00O0000 ))#line:741
            print ('score : {}'.format (OO00OO000O0000O0O .score_best ))#line:742
            print ('____________________ end ___________________')#line:743
        return OOOO00000O00O0000 ,OO00OO000O0000O0O .score_best #line:745
    def dcGA_multi (OOO0000OO0000O00O ,OOOO00O0O0O00O000 ):#line:773
        O0O0O00O0O0OO0O0O =OOO0000OO0000O00O .pool [OOOO00O0O0O00O000 ]#line:775
        OO000O0OOO0O00OO0 =OOO0000OO0000O00O .pool_score [OOOO00O0O0O00O000 ]#line:776
        O0OO00000OO00000O =np .zeros ((OOO0000OO0000O00O .child_num ,OOO0000OO0000O00O .para_num ),dtype =int )#line:777
        OOO00OO000OOOOO0O =np .zeros (OOO0000OO0000O00O .child_num )#line:778
        if OOO0000OO0000O00O .para_num >=3 :#line:781
            OO0OOO0OOO0O0O0OO =nr .choice (range (1 ,OOO0000OO0000O00O .para_num ),2 ,replace =False )#line:785
            if OO0OOO0OOO0O0O0OO [0 ]>OO0OOO0OOO0O0O0OO [1 ]:#line:786
                OO0OOO0OOO0O0O0OO [0 ],OO0OOO0OOO0O0O0OO [1 ]=OO0OOO0OOO0O0O0OO [1 ],OO0OOO0OOO0O0O0OO [0 ]#line:787
            for OO00OO0O00000OO00 in range (len (OOO0000OO0000O00O .choice )):#line:789
                O0OO00000OO00000O [OO00OO0O00000OO00 ]=np .hstack ((O0O0O00O0O0OO0O0O [OOO0000OO0000O00O .choice [OO00OO0O00000OO00 ,0 ],:OO0OOO0OOO0O0O0OO [0 ]],O0O0O00O0O0OO0O0O [OOO0000OO0000O00O .choice [OO00OO0O00000OO00 ,1 ],OO0OOO0OOO0O0O0OO [0 ]:OO0OOO0OOO0O0O0OO [1 ]],O0O0O00O0O0OO0O0O [OOO0000OO0000O00O .choice [OO00OO0O00000OO00 ,2 ],OO0OOO0OOO0O0O0OO [1 ]:]))#line:792
            for OO00OO0O00000OO00 in [2 ,3 ]:#line:797
                OOO0000O00O00OOO0 =nr .randint (0 ,2 ,OOO0000OO0000O00O .para_num )#line:798
                O0OO00000OO00000O [OO00OO0O00000OO00 ][OOO0000O00O00OOO0 ==0 ]=O0O0O00O0O0OO0O0O [0 ][OOO0000O00O00OOO0 ==0 ]#line:799
                O0OO00000OO00000O [OO00OO0O00000OO00 ][OOO0000O00O00OOO0 ==1 ]=O0O0O00O0O0OO0O0O [1 ][OOO0000O00O00OOO0 ==1 ]#line:800
            for O000O00O00O00O0OO in O0OO00000OO00000O :#line:804
                for O0O0OOO00OO0OOOO0 in range (OOO0000OO0000O00O .para_num ):#line:805
                    if nr .rand ()<(1.0 /OOO0000OO0000O00O .para_num ):#line:806
                        O000O00O00O00O0OO [O0O0OOO00OO0OOOO0 ]=nr .choice (OOO0000OO0000O00O .para_index [O0O0OOO00OO0OOOO0 ])#line:807
        elif OOO0000OO0000O00O .para_num ==2 :#line:811
            O0OO00000OO00000O [:2 ]=np .array ([[O0O0O00O0O0OO0O0O [0 ,0 ],O0O0O00O0O0OO0O0O [1 ,1 ]],[O0O0O00O0O0OO0O0O [0 ,1 ],O0O0O00O0O0OO0O0O [1 ,0 ]]])#line:813
            for OO00OO0O00000OO00 in range (2 ,OOO0000OO0000O00O .child_num ):#line:815
                for O0O0OOO00OO0OOOO0 in range (2 ):#line:816
                    O0OO00000OO00000O [OO00OO0O00000OO00 ,O0O0OOO00OO0OOOO0 ]=nr .choice (OOO0000OO0000O00O .para_index [O0O0OOO00OO0OOOO0 ])#line:817
        elif OOO0000OO0000O00O .para_num ==1 :#line:819
            for OO00OO0O00000OO00 in range (OOO0000OO0000O00O .child_num ):#line:821
                O0OO00000OO00000O [OO00OO0O00000OO00 ]=nr .choice (OOO0000OO0000O00O .para_index [0 ])#line:822
        for OO00OO0O00000OO00 in range (OOO0000OO0000O00O .child_num ):#line:826
            O00OO00000OOO0000 =[]#line:827
            for O0O0OOO00OO0OOOO0 in range (OOO0000OO0000O00O .para_num ):#line:828
                O00OO00000OOO0000 .append (OOO0000OO0000O00O .para_range [O0O0OOO00OO0OOOO0 ][O0OO00000OO00000O [OO00OO0O00000OO00 ,O0O0OOO00OO0OOOO0 ]])#line:829
            O00OO00000OOO0000 =np .array (O00OO00000OOO0000 )#line:830
            OOO00OO000OOOOO0O [OO00OO0O00000OO00 ]=OOO0000OO0000O00O .score_func (O00OO00000OOO0000 )#line:831
        OO000000O00OO000O =np .vstack ((O0OO00000OO00000O ,O0O0O00O0O0OO0O0O ))#line:833
        OO0OOOOO00OOOO0O0 =np .hstack ((OOO00OO000OOOOO0O ,OO000O0OOO0O00OO0 ))#line:834
        OO0O0O00OOOOOO00O =np .argpartition (np .abs (OOO0000OO0000O00O .aim -OO0OOOOO00OOOO0O0 ),OOO0000OO0000O00O .parent_num )[:OOO0000OO0000O00O .parent_num ]#line:836
        OOO0000OO0000O00O .pool [OOOO00O0O0O00O000 ]=OO000000O00OO000O [OO0O0O00OOOOOO00O ]#line:837
        OOO0000OO0000O00O .pool_score [OOOO00O0O0O00O000 ]=OO0OOOOO00OOOO0O0 [OO0O0O00OOOOOO00O ]#line:838
    def dcGA (OO00OO000OO0O000O ,O000000000000000O ,O00OO00000O000OOO ,O0OO00OOOOOO0OOO0 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:841
        if type (O000000000000000O )==list :#line:846
            if isinstance (O000000000000000O [0 ],list )==False :#line:847
                O000000000000000O =[O000000000000000O ]#line:848
        if type (O000000000000000O )==np .ndarray :#line:849
            if O000000000000000O .ndim ==1 :#line:850
                O000000000000000O =O000000000000000O .reshape (1 ,len (O000000000000000O ))#line:851
        OO00OO000OO0O000O .setting_1 (O000000000000000O ,O00OO00000O000OOO ,O0OO00OOOOOO0OOO0 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:854
        OO00OO000OO0O000O .setting_2 (OO00OO000OO0O000O .para_num *10 ,2 ,4 )#line:855
        OO00OO000OO0O000O .setting_3 (int )#line:856
        OO00OO000OO0O000O .print_info ()#line:857
        OO00OO000OO0O000O .para_index =[]#line:860
        for OO0O0O0O00000O0O0 in range (OO00OO000OO0O000O .para_num ):#line:861
            OO00OO000OO0O000O .para_index .append (np .arange (len (OO00OO000OO0O000O .para_range [OO0O0O0O00000O0O0 ])))#line:862
        OO00OO000OO0O000O .choice =np .array ([[0 ,1 ,0 ],[1 ,0 ,1 ]],dtype =int )#line:863
        for OO0O0O0O00000O0O0 in range (OO00OO000OO0O000O .pool_num ):#line:866
            for O0OO0O00OOOOOO0O0 in range (OO00OO000OO0O000O .para_num ):#line:867
                OO00OO000OO0O000O .pool [OO0O0O0O00000O0O0 ,O0OO0O00OOOOOO0O0 ]=nr .choice (OO00OO000OO0O000O .para_index [O0OO0O00OOOOOO0O0 ])#line:868
        OO00OO000OO0O000O .score_pool_dc ()#line:871
        OO00OO000OO0O000O .save_best_mean ()#line:872
        OO00OO000OO0O000O .init_score_range =(np .min (OO00OO000OO0O000O .pool_score ),np .max (OO00OO000OO0O000O .pool_score ))#line:874
        OO00OO000OO0O000O .init_gap_mean =deepcopy (OO00OO000OO0O000O .gap_mean )#line:875
        if OO00OO000OO0O000O .show_pool_func ==None :pass #line:878
        elif OO00OO000OO0O000O .show_pool_func =='bar':OO00OO000OO0O000O .show_pool_bar (0 )#line:879
        elif OO00OO000OO0O000O .show_pool_func =='print':OO00OO000OO0O000O .show_pool_print (0 )#line:880
        elif OO00OO000OO0O000O .show_pool_func =='plot':OO00OO000OO0O000O .show_pool_plot (0 )#line:881
        elif callable (OO00OO000OO0O000O .show_pool_func ):OO00OO000OO0O000O .show_pool_dc (0 )#line:882
        elif type (show_pool_func )==str :#line:883
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:884
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:885
                OO00OO000OO0O000O .show_pool_save (0 )#line:886
        O0OO0O0OO00O00O0O =0 #line:889
        for OOO0O0OO0O0000OO0 in range (1 ,OO00OO000OO0O000O .max_n +1 ):#line:890
            O00O0OOOO0OO0OO0O =np .arange (OO00OO000OO0O000O .pool_num )#line:893
            nr .shuffle (O00O0OOOO0OO0OO0O )#line:894
            O00O0OOOO0OO0OO0O =O00O0OOOO0OO0OO0O .reshape ((OO00OO000OO0O000O .pool_num //OO00OO000OO0O000O .parent_num ),OO00OO000OO0O000O .parent_num )#line:895
            Parallel (n_jobs =OO00OO000OO0O000O .core_num ,require ='sharedmem')([delayed (OO00OO000OO0O000O .dcGA_multi )(O0000O0O000OOOO0O )for O0000O0O000OOOO0O in O00O0OOOO0OO0OO0O ])#line:898
            O0OO0O0OO00O00O0O +=OO00OO000OO0O000O .end_check ()#line:954
            OO00OO000OO0O000O .save_best_mean ()#line:957
            if OO00OO000OO0O000O .show_pool_func ==None :pass #line:960
            elif OO00OO000OO0O000O .show_pool_func =='bar':OO00OO000OO0O000O .show_pool_bar (OOO0O0OO0O0000OO0 *OO00OO000OO0O000O .pool_num )#line:961
            elif OO00OO000OO0O000O .show_pool_func =='print':OO00OO000OO0O000O .show_pool_print (OOO0O0OO0O0000OO0 *OO00OO000OO0O000O .pool_num )#line:962
            elif OO00OO000OO0O000O .show_pool_func =='plot':OO00OO000OO0O000O .show_pool_plot (OOO0O0OO0O0000OO0 *OO00OO000OO0O000O .pool_num )#line:963
            elif callable (OO00OO000OO0O000O .show_pool_func ):OO00OO000OO0O000O .show_pool_dc (OOO0O0OO0O0000OO0 *OO00OO000OO0O000O .pool_num )#line:964
            elif type (show_pool_func )==str :#line:965
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:966
                    OO00OO000OO0O000O .show_pool_save (OOO0O0OO0O0000OO0 )#line:967
            if O0OO0O0OO00O00O0O >=1 :#line:970
                break #line:971
        O0O0O0O00O0000000 =[]#line:974
        for O0OO0O00OOOOOO0O0 in range (OO00OO000OO0O000O .para_num ):#line:975
            O0O0O0O00O0000000 .append (OO00OO000OO0O000O .para_range [O0OO0O00OOOOOO0O0 ][OO00OO000OO0O000O .pool [OO00OO000OO0O000O .best_index ,O0OO0O00OOOOOO0O0 ]])#line:976
        O0O0O0O00O0000000 =np .array (O0O0O0O00O0000000 )#line:977
        if OO00OO000OO0O000O .show_pool_func =='bar':print ()#line:980
        elif type (show_pool_func )==str :#line:981
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:982
                print ()#line:983
        if OO00OO000OO0O000O .show_pool_func !=None :#line:986
            print ('__________________ results _________________')#line:987
            print ('para : {}'.format (O0O0O0O00O0000000 ))#line:988
            print ('score : {}'.format (OO00OO000OO0O000O .score_best ))#line:989
            print ('____________________ end ___________________')#line:990
        return O0O0O0O00O0000000 ,OO00OO000OO0O000O .score_best #line:992
    def setGA_multi (OOOOO000O0O00000O ,O000OOO0O00OOO0OO ):#line:1022
        O0OO00000O000OOO0 =OOOOO000O0O00000O .pool [O000OOO0O00OOO0OO ]#line:1024
        OO000O0O0OO00O0OO =OOOOO000O0O00000O .pool_score [O000OOO0O00OOO0OO ]#line:1025
        OO0O00OOOOO0O00OO =np .zeros ((OOOOO000O0O00000O .child_num ,OOOOO000O0O00000O .para_num ),dtype =int )#line:1026
        O000OO0000O0O0O00 =np .zeros (OOOOO000O0O00000O .child_num )#line:1027
        OOO0OOOOOOOOO0OOO =set (O0OO00000O000OOO0 [0 ])&set (O0OO00000O000OOO0 [1 ])#line:1032
        OO00O00O00OOO000O =set (OOOOO000O0O00000O .para_index )-OOO0OOOOOOOOO0OOO #line:1034
        for O000O0O0000OOOOOO in range (len (OO0O00OOOOO0O00OO )):#line:1036
            O0000O0OO00O0OO0O =nr .choice (np .array (list (OO00O00O00OOO000O )),OOOOO000O0O00000O .set_num -len (OOO0OOOOOOOOO0OOO ),replace =False )#line:1037
            OO0O00OOOOO0O00OO [O000O0O0000OOOOOO ]=np .hstack ((np .array (list (OOO0OOOOOOOOO0OOO )),O0000O0OO00O0OO0O ))#line:1039
        for O0O0O0OOO0O00OOOO in OO0O00OOOOO0O00OO [2 :]:#line:1046
            for O0OOOO0OO0O00OO0O in range (OOOOO000O0O00000O .set_num ):#line:1047
                if nr .rand ()<(1.0 /OOOOO000O0O00000O .set_num ):#line:1048
                    OOOOO00OOOOO00000 =nr .choice (OOOOO000O0O00000O .para_index )#line:1049
                    if OOOOO00OOOOO00000 not in O0O0O0OOO0O00OOOO :#line:1050
                        O0O0O0OOO0O00OOOO [O0OOOO0OO0O00OO0O ]=OOOOO00OOOOO00000 #line:1051
        for O000O0O0000OOOOOO in range (OOOOO000O0O00000O .child_num ):#line:1056
            O0O00OOOOO00O0000 =OOOOO000O0O00000O .para_range [OO0O00OOOOO0O00OO [O000O0O0000OOOOOO ]]#line:1057
            O000OO0000O0O0O00 [O000O0O0000OOOOOO ]=OOOOO000O0O00000O .score_func (O0O00OOOOO00O0000 )#line:1058
        OO0OO00O00OOOOOO0 =np .vstack ((OO0O00OOOOO0O00OO ,O0OO00000O000OOO0 ))#line:1060
        OO00O00OO0OOOOO0O =np .hstack ((O000OO0000O0O0O00 ,OO000O0O0OO00O0OO ))#line:1061
        O00O00O00OO0O00O0 =np .argpartition (np .abs (OOOOO000O0O00000O .aim -OO00O00OO0OOOOO0O ),OOOOO000O0O00000O .parent_num )[:OOOOO000O0O00000O .parent_num ]#line:1063
        OOOOO000O0O00000O .pool [O000OOO0O00OOO0OO ]=OO0OO00O00OOOOOO0 [O00O00O00OO0O00O0 ]#line:1064
        OOOOO000O0O00000O .pool_score [O000OOO0O00OOO0OO ]=OO00O00OO0OOOOO0O [O00O00O00OO0O00O0 ]#line:1065
    def setGA (O0OO000OO0O000OOO ,OO00O00OOOO0O0000 ,O000OOO00000OO000 ,O0O0O00O000O0O00O ,O0OO0OOO0OO0O0O0O ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1067
        OO00O00OOOO0O0000 =np .array (OO00O00OOOO0O0000 )#line:1072
        O0OO000OO0O000OOO .setting_1 (OO00O00OOOO0O0000 ,O0O0O00O000O0O00O ,O0OO0OOO0OO0O0O0O ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1075
        O0OO000OO0O000OOO .set_num =O000OOO00000OO000 #line:1076
        O0OO000OO0O000OOO .para_num =O0OO000OO0O000OOO .set_num #line:1077
        O0OO000OO0O000OOO .setting_2 (O0OO000OO0O000OOO .para_num *10 ,2 ,4 )#line:1078
        O0OO000OO0O000OOO .setting_3 (int )#line:1079
        O0OO000OO0O000OOO .print_info ()#line:1080
        O0OO000OO0O000OOO .para_index =np .arange (len (O0OO000OO0O000OOO .para_range ))#line:1083
        for O00OOOO00OO0O0OOO in range (O0OO000OO0O000OOO .pool_num ):#line:1086
            O0OO000OO0O000OOO .pool [O00OOOO00OO0O0OOO ]=nr .choice (O0OO000OO0O000OOO .para_index ,O0OO000OO0O000OOO .set_num ,replace =False )#line:1087
        O0OO000OO0O000OOO .score_pool ()#line:1091
        O0OO000OO0O000OOO .save_best_mean ()#line:1092
        O0OO000OO0O000OOO .init_score_range =(np .min (O0OO000OO0O000OOO .pool_score ),np .max (O0OO000OO0O000OOO .pool_score ))#line:1094
        O0OO000OO0O000OOO .init_gap_mean =deepcopy (O0OO000OO0O000OOO .gap_mean )#line:1095
        if O0OO000OO0O000OOO .show_pool_func ==None :pass #line:1098
        elif O0OO000OO0O000OOO .show_pool_func =='bar':O0OO000OO0O000OOO .show_pool_bar (0 )#line:1099
        elif O0OO000OO0O000OOO .show_pool_func =='print':O0OO000OO0O000OOO .show_pool_print (0 )#line:1100
        elif O0OO000OO0O000OOO .show_pool_func =='plot':O0OO000OO0O000OOO .show_pool_plot (0 )#line:1101
        elif callable (O0OO000OO0O000OOO .show_pool_func ):O0OO000OO0O000OOO .show_pool (0 )#line:1102
        elif type (show_pool_func )==str :#line:1103
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1104
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1105
                O0OO000OO0O000OOO .show_pool_save (0 )#line:1106
        O0OOO0000000OOO0O =0 #line:1109
        for O0O0OO0OOO00OO0O0 in range (1 ,O0OO000OO0O000OOO .max_n +1 ):#line:1110
            OOOOOO0OOOO000O00 =np .arange (O0OO000OO0O000OOO .pool_num )#line:1113
            nr .shuffle (OOOOOO0OOOO000O00 )#line:1114
            OOOOOO0OOOO000O00 =OOOOOO0OOOO000O00 .reshape ((O0OO000OO0O000OOO .pool_num //O0OO000OO0O000OOO .parent_num ),O0OO000OO0O000OOO .parent_num )#line:1115
            Parallel (n_jobs =O0OO000OO0O000OOO .core_num ,require ='sharedmem')([delayed (O0OO000OO0O000OOO .setGA_multi )(O0OO0OOO000O0O000 )for O0OO0OOO000O0O000 in OOOOOO0OOOO000O00 ])#line:1118
            O0OOO0000000OOO0O +=O0OO000OO0O000OOO .end_check ()#line:1154
            O0OO000OO0O000OOO .save_best_mean ()#line:1157
            if O0OO000OO0O000OOO .show_pool_func ==None :pass #line:1160
            elif O0OO000OO0O000OOO .show_pool_func =='bar':O0OO000OO0O000OOO .show_pool_bar (O0O0OO0OOO00OO0O0 *O0OO000OO0O000OOO .pool_num )#line:1161
            elif O0OO000OO0O000OOO .show_pool_func =='print':O0OO000OO0O000OOO .show_pool_print (O0O0OO0OOO00OO0O0 *O0OO000OO0O000OOO .pool_num )#line:1162
            elif O0OO000OO0O000OOO .show_pool_func =='plot':O0OO000OO0O000OOO .show_pool_plot (O0O0OO0OOO00OO0O0 *O0OO000OO0O000OOO .pool_num )#line:1163
            elif callable (O0OO000OO0O000OOO .show_pool_func ):O0OO000OO0O000OOO .show_pool (O0O0OO0OOO00OO0O0 *O0OO000OO0O000OOO .pool_num )#line:1164
            elif type (show_pool_func )==str :#line:1165
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1166
                    O0OO000OO0O000OOO .show_pool_save (O0O0OO0OOO00OO0O0 )#line:1167
            if O0OOO0000000OOO0O >=1 :#line:1170
                break #line:1171
        O00O0OOOO0000O0OO =O0OO000OO0O000OOO .para_range [O0OO000OO0O000OOO .pool_best ]#line:1174
        if O0OO000OO0O000OOO .show_pool_func =='bar':print ()#line:1177
        elif type (show_pool_func )==str :#line:1178
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1179
                print ()#line:1180
        if O0OO000OO0O000OOO .show_pool_func !=None :#line:1183
            print ('__________________ results _________________')#line:1184
            print ('para : {}'.format (O00O0OOOO0000O0OO ))#line:1185
            print ('score : {}'.format (O0OO000OO0O000OOO .score_best ))#line:1186
            print ('____________________ end ___________________')#line:1187
        return O00O0OOOO0000O0OO ,O0OO000OO0O000OOO .score_best #line:1189
    def rcGA_multi (OO0OO0000OO0OO0O0 ,O000OO00O0000O0O0 ):#line:1217
        OO0O00O0OOOO0O0O0 =OO0OO0000OO0OO0O0 .pool [O000OO00O0000O0O0 ]#line:1219
        OO00O0O0O00OO0O0O =OO0OO0000OO0OO0O0 .pool_score [O000OO00O0000O0O0 ]#line:1220
        OO0000O00OOO0O0OO =np .ones ((OO0OO0000OO0OO0O0 .child_num ,OO0OO0000OO0OO0O0 .para_num ),dtype =float )*2.0 #line:1221
        OOO0OO00OO0O0O00O =np .zeros (OO0OO0000OO0OO0O0 .child_num )#line:1222
        OO000OOOO0O0OOOOO =np .mean (OO0O00O0OOOO0O0O0 ,axis =0 )#line:1227
        for O00OOO00OOO0O000O in range (OO0OO0000OO0OO0O0 .child_num ):#line:1230
            for OOO0OOOOO0000OOOO in range (OO0OO0000OO0OO0O0 .para_num ):#line:1231
                OO0000O00OOO0O0OO [O00OOO00OOO0O000O ,OOO0OOOOO0000OOOO ]=OO000OOOO0O0OOOOO [OOO0OOOOO0000OOOO ]#line:1233
                for O00OOOOOOO0O0OOO0 in range (OO0OO0000OO0OO0O0 .parent_num ):#line:1235
                    OO0000O00OOO0O0OO [O00OOO00OOO0O000O ,OOO0OOOOO0000OOOO ]+=nr .normal (0 ,OO0OO0000OO0OO0O0 .sd )*(OO0O00O0OOOO0O0O0 [O00OOOOOOO0O0OOO0 ][OOO0OOOOO0000OOOO ]-OO000OOOO0O0OOOOO [OOO0OOOOO0000OOOO ])#line:1236
        OO0000O00OOO0O0OO =np .clip (OO0000O00OOO0O0OO ,0.0 ,1.0 )#line:1238
        for O00OOO00OOO0O000O in range (OO0OO0000OO0OO0O0 .child_num ):#line:1242
            O00OOO0OOOO0O00OO =OO0000O00OOO0O0OO [O00OOO00OOO0O000O ]*(OO0OO0000OO0OO0O0 .para_range [:,1 ]-OO0OO0000OO0OO0O0 .para_range [:,0 ])+OO0OO0000OO0OO0O0 .para_range [:,0 ]#line:1243
            OOO0OO00OO0O0O00O [O00OOO00OOO0O000O ]=OO0OO0000OO0OO0O0 .score_func (O00OOO0OOOO0O00OO )#line:1244
        O0OO0O0O0O00000O0 =np .vstack ((OO0000O00OOO0O0OO ,OO0O00O0OOOO0O0O0 ))#line:1246
        OO00O0O000O00O0O0 =np .hstack ((OOO0OO00OO0O0O00O ,OO00O0O0O00OO0O0O ))#line:1247
        OO00000OOO0O000O0 =np .argpartition (np .abs (OO0OO0000OO0OO0O0 .aim -OO00O0O000O00O0O0 ),OO0OO0000OO0OO0O0 .parent_num )[:OO0OO0000OO0OO0O0 .parent_num ]#line:1249
        OO0OO0000OO0OO0O0 .pool [O000OO00O0000O0O0 ]=O0OO0O0O0O00000O0 [OO00000OOO0O000O0 ]#line:1250
        OO0OO0000OO0OO0O0 .pool_score [O000OO00O0000O0O0 ]=OO00O0O000O00O0O0 [OO00000OOO0O000O0 ]#line:1251
    def rcGA (OOOOOO0000OO0OO0O ,O0O00O00OO0000O0O ,OO0O000O0O0O00OO0 ,O0O00O00O0OO0O0OO ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1254
        O0O00O00OO0000O0O =np .array (O0O00O00OO0000O0O )#line:1259
        if O0O00O00OO0000O0O .ndim ==1 :#line:1260
            O0O00O00OO0000O0O =O0O00O00OO0000O0O .reshape (1 ,2 )#line:1261
        OOOOOO0000OO0OO0O .setting_1 (O0O00O00OO0000O0O ,OO0O000O0O0O00OO0 ,O0O00O00O0OO0O0OO ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1264
        OOOOOO0000OO0OO0O .setting_2 (OOOOOO0000OO0OO0O .para_num *10 ,2 ,4 )#line:1265
        OOOOOO0000OO0OO0O .setting_3 (float )#line:1266
        OOOOOO0000OO0OO0O .print_info ()#line:1267
        OOOOOO0000OO0OO0O .sd =1.2 /math .sqrt (OOOOOO0000OO0OO0O .parent_num )#line:1270
        if OOOOOO0000OO0OO0O .para_num ==1 :#line:1275
            O0O00000OOOOOOOOO =np .tile (np .array ([0.5 ]),(OOOOOO0000OO0OO0O .pool_num //OOOOOO0000OO0OO0O .para_num )+1 )#line:1276
        else :#line:1277
            O0O00000OOOOOOOOO =np .tile (np .arange (0.0 ,1.000001 ,1.0 /(OOOOOO0000OO0OO0O .para_num -1 )),(OOOOOO0000OO0OO0O .pool_num //OOOOOO0000OO0OO0O .para_num )+1 )#line:1278
        for O0OO000OOO0OOO000 in range (OOOOOO0000OO0OO0O .para_num ):#line:1281
            OOOOOO0000OO0OO0O .pool [:,O0OO000OOO0OOO000 ]=nr .permutation (O0O00000OOOOOOOOO [:OOOOOO0000OO0OO0O .pool_num ])#line:1282
        if OOOOOO0000OO0OO0O .para_num ==1 :#line:1285
            OOOOOO0000OO0OO0O .pool +=nr .rand (OOOOOO0000OO0OO0O .pool_num ,OOOOOO0000OO0OO0O .para_num )*1.0 -0.5 #line:1286
        else :#line:1287
            OOOOOO0000OO0OO0O .pool +=nr .rand (OOOOOO0000OO0OO0O .pool_num ,OOOOOO0000OO0OO0O .para_num )*(2.0 /(3 *OOOOOO0000OO0OO0O .para_num -3 ))-(1.0 /(3 *OOOOOO0000OO0OO0O .para_num -3 ))#line:1288
        OOOOOO0000OO0OO0O .pool =np .clip (OOOOOO0000OO0OO0O .pool ,0.0 ,1.0 )#line:1291
        def O0OOOOOOOOOO0O0O0 (O0O0OOO0OO0000O0O ):#line:1294
            O00OOO0OOO0OO00O0 =np .expand_dims (OOOOOO0000OO0OO0O .pool ,axis =1 )-np .expand_dims (OOOOOO0000OO0OO0O .pool ,axis =0 )#line:1295
            O00OOO0OOO0OO00O0 =np .sqrt (np .sum (O00OOO0OOO0OO00O0 **2 ,axis =-1 ))#line:1296
            O00OOO0OOO0OO00O0 =np .sum (O00OOO0OOO0OO00O0 ,axis =-1 )/OOOOOO0000OO0OO0O .pool_num #line:1297
            return O00OOO0OOO0OO00O0 #line:1298
        if OOOOOO0000OO0OO0O .pool_num <=5 *10 :#line:1301
            OO0O0000O0OO0O000 =200 #line:1302
        elif OOOOOO0000OO0OO0O .pool_num <=10 *10 :#line:1303
            OO0O0000O0OO0O000 =150 #line:1304
        elif OOOOOO0000OO0OO0O .pool_num <=15 *10 :#line:1305
            OO0O0000O0OO0O000 =70 #line:1306
        elif OOOOOO0000OO0OO0O .pool_num <=20 *10 :#line:1307
            OO0O0000O0OO0O000 =30 #line:1308
        elif OOOOOO0000OO0OO0O .pool_num <=30 *10 :#line:1309
            OO0O0000O0OO0O000 =12 #line:1310
        else :#line:1311
            OO0O0000O0OO0O000 =0 #line:1312
        O0O0O00OO0O00OO00 =False #line:1313
        for OO0O0O0000O0OOO00 in range (OO0O0000O0OO0O000 ):#line:1314
            OOO0O000OOO0O00OO =O0OOOOOOOOOO0O0O0 (OOOOOO0000OO0OO0O .pool )#line:1315
            OOO0O0O00OO0O00OO =np .argmin (OOO0O000OOO0O00OO )#line:1316
            OOOOOO0000OO0OO0O .pool [OOO0O0O00OO0O00OO ]=nr .rand (OOOOOO0000OO0OO0O .para_num )#line:1318
            OOOOO000000O0OO00 =O0OOOOOOOOOO0O0O0 (OOOOOO0000OO0OO0O .pool )#line:1319
            OOOOOOO0OO0OO00O0 =0 #line:1321
            while np .sum (OOOOO000000O0OO00 )<np .sum (OOO0O000OOO0O00OO ):#line:1322
                OOOOOO0000OO0OO0O .pool [OOO0O0O00OO0O00OO ]=nr .rand (OOOOOO0000OO0OO0O .para_num )#line:1324
                OOOOO000000O0OO00 =O0OOOOOOOOOO0O0O0 (OOOOOO0000OO0OO0O .pool )#line:1325
                OOOOOOO0OO0OO00O0 +=1 #line:1326
                if OOOOOOO0OO0OO00O0 ==OO0O0000O0OO0O000 :#line:1327
                    O0O0O00OO0O00OO00 =True #line:1329
                    break #line:1330
            if O0O0O00OO0O00OO00 ==True :#line:1331
                break #line:1332
        OOOOOO0000OO0OO0O .score_pool_rc ()#line:1337
        OOOOOO0000OO0OO0O .save_best_mean ()#line:1338
        OOOOOO0000OO0OO0O .init_score_range =(np .min (OOOOOO0000OO0OO0O .pool_score ),np .max (OOOOOO0000OO0OO0O .pool_score ))#line:1340
        OOOOOO0000OO0OO0O .init_gap_mean =deepcopy (OOOOOO0000OO0OO0O .gap_mean )#line:1341
        if OOOOOO0000OO0OO0O .show_pool_func ==None :pass #line:1344
        elif OOOOOO0000OO0OO0O .show_pool_func =='bar':OOOOOO0000OO0OO0O .show_pool_bar (0 )#line:1345
        elif OOOOOO0000OO0OO0O .show_pool_func =='print':OOOOOO0000OO0OO0O .show_pool_print (0 )#line:1346
        elif OOOOOO0000OO0OO0O .show_pool_func =='plot':OOOOOO0000OO0OO0O .show_pool_plot (0 )#line:1347
        elif callable (OOOOOO0000OO0OO0O .show_pool_func ):OOOOOO0000OO0OO0O .show_pool_rc (0 )#line:1348
        elif type (show_pool_func )==str :#line:1349
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1350
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1351
                OOOOOO0000OO0OO0O .show_pool_save (0 )#line:1352
        OOOOOOO0OO0OO00O0 =0 #line:1355
        for OOO00OO00O00O0OO0 in range (1 ,OOOOOO0000OO0OO0O .max_n +1 ):#line:1356
            O0O0OOO00O0O0OOO0 =np .arange (OOOOOO0000OO0OO0O .pool_num )#line:1359
            nr .shuffle (O0O0OOO00O0O0OOO0 )#line:1360
            O0O0OOO00O0O0OOO0 =O0O0OOO00O0O0OOO0 .reshape ((OOOOOO0000OO0OO0O .pool_num //OOOOOO0000OO0OO0O .parent_num ),OOOOOO0000OO0OO0O .parent_num )#line:1361
            Parallel (n_jobs =OOOOOO0000OO0OO0O .core_num ,require ='sharedmem')([delayed (OOOOOO0000OO0OO0O .rcGA_multi )(O0OOO0OO0O0000OOO )for O0OOO0OO0O0000OOO in O0O0OOO00O0O0OOO0 ])#line:1364
            OOOOOO0000OO0OO0O .sd =max (OOOOOO0000OO0OO0O .sd *0.995 ,0.9 /math .sqrt (OOOOOO0000OO0OO0O .parent_num ))#line:1394
            if np .max (np .std (OOOOOO0000OO0OO0O .pool ,axis =0 ))<0.03 :#line:1397
                OOOOOOO0OO0OO00O0 +=1 #line:1398
            OOOOOO0000OO0OO0O .save_best_mean ()#line:1401
            if OOOOOO0000OO0OO0O .show_pool_func ==None :pass #line:1404
            elif OOOOOO0000OO0OO0O .show_pool_func =='bar':OOOOOO0000OO0OO0O .show_pool_bar (OOO00OO00O00O0OO0 *OOOOOO0000OO0OO0O .pool_num )#line:1405
            elif OOOOOO0000OO0OO0O .show_pool_func =='print':OOOOOO0000OO0OO0O .show_pool_print (OOO00OO00O00O0OO0 *OOOOOO0000OO0OO0O .pool_num )#line:1406
            elif OOOOOO0000OO0OO0O .show_pool_func =='plot':OOOOOO0000OO0OO0O .show_pool_plot (OOO00OO00O00O0OO0 *OOOOOO0000OO0OO0O .pool_num )#line:1407
            elif callable (OOOOOO0000OO0OO0O .show_pool_func ):OOOOOO0000OO0OO0O .show_pool_rc (OOO00OO00O00O0OO0 *OOOOOO0000OO0OO0O .pool_num )#line:1408
            elif type (show_pool_func )==str :#line:1409
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1410
                    OOOOOO0000OO0OO0O .show_pool_save (OOO00OO00O00O0OO0 )#line:1411
            if OOOOOOO0OO0OO00O0 >=1 :#line:1414
                break #line:1415
        O0OOOO00O00O0O0O0 =OOOOOO0000OO0OO0O .pool_best *(OOOOOO0000OO0OO0O .para_range [:,1 ]-OOOOOO0000OO0OO0O .para_range [:,0 ])+OOOOOO0000OO0OO0O .para_range [:,0 ]#line:1418
        if OOOOOO0000OO0OO0O .show_pool_func =='bar':print ()#line:1421
        elif type (show_pool_func )==str :#line:1422
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1423
                print ()#line:1424
        if OOOOOO0000OO0OO0O .show_pool_func !=None :#line:1427
            print ('__________________ results _________________')#line:1428
            print ('para : {}'.format (O0OOOO00O00O0O0O0 ))#line:1429
            print ('score : {}'.format (OOOOOO0000OO0OO0O .score_best ))#line:1430
            print ('____________________ end ___________________')#line:1431
        return O0OOOO00O00O0O0O0 ,OOOOOO0000OO0OO0O .score_best #line:1433
if __name__ =='__main__':#line:1443
    pass #line:1444
