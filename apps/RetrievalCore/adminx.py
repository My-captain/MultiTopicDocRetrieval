import xadmin
from RetrievalCore.models import Document, UserProfile, Session, DVectorRecord


class DocumentAdmin(object):
    list_display = ["title", "publish_year", "authors", "abstract", "doi_url", "references", "publication",
                    "classification", "flag"]
    search_fields = ["title", "publish_year", "authors", "abstract", "doi_url", "references", "publication",
                     "classification", "flag"]
    list_filter = ["title", "publish_year", "authors", "abstract", "doi_url", "references", "publication",
                   "classification", "flag"]
    show_detail_fields = ["title", "publish_year", "authors", "abstract", "doi_url", "references", "publication",
                          "classification", "flag"]


class UserProfileAdmin(object):
    list_display = ["username", "D_vector_female", "P_vector_female", "D_vector_male", "P_vector_male", "D_vector_older", "P_vector_older"]
    search_fields = ["username", "D_vector_female", "P_vector_female", "D_vector_male", "P_vector_male", "D_vector_older", "P_vector_older"]
    list_filter = ["username", "D_vector_female", "P_vector_female", "D_vector_male", "P_vector_male", "D_vector_older", "P_vector_older"]
    show_detail_fields = ["username", "D_vector_female", "P_vector_female", "D_vector_male", "P_vector_male", "D_vector_older", "P_vector_older"]


class SessionAdmin(object):
    list_display = ["user", "documents", "D_vector", "P_vector", "precision", "default_precision"]
    search_fields = ["user", "documents", "D_vector", "P_vector", "precision", "default_precision"]
    list_filter = ["user", "documents", "D_vector", "P_vector", "precision", "default_precision"]
    show_detail_fields = ["user", "documents", "D_vector", "P_vector", "precision", "default_precision"]


class DVectorRecordAdmin(object):
    list_display = ["user", "user_D_vector", "sys_D_vector", "submit_time", "flag"]
    search_fields = ["user", "user_D_vector", "sys_D_vector", "submit_time", "flag"]
    list_filter = ["user", "user_D_vector", "sys_D_vector", "submit_time", "flag"]
    show_detail_fields = ["user", "user_D_vector", "sys_D_vector", "submit_time", "flag"]


xadmin.site.register(Document, DocumentAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(Session, SessionAdmin)
xadmin.site.register(DVectorRecord, DVectorRecordAdmin)

