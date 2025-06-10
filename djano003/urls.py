
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/products/', permanent=True)), # Redirect root to product list
    path('', include('products.urls',namespace='products')), # Include app URLs
]


'''
RedirectView: 这是一个专门用于执行重定向的视图类。
url='/products/': 这是 RedirectView 的一个参数，它指定了重定向的目标 URL。这意味着当用户访问根 URL 时，他们会被重定向到 http://yourwebsite.com/products/。
permanent=True: 表示执行一个 301 永久重定向（Moved Permanently）。
优点: 对 SEO（搜索引擎优化）非常有利，它告诉搜索引擎这个页面的内容已经永久性地移动到新地址了，搜索引擎会更新其索引，并将原页面的 PageRank（权重）传递给新页面。
缺点: 浏览器和搜索引擎会缓存这种重定向，如果你以后想更改这个重定向，可能会遇到缓存问题，需要清除浏览器缓存才能看到变化。
permanent=False (默认值): 表示执行一个 302 临时重定向（Found）。
优点: 浏览器和搜索引擎不会缓存这种重定向，更适合临时的重定向。
缺点: 对 SEO 不利，搜索引擎可能不会传递 PageRank。
'''