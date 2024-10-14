import os
import re
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import two_d_cover
from .serializer import two_d_cover_serializers

# Custom exception for cover not found
class CoverNotFound(Exception):
    pass

# GET all covers
@api_view(['GET'])
def get_cover(request):
    covers = two_d_cover.objects.all()
    serializer = two_d_cover_serializers(covers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Helper function to format the file name
def format_template_name(original_name):
    # Remove the file extension
    name, ext = os.path.splitext(original_name)
    
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    
    # Remove special characters, keeping only alphanumeric characters and underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)

    # Return the formatted name with the original extension
    return f"{name}{ext}"

# POST add a new cover
@api_view(['POST'])
def add_cover(request):
    # Check if a file is uploaded
    if 'cover_template' not in request.FILES:
        return Response({
            'message': 'No cover template file provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get the file from the request
    cover_template_file = request.FILES['cover_template']
    
    # Format the cover template name
    formatted_name = format_template_name(cover_template_file.name)
    
    # Define the save path
    save_path = os.path.join(settings.BASE_DIR, 'cover_one/static/cover_templates', formatted_name)
    
    # Save the file
    with open(save_path, 'wb+') as destination:
        for chunk in cover_template_file.chunks():
            destination.write(chunk)
    
    # Create a new cover instance with the formatted file name as the cover_template
    cover_data = {
        'cover_model': request.data.get('cover_model'),
        'cover_template': formatted_name,  # Store the formatted file name in the DB
    }
    
    serializer = two_d_cover_serializers(data=cover_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Cover created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'message': 'Failed to create cover',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# PUT update a cover
@api_view(['PUT'])
def update_cover(request, pk):
    cover = get_object_or_404(two_d_cover, pk=pk)  # Fetch the specific cover by ID (primary key)

    # Create a dictionary of the data to update, starting with existing data
    updated_data = {
        'cover_model': request.data.get('cover_model', cover.cover_model),  # Use existing value if not provided
        'cover_template': cover.cover_template  # Keep the current template file name unless updated
    }

    # Check if a new file is uploaded
    if 'cover_template' in request.FILES:
        cover_template_file = request.FILES['cover_template']

        # Format the cover template name
        formatted_name = format_template_name(cover_template_file.name)

        # Define the save path for the new file
        save_path = os.path.join(settings.BASE_DIR, 'cover_one/static/cover_templates', formatted_name)

        # Save the new file
        with open(save_path, 'wb+') as destination:
            for chunk in cover_template_file.chunks():
                destination.write(chunk)

        # Update the file name in the cover data
        updated_data['cover_template'] = formatted_name  # Use the formatted name

    # Serialize the data with the updated fields
    serializer = two_d_cover_serializers(cover, data=updated_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Cover updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'message': 'Failed to update cover',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# DELETE a cover
@api_view(['DELETE'])
def delete_cover(request, pk):
    cover = get_object_or_404(two_d_cover, pk=pk)  # Fetch the specific cover by ID (primary key)
    cover.delete()
    return Response({'message': 'Cover deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
