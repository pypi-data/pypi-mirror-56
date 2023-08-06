import numpy as np
import numba
from functools import reduce
import gc
from scipy.stats import chi2


def remma_add(y, xmat, gmat_lst, var_com, bed_file):
    """
    # 加性检验
    :param y: 表型
    :param xmat: 固定效应设计矩阵
    :param gmat_lst: 基因组关系矩阵列表
    :param var_com: 方差组分
    :param bed_file: plink文件
    :return:
    """
    # 计算V矩阵
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    vmat = np.diag([var_com[-1]] * n)
    for val in range(len(gmat_lst)):
        vmat += gmat_lst[val] * var_com[val]
    vmat_inv = np.linalg.inv(vmat)
    # 计算P矩阵
    vxmat = np.dot(vmat_inv, xmat)
    xvxmat = np.dot(xmat.T, vxmat)
    xvxmat = np.linalg.inv(xvxmat)
    pmat = reduce(np.dot, [vxmat, xvxmat, vxmat.T])
    pmat = vmat_inv - pmat
    pymat = np.dot(pmat, y)
    pvpmat = reduce(np.dot, [pmat, vmat, pmat])
    del vmat, vmat_inv, pmat
    gc.collect()
    # 读取SNP文件
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    snp_mat = snp_mat - 2 * freq
    eff_vec = np.dot(snp_mat.T, pymat)[:, -1]
    var_vec = np.sum(snp_mat * np.dot(pvpmat, snp_mat), axis=0)
    chi_vec = eff_vec*eff_vec/var_vec
    p_vec = chi2.sf(chi_vec, 1)
    snp_info_file = bed_file + '.bim'
    snp_info = pd.read_csv(snp_info_file, sep='\s+', header=None)
    res_df = snp_info.iloc[:, [0, 1, 3, 4, 5]]
    res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
    res_df.loc[:, 'eff_val'] = eff_vec
    res_df.loc[:, 'chi_val'] = chi_vec
    res_df.loc[:, 'p_val'] = p_vec
    return res_df


def remma_dom(y, xmat, gmat_lst, var_com, bed_file):
    """
    # 显性检验
    :param y: 表型
    :param xmat: 固定效应设计矩阵
    :param gmat_lst: 基因组关系矩阵列表
    :param var_com: 方差组分
    :param bed_file: plink文件
    :return:
    """
    # 计算V矩阵
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    vmat = np.diag([var_com[-1]] * n)
    for val in range(len(gmat_lst)):
        vmat += gmat_lst[val] * var_com[val]
    vmat_inv = np.linalg.inv(vmat)
    # 计算P矩阵
    vxmat = np.dot(vmat_inv, xmat)
    xvxmat = np.dot(xmat.T, vxmat)
    xvxmat = np.linalg.inv(xvxmat)
    pmat = reduce(np.dot, [vxmat, xvxmat, vxmat.T])
    pmat = vmat_inv - pmat
    pymat = np.dot(pmat, y)
    pvpmat = reduce(np.dot, [pmat, vmat, pmat])
    del vmat, vmat_inv, pmat
    gc.collect()
    # 读取SNP文件
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    snp_mat[snp_mat > 1.5] = 0.0
    snp_mat = snp_mat - 2 * freq * (1 - freq)
    eff_vec = np.dot(snp_mat.T, pymat)[:, -1]
    var_vec = np.sum(snp_mat * np.dot(pvpmat, snp_mat), axis=0)
    chi_vec = eff_vec*eff_vec/var_vec
    p_vec = chi2.sf(chi_vec, 1)
    snp_info_file = bed_file + '.bim'
    snp_info = pd.read_csv(snp_info_file, sep='\s+', header=None)
    res_df = snp_info.iloc[:, [0, 1, 3, 4, 5]]
    res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
    res_df.loc[:, 'eff_val'] = eff_vec
    res_df.loc[:, 'chi_val'] = chi_vec
    res_df.loc[:, 'p_val'] = p_vec
    return res_df


