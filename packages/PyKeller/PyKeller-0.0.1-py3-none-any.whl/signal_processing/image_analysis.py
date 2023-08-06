#Image Analysis functions

import numpy as np

def mean_pixel(img,n):
    m = 2*n + 1
    end_i = img.shape[0]
    end_j = img.shape[1]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            edge_i = [i<n, i>=n and i<=end_i-n, i>end_i-n]
            edge_j = [j<n, j>=n and j<=end_j-n, j>end_j-n]
            ind_i = np.where(edge_i)[0][0]
            ind_j = np.where(edge_j)[0][0]
            k_i = [n-i, 0, i-(end_i-n)]
            k_j = [n-j, 0, j-(end_j-n)]
            start_i = [0, i-int(np.floor(m/2)), i-int(np.floor(m/2))]
            stop_i = [i+int(np.ceil(m/2)), i+int(np.ceil(m/2)), end_i]
            start_j = [0, j-int(np.floor(m/2)), j-int(np.floor(m/2))]
            stop_j = [j+int(np.ceil(m/2)), j+int(np.ceil(m/2)), end_j]
            img[i,j] = np.sum(img[start_i[ind_i]:stop_i[ind_i], start_j[ind_j]:stop_j[ind_j]])/(m**2 - k_j[ind_j]*m - k_i[ind_i]*(m - k_j[ind_j]))
            
def alone_pixels(img,n):
    end_i = img.shape[0]
    end_j = img.shape[1]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            edge_i = [i<1, i>=1 and i<=end_i-1, i>end_i-1]
            edge_j = [j<1, j>=1 and j<=end_j-1, j>end_j-1]
            ind_i = np.where(edge_i)[0][0]
            ind_j = np.where(edge_j)[0][0]
            start_i = [0, i-1, i-1]
            stop_i = [i+2, i+2, end_i]
            start_j = [0, j-1, j-1]
            stop_j = [j+2, j+2, end_j]
            if img[i,j] == 1 and np.sum(img[start_i[ind_i]:stop_i[ind_i], start_j[ind_j]:stop_j[ind_j]]) < n+1:
                img[i,j] = 0
                
def next_scan_vert(img,pos):
    if np.where(img[:,pos[1]]>0)[0].size != 0:
        new_i = np.where(img[:,pos[1]]>0)[0][0]
    else:
        new_i = np.nan
    pos = (new_i,pos[1])
    return pos

def scan_grad_for(img,pos):
    n = 1
    i = pos[0]
    j = pos[1]
    end_i = img.shape[0]
    end_j = img.shape[1]
    while j+n < end_j:
        edge_i = [i-n<0, i-n>=0 and i+n<=end_i, i+n>end_i, i-n<0 and i+n>end_i]
        ind_i = np.where(edge_i)[0][0]
        start_i = [0, i-n, i-n, 0]
        stop_i = [i+n+1, i+n+1, end_i+1, end_i+1]
        x = img[start_i[ind_i]:stop_i[ind_i], j+n]
        max_pos = np.where(x==x.max())[0]
        if img[start_i[ind_i]:stop_i[ind_i], j+n].max() > 0.:
            if max_pos.size != 0:
                pos = (start_i[ind_i]+max_pos[0],j+n)
                return pos
            else:
                n+=1
        else:
            n+=1
    pos = (np.nan,np.nan)
    return pos

def trace_scan_grad_for(img,pos):
    pos_layer = []
    while pos[1] < img.shape[1]:
        pos = scan_grad_for(img,pos)
        if not np.isnan(pos[0]):
            pos_layer.append(pos)
    return pos_layer