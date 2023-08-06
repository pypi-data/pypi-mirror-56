import pandas as pd


bed_file = '/data/zhanglab/ningc/Acode/GLTA/PKG/examples/uvlmm/plink'
df = pd.read_csv("/data/zhanglab/ningc/Acode/GLTA/PKG/examples/uvlmm/pheno", header=None, sep='\s+')

y = np.array(df.iloc[:, -1:])
xmat = np.array(df.iloc[:, 2:-1])

mat1 = agmat(bed_file, inv=True, small_val=0.001)
mat2 = dgmat_as(bed_file, inv=True, small_val=0.001)

gmat_lst = [mat1[0], mat2[0], mat1[0]*mat1[0], mat1[0]*mat2[0], mat2[0]*mat2[0]]

var_com = wemai_multi_gmat(y, xmat, gmat_lst, init=None, maxiter=100, cc=1.0e-8)

res_df = remma_epiAA(y, xmat, gmat_lst, var_com, bed_file)
