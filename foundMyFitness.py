###################################
#
# Sample noteworthy genetic variants collected from various Found My Fitness
# reports. This data is compiled from multiple reports that have flagged these
# varients as noteworthy. Your mileage may vary.
#
# Note some SNPs have two variant combinations of interest. In that case, the
# second variant SNP starts with a '*' so that it represents a unique key in
# the dictionary structure. This '*' character will need to be stripped off
# by the program doing the analysis.
#
# Also Note: 23andMe reports all SNPs from the plus orientation.
# In the scientific literature, some are actually supposed to be reported from
# the opposite strand. Remember that A pairs with T and G with C. For these
# handful of SNPs that are reported from the opposite strand, FoundMyFitness
# makes the correction and effectively invert the letters... this is to
# correspond to the published science rather than 23andMe's
# arbitrary decision to differ in its reporting style.
#
# Per Found My Fitness, these results are NOT FOR MEDICAL PURPOSES and are subject
# to change. Raw data from genetic providers is suitable only for research,
# educational, and informational use and not for medical or other uses.
#
###################################

FMF_NOTEWORTHY = {
    'rs1695'    :['GSTP1',    'AA', 'Supplemental vitamin E has been shown to have a negative impact'],
    '*rs1695'   :['GSTP1',    'AG', 'Supplemental vitamin E has been shown to have a negative impact'],
    'rs7041'    :['VitD*',    'GT', 'Possible genetic risk for vitamin d deficiency'],
    '*rs7041'   :['VitD*',    'TT', 'This genotype increases the risk of vitamin D deficiency by two-fold.'],
    'rs6265'    :['BDNF',     'AG', 'Greater error in short-term motor learning'],
    'rs9939609' :['FTO',      'AT', 'Possible increased risk for obesity and type-2 diabetes'],
    'rs12340895':['JAK2',     'CG', '2-fold increased risk for blood cancer'],
    'rs1121980' :['FTO',      'CT', '1.67-fold increased risk for obesity particularly with saturated fat'],
    'rs429358'  :['APO-E3/E4', 'CT', "Increased heart disease risk and 2-3x increased alzheimer's disease risk"],
    'rs7412'    :['APO-E3/E4', 'CC', "Increased heart disease risk and 2-3x increased alzheimer's disease risk"],
    'rs1535'    :['FADS2',    'AG', '~26.7% poorer conversion of ala into omega-3 epa'],
    'rs174548'  :['FADS1',    'CG', 'Associated with intermediate phosphatidylcholine levels'],
    'rs7946'    :['PEMT',     'TT', 'Associated with lower phosphatidylcholine production (liver) with a second T increasing the effect'],
    'rs1801131' :['MTHFR',    'AA', 'Risk for altered folate metabolism and hyperhomocysteinemia'],
    'rs1801133' :['MTHFR',    'TT', 'Risk for altered folate metabolism and hyperhomocysteinemia'],
    'rs2282679' :['VitD*',    'AC', 'Associated with an increased risk of vitamin D deficiency'],
    'rs1421085' :['FTO',      'CT', '1.3-fold increased obesity risk and decreased thermogenesis'],
    'rs2802292' :['FOX03',    'GT', 'This genotype is associated with increased lifespan.'],
    'rs7501331' :['BCMO1',    'CT', '~32% reduced conversion of beta-carotene into retinal'],
    'rs4363657' :['SLCO1B1',  'CT', 'Increased risk for myopathy with statin use'],
    'rs4149056' :['SLCO1B1',  'CT', 'Increased risk for myopathy with statin use'],
    'rs2236225' :['MTHFD1',   'CT', 'Increased risk of choline deficiency even at adequate dietary choline intake'],
    'rs1042522' :['TP53',     'CG', 'Associated with increased lifespan'],
    'rs3803304' :['AKT1',     'GG', 'Associated with increased lifespan'],
    '*rs3803304':['AKT1',     'CG', 'Associated with increased lifespan and better response to chemotherapy'],
    'rs1800795' :['IL-6',     'CC', 'Normal lifespan and increased risk of certain diseases'],
    'rs1061170' :['CFH',      'CT', 'Normal lifespan; slightly increased risk for macular degeneration'],
    'rs2811712' :['CDKN2B-AS1', 'AG', 'Less risk of physical impairment with age'],
    'rs1801394' :['MTRR',     'GG', 'May be associated with hyperhomocysteinemia and altered choline metabolism'],
    'rs8192678' :['PGC-1α',   'AG', 'Slightly reduced cardiorespiratory fitness and slightly increased risk for type 2 diabetes'],
    '*rs8192678':['PGC-1α',   'GG', 'Slightly reduced cardiorespiratory fitness'],
    'rs1815739' :['ACTN3',    'CC', 'Enhanced fast-twitch muscle performance, more likely to favor sprint/power athletics'],
    'rs17817449':['FTO',      'GT', 'Saturated fat may have a negative effect on blood glucose and insulin levels'],
    'rs838133'  :['FGF21',    'CC', 'Preference for salty over sweet foods'],
    '*rs838133' :['FGF21',    'CT', 'Slight preference for sweet over salty foods, slight metabolic risk may affect dietary suitability'],
    'rs17782313':['MC4R',     'CT', 'Slightly higher body mass index (bmi), possibly affecting dietary suitability'],
    'rs762551'  :['CYP1A2',   'AC', 'Associated with slower caffeine metabolism'],
    'rs602662'  :['FUT2',     'GG', 'Associated with lower vitamin B12 levels'],
    '*rs602662' :['FUT2',     'AG', 'This genotype has been associated with slightly lower vitamin B12 levels'],
    'rs10063949':['SLC23A1',  'TT', 'Normal risk of crohn’s disease'],
    'rs1558902' :['FTO',      'AT', 'Associated with slight increase risk of obesity and greater weight loss on a high-protein diet.'],
    'rs601338'  :['FUT2',     'GG', 'Associated with lower vitamin b12 levels and susceptibility to norovirus infection'],
    '*rs601338' :['FUT2',     'AG', 'Associated with slightly lower vitamin b12 levels and susceptibility to norovirus infection'],
    'rs3184504' :['SH2B3',    'CT', 'Associated with a slight increased risk for celiac disease.'],
    'rs7903146' :['TCF7L2',   'CT', 'Has been associated with an increased risk for type 2 diabetes'],
    'rs2060793' :['CYP2R1',   'AA', 'Genetic risk for vitamin d deficiency'],
    'rs2305160' :['NPAS2',    'CC', 'Circadian-associated increased breast/prostate cancer risk'],
    'rs6922269' :['MTHFD1L',  'AG', 'Slight increased risk for cardiovascular disease'],
    'rs2542052' :['APOC3',    'CC', 'Associated with increased lifespan and better cardiovascular and metabolic health'],
    'i6010053'  :['FABP2',    'AG', 'Moderate increased sensitivity to saturated fats and refined sugars'],
    'rs7571842' :['SLC4A5',   'AA', 'Increased risk for salt sensitivity of blood pressure'],
    'rs2070895' :['LIPC',     'AG', 'Associated with slightly higher HDL-C levels'],
    'rs10830963':['MTNR1B',   'CG', 'Slight impaired glucose tolerance with a late dinner, slight increased risk for type-2 diabetes'],
    'rs11605924':['CRY2',     'AC', 'Associated with slight increase in fasting glucose levels']
    }
