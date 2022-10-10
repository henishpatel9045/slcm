from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class PaginatorSerializer(ModelViewSet):
    def list(self, request):
        page_size = int(self.request.GET.get("page_size", 20))
        page_number = int(self.request.GET.get("page_number", 1))
        
        if page_size < 1:
            page_size = 1
        
        if page_number < 1:
            page_number = 1
        
        start = (page_number-1) * page_size
        end = page_size * page_number
        
        queryset = self.filter_queryset(self.get_queryset()[start:end])
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
