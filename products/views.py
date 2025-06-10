# products/views.py
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView,DeleteView,UpdateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm # We'll create this form
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# DRF related imports
from rest_framework import viewsets

from .serializers import ProductSerializer, CategorySerializer

# --- Traditional Django Views (for rendering templates) ---

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'  # 指定在模板中使用的上下文变量名，默认为 object_list

    def get_context_data(self, **kwargs):
        """
        添加额外的上下文数据，例如表单。
        """
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()  # 将 ProductForm 添加到上下文
        return context

class ProductDetailView(DetailView):
    model = Product  # 指定要获取详情的模型
    template_name = 'products/product_detail.html'  # 指定模板文件的路径
    context_object_name = 'product'  # 指定在模板中使用的上下文变量名，默认为 object
    # DetailView 默认会查找 URL 中名为 'pk' 或 'slug' 的参数来获取对象。
    # 因为你的 URL 中使用了 <int:pk>，所以这里不需要额外重写 get_object 方法。
    # 它会自动执行 get_object_or_404(Product, pk=self.kwargs['pk'])



class ProductUpdateView(UpdateView):
    model = Product  # 指定要更新的模型
    form_class = ProductForm  # 指定要使用的表单类
    template_name = 'products/product_edit.html'  # 指定模板文件的路径
    context_object_name = 'product'  # 指定在模板中使用的上下文变量名，默认为 object

    # success_url 定义了表单成功提交后重定向到哪个 URL。
    # reverse_lazy 用于在 URL 配置加载之前构建 URL。
    # 这里假设你有一个名为 'product_detail' 的 URL 用于显示产品详情，
    # 并且该 URL 接收一个名为 'pk' 的参数。
    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})

    # UpdateView 默认会查找 URL 中名为 'pk' 或 'slug' 的参数来获取对象。
    # 它会自动处理 GET 请求（展示带有当前数据的表单）和 POST 请求（处理表单提交、验证和保存）。
    # 因此，你无需像函数视图那样手动 get_object_or_404 和实例化表单。
    # 在模板中，你可以使用 {{ form.as_p }} 来渲染表单。

class ProductDeleteView(DeleteView):
    model = Product # 指定要删除的模型
    # 删除成功后重定向到哪个 URL。reverse_lazy 是为了确保 URL 在 Django 启动时被解析，而不是在模块加载时。
    success_url = reverse_lazy('products:product_list')

    # 如果你确定想直接删除，可以在这里覆盖：
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)



# --- DRF ViewSets (for API endpoints) ---

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated] # 根据需要添加认证
    # 通常情况下，除了以上这三行，你无需写其他代码！
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read for all, write for authenticated
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']

    # 为 SearchFilter 指定可以通过哪些字段进行搜索（例如 ?search=iphone 会在 name 和 description 中搜索）。
    search_fields = ['name', 'description']

    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']  # Default ordering

    # 这是一个自定义的 list action。它会创建一个新的 URL 路径（例如 /products/featured/）。
    # 当用户访问这个 URL 时，它会执行 get 方法，返回一个包含所有 featured 产品的序列化数据。
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        featured_products = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    # detail=True 表示它操作的是单个实例，需要通过 pk（主键）来指定产品。
    # 当用户访问 /products/1/toggle_featured/ 时，它会执行 post 方法，切换该产品的 featured 状态。
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        """Toggle featured status of a product"""
        product = self.get_object()
        product.is_featured = not getattr(product, 'is_featured', False)
        product.save()
        return Response({'status': 'featured status updated'})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in this category"""
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


'''
1.Permissions:IsAuthenticatedOrReadOnly 允许任何人进行读取操作，但要求进行身份验证才能进行修改操作。
2.Search:新增了按类别和价格筛选商品的功能支持。
3.Filtering:新增了按类别和价格筛选商品的功能支持。
4.Ordering:新增了按名称、价格和创建日期排序商品的功能支持。
5.Custom Actions:
- featured: 获取所有特色商品。
- toggle_featured: 切换商品的特色状态。

'''