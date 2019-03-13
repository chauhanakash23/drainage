import numpy as np
import resource, sys
import copy

resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

test_matrix  = np.array([
    [5, 5, 5, 5, 5],
    [9, 1, 1, 1, 5],
    [5, 1, 5, 1, 5],
    [5, 1, 1, 1, 5],
    [5, 5, 5, 5, 5]
])
test_matrix_1  = np.array([
    [3, 3, 3, 3, 3, 3],
    [3, 1, 2, 3, 1, 3],
    [3, 1, 2, 3, 1, 3],
    [3, 3, 3, 1, 3, 3],
])

#storage_matrix  = np.zeros(shape=test_matrix.shape)

def check_plane(matrix,r,c,plane_list,boundary_list,global_recurssion_list):
    current_ele = matrix[r][c]
    plane_list.append((r,c))
    recursion_list = []
    if r == 0 or c == 0 or r == matrix.shape[0] or c == matrix.shape[1]:
        return
    if matrix[r-1][c] == current_ele:
        if (r-1,c) in plane_list and (r-1,c) in global_recurssion_list:
            pass
        else:
            recursion_list.append((r-1,c))
            global_recurssion_list.append((r-1,c))
    if matrix[r][c+1] == current_ele:
        if (r,c+1) in plane_list and (r,c+1) in global_recurssion_list:
            pass
        else:
            recursion_list.append((r,c+1))
            global_recurssion_list.append((r,c+1))
    if matrix[r+1][c] == current_ele:
        if (r+1,c) in plane_list and (r+1,c) in global_recurssion_list:
            pass
        else:
            recursion_list.append((r+1,c))
            global_recurssion_list.append((r+1,c))
    if matrix[r][c-1] == current_ele:
        if (r,c-1) in plane_list and (r,c-1) in global_recurssion_list:
            pass
        else:
            recursion_list.append((r,c-1))
            global_recurssion_list.append((r,c-1))
    if (r-1,c) not in recursion_list and (r-1,c) not in plane_list and (r-1,c) not in global_recurssion_list:
        boundary_list.append(matrix[(r-1,c)])
    if (r,c+1) not in recursion_list and (r,c+1) not in plane_list and (r,c+1) not in global_recurssion_list:
        boundary_list.append(matrix[(r,c+1)])
    if (r+1,c) not in recursion_list and (r+1,c) not in plane_list and (r+1,c) not in global_recurssion_list:
        boundary_list.append(matrix[(r+1,c)])
    if (r,c-1) not in recursion_list and (r,c-1) not in plane_list and (r,c-1) not in global_recurssion_list:
        boundary_list.append(matrix[(r,c-1)])
    
    for i in recursion_list:
        check_plane(matrix,i[0],i[1],plane_list,boundary_list,global_recurssion_list)
    return

def check_plane_master(matrix,r,c):
    plane_list = []
    boundary_list = []
    global_recurssion_list = []
    check_plane(matrix,r,c,plane_list,boundary_list,global_recurssion_list)
    plane_list = list(set(plane_list))
    if len(plane_list) > 0:
        volume = (min(boundary_list)-matrix[r][c])
    #for i in plane_list:
    #    storage_matrix[i] += volume
    return plane_list,volume

def destroy_zeros_neighbours(matrix,storage_matrix):
    idx_to_destroy = []
    for i,x in np.ndenumerate(matrix):
        if x == 0:
            idx_to_destroy.append((i[0]-1,i[1]-1))
            idx_to_destroy.append((i[0]-1,i[1]+1))
            idx_to_destroy.append((i[0]+1,i[1]-1))
            idx_to_destroy.append((i[0]+1,i[1]+1))
            idx_to_destroy.append((i[0]-1,i[1]))
            idx_to_destroy.append((i[0],i[1]+1))
            idx_to_destroy.append((i[0]+1,i[1]))
            idx_to_destroy.append((i[0],i[1]-1))
            #plane,v = check_plane_master(matrix,i[0],i[1])
            #for i in plane:
            #    storage_matrix[i] = 0
    for i in idx_to_destroy:
        if i[0] < 0 or i[1] < 0 or i[0] >= matrix.shape[0] or i[1] >= matrix.shape[1]:
            continue
        else:
            storage_matrix[i] = 0
            
def get_min_idx(matrix):
    min_value = float("inf")
    min_idx = []
    for i,x in np.ndenumerate(matrix):
        if i[0] == 0 or i[1] == 0 or i[0] == matrix.shape[0]-1 or i[1] == matrix.shape[1]-1:
            continue
        if min_value >= x and x!=0:
            min_value = x
    for i,x in np.ndenumerate(matrix):
        if i[0] == 0 or i[1] == 0 or i[0] == matrix.shape[0]-1 or i[1] == matrix.shape[1]-1:
            continue
        if x == min_value and x!=0:
            min_idx.append(i)
    return (min_idx,min_value)

def get_max_value(matrix):
    max_value = 0
    max_idx = []
    for i,x in np.ndenumerate(matrix):
        if x >= max_value:
            max_value = x
            max_idx.append(i)
    return (max_value,max_idx)

def check_neighbours(matrix,r,c):
    ret = True
    current_ele = matrix[r][c]
    if matrix[r-1][c] >= current_ele:
        pass
    else:
        return False
    if matrix[r][c+1] >= current_ele:
        pass
    else:
        return False
    if matrix[r+1][c] >= current_ele:
        pass
    else:
        return False
    if matrix[r][c-1] >= current_ele:
        pass
    else:
        return False
    return ret

def check_matrix_overflow(matrix):
    ret = True
    min_idx = get_min_idx(matrix)[0]
    for i in min_idx:
        ret = check_neighbours(matrix,i[0],i[1])
        if ret == False:
            return False
    return ret

def fill_one(matrix,storage_matrix,tmp_storage_matrix):
    #get minimum value and its index
    tmp_matrix = copy.deepcopy(matrix)
    min_idx = get_min_idx(matrix)[0]
    for i in min_idx:
        tmp_matrix[i] += 1
        tmp_storage_matrix[i] = storage_matrix[i]
        storage_matrix[i] += 1
    return tmp_matrix

def routine(matrix):
    storage_matrix  = np.zeros(shape=matrix.shape)
    tmp_storage_matrix  = np.zeros(shape=matrix.shape)
    max_iter = get_max_value(matrix)[0]
    tmp_matrix = fill_one(matrix,storage_matrix,tmp_storage_matrix)
    for _ in range(max_iter-1):
        tmp_matrix = fill_one(tmp_matrix,storage_matrix,tmp_storage_matrix)
        if check_matrix_overflow(tmp_matrix) == False:
            break
    destroy_zeros_neighbours(matrix,storage_matrix)
    destroy_zeros_neighbours(matrix,tmp_storage_matrix)
    return storage_matrix.sum(),tmp_storage_matrix.sum()
    