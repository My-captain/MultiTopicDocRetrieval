import random
import math


def initial_d_p_vector(type_num):
    """
    初始化D&P
    :param type_num: 类别个数
    :return: D/P向量
    """
    return [0 for i in range(type_num)], [1 / type_num for i in range(type_num)]


def update_d_value(origin_d_vector, current_vector, session_num):
    """
    更新d值
    :param origin_d_vector: 原d值向量 list<float>
    :param current_vector: 当前用户打分向量 list<float>
    :param session_num: 会话数量 int
    :return: 更新后的d值向量
    """
    return [origin_d_vector[i] + current_vector[i] / session_num for i in range(len(origin_d_vector))]


def update_p_value(origin_p_vector, current_vector, eta):
    """
    更新p值
    :param origin_p_vector: 原p值向量 list<float>
    :param current_vector: 原d值向量 list<float>
    :param eta: 更新系数η float
    :return: 更新后的p值向量
    """
    r = 1 - eta
    max_d_idx = current_vector.index(max(current_vector))
    return [origin_p_vector[i] * r if i != max_d_idx else origin_p_vector[i] * r + eta for i in range(len(origin_p_vector))]


def sort_docs_by_dp(doc_list, d_vector, p_vector):
    """
    根据D/P向量对文献列表进行排序
    :param doc_list: list<DocModel>
    :param d_vector: d值向量
    :param p_vector: p值向量
    :return: list<DocModel>
    """
    rand = random.uniform(0, sum(p_vector))
    top_class_idx = 0
    while rand >= 0:
        rand -= p_vector[top_class_idx]
        top_class_idx += 1
    top_class_idx -= 1
    top_doc_list = [i for i in doc_list if i.classification == top_class_idx]
    sort_doc_list = [i for i in doc_list if i.classification != top_class_idx]
    return top_doc_list + sorted(sort_doc_list, key=lambda x: d_vector[x.classification], reverse=True)


def calc_precision(rel_list, origin_list):
    rels = []
    s = 0
    t = 0
    for k, v in enumerate(rel_list):
        print(v['document_id'], origin_list[k].id)
        if v['user_relevant']:
            rels.append(k)
            s += math.log10(k + 1)
            s -= math.log10(len(rels))
            for i, j in enumerate(origin_list):
                if int(v['document_id']) == j.id:
                    t += math.log10(i + 1)
                    t -= math.log10(len(rels))
                    break
    m = math.log(math.factorial(len(rel_list)) / (math.factorial(len(rel_list) - len(rels)) * math.factorial(len(rels))))
    if m == 0:
        return 1, 1
    return 1 - s / m, 1 - t / m