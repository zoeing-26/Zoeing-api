from django.shortcuts import render
from v1.models import Materials,SubCategory,Brand,Category
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from v1.serializers.material_serializer import BrandSerializer,CategorySerializer,EnquirySerializer
from v1.constants import SUCCESS_RESPONSE,ERROR_RESPONSE
from rest_framework import status
import configs as cfg
from v1.services.send_order_confirmation import send_order_confirmation_email,receive_order_confirmation_mail
from v1.common.response import success_response,error_response



class EnquiryView(viewsets.ViewSet):
        
    def post(self,request):

        data = request.data        
        serializer = EnquirySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # material_list = data['materials']
            # formatted_list = '\n'.join([
            #     f" - {item['name']} : {item['quantity']}"
            #     for item in material_list
            # ])

            mail_sent = send_order_confirmation_email(data)
            receive_mail = receive_order_confirmation_mail(data)
            
            return success_response(message=SUCCESS_RESPONSE,status_code=status.HTTP_200_OK)
        
        return error_response(message=ERROR_RESPONSE,status_code=status.HTTP_400_BAD_REQUEST)
        
class MaterialView(viewsets.ViewSet): 
     
    def get(self,request):
                
        products = Category.objects.prefetch_related('sub_category__materials').all()
        serializer = CategorySerializer(products,many=True,context={'request':request})
    
        if serializer:
            return success_response(message=SUCCESS_RESPONSE,data=serializer.data,status_code=status.HTTP_200_OK)
        return error_response(message=ERROR_RESPONSE,status_code=status.HTTP_400_BAD_REQUEST)
    
    
    def brand_list(self,request):
        
        brands = Brand.objects.prefetch_related('materials').all()
        
        serializer = BrandSerializer(brands,many=True,context={'request': request})
        
        if serializer:
            return success_response(message=SUCCESS_RESPONSE,data=serializer.data,status_code=status.HTTP_200_OK)
        
        return error_response(message=ERROR_RESPONSE,status_code=status.HTTP_400_BAD_REQUEST)
    
    
    def get_all_materials(self,request):
                
        all_materials = Materials.objects.select_related('category', 'brand', 'sub_category').all()
        
        response = []
        
        for material in all_materials:
            
            attachments = []

            for i in range(1, 5):
                file_field = getattr(material, f'attachment_{i}', None)

                if file_field:
                    file_url = request.build_absolute_uri(file_field.url)
                    file_name = file_field.name.split('/')[-1]

                    attachments.append({
                        'name' :file_name,
                        'file':file_url
                    })
            
            data = {
                'id': material.id,
                'name':material.name,
                'description' :material.description,
                'count': material.count,
                'price': material.price,
                'product_code': material.product_code,
                'image': request.build_absolute_uri(material.image.url) if material.image else None,
                'industry': material.industry,
                'category': material.category.name if material.category else None,
                'brand': material.brand.name if material.brand else None,
                'sub_category': material.sub_category.name if material.sub_category else None,
                'attachment' :  attachments  
                                      
            }
            response.append(data)
            
        if response:
            return success_response(message=SUCCESS_RESPONSE,data=response,status_code=status.HTTP_200_OK)
        
        return error_response(message=ERROR_RESPONSE,status_code=status.HTTP_404_NOT_FOUND)
        
    
    
    
        