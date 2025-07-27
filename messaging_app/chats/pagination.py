from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # Optional: client can set ?page_size=10
    max_page_size = 100
