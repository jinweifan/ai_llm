import numpy as np

def get_dot(vec_a, vec_b):
    """
    计算点积
    
    对两个向量的对应单个向量进行乘积，并将这些乘积求和，得到点积。
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be of the same length")
    return sum(a * b for a, b in zip(vec_a, vec_b))


def get_norm(vec):
    """
    计算模长
    
    对向量的每个单个向量进行平方，求和后取平方根，得到模长。
    """
    return np.sqrt(np.sum(x ** 2 for x in vec))


def get_cosine_similarity(vec_a, vec_b):
    """
    计算余弦相似度
    
    余弦相似度是通过点积除以两个向量的模长的乘积来计算的。
    """
    dot_product = get_dot(vec_a, vec_b)
    norm_a = get_norm(vec_a)
    norm_b = get_norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be zero vectors")
    
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    vec_a = [1, 2, 3]
    vec_b = [4, 5, 6]
    vec_c = [1, 2, 3]
    
    similarity_ab = get_cosine_similarity(vec_a, vec_b)
    print(f"vec_a and vec_b: {similarity_ab}")
    similarity_ac = get_cosine_similarity(vec_a, vec_c)
    print(f"vec_a and vec_c: {similarity_ac}")
    similarity_bc = get_cosine_similarity(vec_b, vec_c)
    print(f"vec_b and vec_c: {similarity_bc}")