def remma_epiAA(y, xmat, gmat_lst, var_com, bed_file):
    """
    # 加加上位检验
    :param y: 表型
    :param xmat: 固定效应设计矩阵
    :param gmat_lst: 基因组关系矩阵列表
    :param var_com: 方差组分
    :param bed_file: plink文件
    :return:
    """
    # 计算V矩阵
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    vmat = np.diag([var_com[-1]] * n)
    for val in range(len(gmat_lst)):
        vmat += gmat_lst[val] * var_com[val]
    vmat_inv = np.linalg.inv(vmat)
    # 计算P矩阵
    vxmat = np.dot(vmat_inv, xmat)
    xvxmat = np.dot(xmat.T, vxmat)
    xvxmat = np.linalg.inv(xvxmat)
    pmat = reduce(np.dot, [vxmat, xvxmat, vxmat.T])
    pmat = vmat_inv - pmat
    pymat = np.dot(pmat, y)
    pvpmat = reduce(np.dot, [pmat, vmat, pmat])
    del vmat, vmat_inv, pmat
    gc.collect()
    # 读取SNP文件
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    snp_mat = snp_mat - 2 * freq
    res_dct = {}
    for i in range(snp_mat.shape[1] - 1):
        epi_mat = snp_mat[:, i:i+1] * snp_mat[:, (i+1):]
        eff_vec = np.dot(epi_mat.T, pymat)
        var_vec = np.sum(epi_mat * np.dot(pvpmat, epi_mat), axis=0)
        var_vec = var_vec.reshape(len(var_vec), -1)
        chi_vec = eff_vec * eff_vec / var_vec
        p_vec = chi2.sf(chi_vec, 1)
        res = np.concatenate([np.array([i]*(snp_mat.shape[1]-i-1)).reshape(snp_mat.shape[1]-i-1, -1), np.arange((i+1), snp_mat.shape[1]).reshape(snp_mat.shape[1]-i-1, -1), eff_vec, p_vec], axis=1)
        res_dct[i] = res[res[:, -1] < 0.001, :]
    return res_dct


@numba.jit(nopython=True)
def remma_epiAA_test(snp_mat, pymat, pvpmat):
    res_dct = {}
    for i in range(snp_mat.shape[1] - 1):
        epi_mat = snp_mat[:, i:i + 1] * snp_mat[:, (i + 1):]
        eff_vec = np.dot(epi_mat.T, pymat)
        var_vec = np.sum(epi_mat * np.dot(pvpmat, epi_mat), axis=0)
        var_vec = var_vec.reshape(len(var_vec), -1)
        chi_vec = eff_vec * eff_vec / var_vec
        p_vec = chi2.sf(chi_vec, 1)
        res = np.concatenate([np.array([i] * (snp_mat.shape[1] - i - 1)).reshape(snp_mat.shape[1] - i - 1, -1),
                              np.arange((i + 1), snp_mat.shape[1]).reshape(snp_mat.shape[1] - i - 1, -1), eff_vec,
                              p_vec], axis=1)
        res_dct[i] = res[res[:, -1] < 0.001, :]
    return res_dct


def remma_epiAA_gpu(y, xmat, gmat_lst, var_com, bed_file):
    """
    # 加加上位检验
    :param y: 表型
    :param xmat: 固定效应设计矩阵
    :param gmat_lst: 基因组关系矩阵列表
    :param var_com: 方差组分
    :param bed_file: plink文件
    :return:
    """
    # 计算V矩阵
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    vmat = np.diag([var_com[-1]] * n)
    for val in range(len(gmat_lst)):
        vmat += gmat_lst[val] * var_com[val]
    vmat_inv = np.linalg.inv(vmat)
    # 计算P矩阵
    vxmat = np.dot(vmat_inv, xmat)
    xvxmat = np.dot(xmat.T, vxmat)
    xvxmat = np.linalg.inv(xvxmat)
    pmat = reduce(np.dot, [vxmat, xvxmat, vxmat.T])
    pmat = vmat_inv - pmat
    pymat = np.dot(pmat, y)
    pvpmat = reduce(np.dot, [pmat, vmat, pmat])
    del vmat, vmat_inv, pmat
    gc.collect()
    # 读取SNP文件
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    snp_mat = snp_mat - 2 * freq
    res_dct = remma_epiAA_test(snp_mat, pymat, pvpmat)
    return res_dct
