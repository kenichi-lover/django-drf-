
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    # related_name 用于在 Django 模型的 ForeignKey 或 ManyToManyField 定义中进行设置。它的作用就是设定反向管理器的名称。
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "产品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


'''
在 Django 中,当你定义一个外键(ForeignKey)或多对多字段(ManyToManyField)时，你会从“多”的一方指向“一”的一方（或者从一方指向多方）
默认情况下： Django 会自动为你创建一个反向管理器，其名称通常是小写模型名加上 _set 后缀。
使用 related_name 时： 你可以使用 related_name 参数来自定义这个反向管理器的名称，使其更具描述性或避免命名冲突。
如上面模型：
1. 获取 'python' 这个分类对象
python_category = Category.objects.get(name='python')
2. 使用反向管理器查询该分类下的所有产品。 这里的 'product_set' 是 Django 自动生成的,若没有设置related_name参数。
python_products = python_category.product_set.all()    要改为:python_products = python_category.products.all()
3.输出所有产品
python_products
'''