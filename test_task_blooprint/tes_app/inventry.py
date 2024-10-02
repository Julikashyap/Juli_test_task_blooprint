from rest_framework import viewsets
from .models import Category, Product, Stock
from .serialization import CategorySerializer, ProductSerializer, StockSerializer
import logging
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    # List all categories
    @swagger_auto_schema(tags=['Inventry Category'])
    def list(self, request, *args, **kwargs):
        try:
            cached_categories = cache.get('categories')
            if cached_categories:
                logger.info("Returning cached categories")
                return Response(cached_categories)

            response = super().list(request, *args, **kwargs)
            cache.set('categories', response.data, timeout=60 * 15)  # Cache for 15 minutes
            logger.info("Caching category list")
            return response
        except Exception as e:
            logger.error(f"Error fetching category list: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Retrieve a single category
    @swagger_auto_schema(tags=['Inventry Category'])
    def retrieve(self, request, *args, **kwargs):
        try:
            category_id = kwargs.get('pk')
            cached_category = cache.get(f'category_{category_id}')
            if cached_category:
                logger.info(f"Returning cached category with ID {category_id}")
                return Response(cached_category)

            response = super().retrieve(request, *args, **kwargs)
            cache.set(f'category_{category_id}', response.data, timeout=60 * 15)
            logger.info(f"Caching category with ID {category_id}")
            return response
        except Exception as e:
            logger.error(f"Error fetching category with ID {category_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create a new category
    @swagger_auto_schema(tags=['Inventry Category'])
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            cache.delete('categories')  # Invalidate cached category list after creation
            logger.info("Category created and cache invalidated for category list")
            return response
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update a category
    @swagger_auto_schema(tags=['Inventry Category'])
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            category_id = kwargs.get('pk')
            cache.delete(f'category_{category_id}')  # Invalidate cached category
            cache.delete('categories')  # Invalidate category list cache
            logger.info(f"Category with ID {category_id} updated and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error updating category with ID {category_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete a category
    @swagger_auto_schema(tags=['Inventry Category'])
    def destroy(self, request, *args, **kwargs):
        try:
            category_id = kwargs.get('pk')
            response = super().destroy(request, *args, **kwargs)
            cache.delete(f'category_{category_id}')  # Invalidate cached category
            cache.delete('categories')  # Invalidate category list cache
            logger.info(f"Category with ID {category_id} deleted and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error deleting category with ID {category_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(tags=['Inventry Item'])
    def list(self, request, *args, **kwargs):
        try:
            cached_products = cache.get('products')
            if cached_products:
                return Response(cached_products)

            response = super().list(request, *args, **kwargs)
            cache.set('products', response.data, timeout=60 * 15)
            return response
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(tags=['Inventry Item'])
    def retrieve(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get('pk')
            cached_product = cache.get(f'product_{product_id}')
            if cached_product:
                logger.info(f"Returning cached product with ID {product_id}")
                return Response(cached_product)

            response = super().retrieve(request, *args, **kwargs)
            cache.set(f'product_{product_id}', response.data, timeout=60 * 15)
            logger.info(f"Caching product with ID {product_id}")
            return response
        except Exception as e:
            logger.error(f"Error fetching product with ID {kwargs.get('pk')}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create a new product
    @swagger_auto_schema(tags=['Inventry Item'])
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            cache.delete('products')  # Invalidate cached product list after creation
            logger.info("Product created and cache invalidated for product list")
            return response
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update a product
    @swagger_auto_schema(tags=['Inventry Item'])
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            product_id = kwargs.get('pk')
            cache.delete(f'product_{product_id}')  # Invalidate cached product
            cache.delete('products')  # Invalidate product list cache
            logger.info(f"Product with ID {product_id} updated and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error updating product with ID {kwargs.get('pk')}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete a product
    @swagger_auto_schema(tags=['Inventry Item'])
    def destroy(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get('pk')
            response = super().destroy(request, *args, **kwargs)
            cache.delete(f'product_{product_id}')  # Invalidate cached product
            cache.delete('products')  # Invalidate product list cache
            logger.info(f"Product with ID {product_id} deleted and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error deleting product with ID {kwargs.get('pk')}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    # List all stock items
    @swagger_auto_schema(tags=['Inventry Stock'])
    def list(self, request, *args, **kwargs):
        try:
            cached_stock = cache.get('stock')
            if cached_stock:
                logger.info("Returning cached stock list")
                return Response(cached_stock)

            response = super().list(request, *args, **kwargs)
            cache.set('stock', response.data, timeout=60 * 15)  # Cache for 15 minutes
            logger.info("Caching stock list")
            return response
        except Exception as e:
            logger.error(f"Error fetching stock list: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Retrieve a single stock item
    @swagger_auto_schema(tags=['Inventry Stock'])
    def retrieve(self, request, *args, **kwargs):
        try:
            stock_id = kwargs.get('pk')
            cached_stock_item = cache.get(f'stock_{stock_id}')
            if cached_stock_item:
                logger.info(f"Returning cached stock item with ID {stock_id}")
                return Response(cached_stock_item)

            response = super().retrieve(request, *args, **kwargs)
            cache.set(f'stock_{stock_id}', response.data, timeout=60 * 15)
            logger.info(f"Caching stock item with ID {stock_id}")
            return response
        except Exception as e:
            logger.error(f"Error fetching stock item with ID {stock_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create a new stock entry
    @swagger_auto_schema(tags=['Inventry Stock'])
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            cache.delete('stock')  # Invalidate cached stock list after creation
            logger.info("Stock item created and cache invalidated for stock list")
            return response
        except Exception as e:
            logger.error(f"Error creating stock item: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update a stock entry
    @swagger_auto_schema(tags=['Inventry Stock'])
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            stock_id = kwargs.get('pk')
            cache.delete(f'stock_{stock_id}')  # Invalidate cached stock item
            cache.delete('stock')  # Invalidate stock list cache
            logger.info(f"Stock item with ID {stock_id} updated and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error updating stock item with ID {stock_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete a stock entry
    @swagger_auto_schema(tags=['Inventry Stock'])
    def destroy(self, request, *args, **kwargs):
        try:
            stock_id = kwargs.get('pk')
            response = super().destroy(request, *args, **kwargs)
            cache.delete(f'stock_{stock_id}')  # Invalidate cached stock item
            cache.delete('stock')  # Invalidate stock list cache
            logger.info(f"Stock item with ID {stock_id} deleted and cache invalidated")
            return response
        except Exception as e:
            logger.error(f"Error deleting stock item with ID {stock_id}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)