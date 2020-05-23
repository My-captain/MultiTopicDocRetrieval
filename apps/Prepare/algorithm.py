import json
import math
import random
import pymysql
import os

REP_DOC_NUM = 2000
DOC_RANGE = 6000
VOC_FILE_PATH = r'Spider/older'
DOC_JSON_PATH = r'Spider/detail/older/'
CLASS_NUM = 5


def read_doc_list():
    rep_doc_list = []
    doc_list = []
    for i in os.listdir(DOC_JSON_PATH):
        with open(DOC_JSON_PATH + i, "r", encoding="utf-8") as detail:
            doc_list += json.loads(detail.read())
    doc_list = doc_list[:DOC_RANGE]
    random.shuffle(doc_list)
    for doc in doc_list[:REP_DOC_NUM]:
        rep_doc_list.append((doc['title'] + '. ' + doc['abstract']).lower())
    return rep_doc_list


def read_voc_list():
    with open(VOC_FILE_PATH, "r", encoding="utf-8") as file:
        voc_list = [i.strip().lower() for i in file.readlines()]
    return list(set(voc_list))


def calc_idf_list(doc_list, voc_list):
    idf_list = []
    for voc in voc_list:
        counter = 1
        for doc in doc_list:
            if voc in doc:
                counter += 1
        idf_list.append(math.log10(REP_DOC_NUM / counter))
    return idf_list
    #return [math.log10(REP_DOC_NUM / (1 + len([1 for doc in doc_list if voc in doc]))) for voc in voc_list]


def calc_vec_list(doc_list, voc_list, idf_list):
    vec_list = []
    for doc in doc_list:
        vec = []
        for idx, voc in enumerate(voc_list):
            vec.append(doc.count(voc) * idf_list[idx])
        vec_list.append(vec)
    return vec_list
    #return [[doc.count(voc) * idf_list[idx] for idx, voc in enumerate(voc_list)] for doc in doc_list]


def eu_dist_vec_to_vec(v1, v2):
    return math.sqrt(sum([(v1[i] - v2[i])**2 for i in range(len(v1))]))


def cos_dist_vec_to_vec(v1, v2):
    norm_v1 = math.sqrt(sum([(v1[i])**2 for i in range(len(v1))]))
    norm_v2 = math.sqrt(sum([(v2[i])**2 for i in range(len(v1))]))
    if norm_v1 * norm_v2 > 0:
        return 1 - sum([v1[i] * v2[i] for i in range(len(v1))]) / (norm_v1 * norm_v2)
    else:
        return 1


def dist_vec_to_set(v, s, dist_mat):
    return sum([dist_mat[v][e] for e in s]) / len(s)


def cluster_vec(vec_list):
    classifying = [i for i in range(len(vec_list))]
    classes = [[] for i in range(CLASS_NUM)]
    dist_mat = [[0 for j in range(len(vec_list))] for i in range(len(vec_list))]
    max_dist = 0
    c1, c2 = 0, 0
    for i in range(len(vec_list) - 1):
        for j in range(i + 1, len(vec_list)):
            dist = eu_dist_vec_to_vec(vec_list[i], vec_list[j])
            dist_mat[i][j] = dist_mat[j][i] = dist
            if dist > max_dist:
                c1, c2 = i, j
    classes[0].append(c1)
    classes[1].append(c2)
    classifying.pop(classifying.index(c1))
    classifying.pop(classifying.index(c2))
    for i in range(2, len(classes)):
        min_dist_list = [0 for j in range(len(vec_list))]
        for j in classifying:
            min_dist_list[j] = min([dist_vec_to_set(j, k, dist_mat) for k in classes[:i]])
        new_center = min_dist_list.index(max(min_dist_list))
        classes[i].append(new_center)
        classifying.pop(classifying.index(new_center))
    for i in classifying:
        min_dist_list = [dist_vec_to_set(i, k, dist_mat) for k in classes]
        min_dist_class = min_dist_list.index(min(min_dist_list))
        classes[min_dist_class].append(i)
    return classes


def cos_classify(vec, classes, vec_list):
    ave_dist_list = []
    for i in classes:
        ave_dist = sum([cos_dist_vec_to_vec(vec, vec_list[j]) for j in i]) / len(i)
        ave_dist_list.append(ave_dist)
    return ave_dist_list.index(min(ave_dist_list))


if __name__ == '__main__':
    doc_list = read_doc_list()
    voc_list = read_voc_list()
    idf_list = calc_idf_list(doc_list, voc_list)
    vec_list = calc_vec_list(doc_list, voc_list, idf_list)
    classes = cluster_vec(vec_list)
    class_names = []
    for i in classes:
        class_vec = [0 for j in range(len(voc_list))]
        for j in i:
            for k, v in enumerate(vec_list[j]):
                class_vec[k] += v
        class_name = voc_list[class_vec.index(max(class_vec))]
        class_vec[class_vec.index(max(class_vec))] = 0
        class_name += (' and ' + voc_list[class_vec.index(max(class_vec))])
        class_names.append(class_name)
    for class_name in class_names:
        print(class_name)

    connector = pymysql.connect("rm-bp1uk5g6qxw3mqpeevo.mysql.rds.aliyuncs.com", "root", "Doc123456",
                                "DocRetrieval")
    cursor = connector.cursor()
    sql = 'select id, title, abstract from retrievalcore_document where flag=2'
    cursor.execute(sql)
    docs = cursor.fetchall()
    for i in docs:
        vec = []
        doc = (i[1] + '. ' + i[2]).lower()
        for k, v in enumerate(voc_list):
            vec.append(doc.count(v) * idf_list[k])
        vec_class = cos_classify(vec, classes, vec_list)
        sql = 'update retrievalcore_document set classification=%d where id=%s'% (vec_class, i[0])
        cursor.execute(sql)
    connector.commit()
    cursor.close()
    connector.close()

#female 0 6000
# pregnancy and ert
# dysmenorrhea and menstruation
# sterilization and delivery
# preterm labor and ectopic pregnancy
# menopause and premature menopause
#male 1 3000
# std and sex
# prostate cancer and sex
# infertility and fertility
# vasectomy and family planning
# semen and infertility
#older 2 6000
# stroke and cataract
# mci and dementia
# tremor and essential tremor
# menopause and premature menopause
# prostate cancer and incontinence