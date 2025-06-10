
from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_active': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 这行代码的作用是：确保 category 字段的下拉菜单选项包含了 Category 模型中的所有对象。 
        # 尽管 ModelForm 通常会自动处理这个，但有时你可能需要过滤这些选项（例如，只显示活跃的分类），
        # 那么你就可以在这里修改 queryset。在这里，它是明确地将其设置为所有 Category 对象。
        self.fields['category'].queryset = Category.objects.all()

        # Add Bootstrap classes for styling (optional)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
               isinstance(field.widget, forms.NumberInput) or \
               isinstance(field.widget, forms.Textarea) or \
               isinstance(field.widget, forms.Select):
                # field.widget.attrs.update({'class': 'form-control'}): 如果小部件属于这些类型，就为它添加 form-control 这个 Bootstrap 类。
                # 这个类通常会为输入框提供统一的样式，如宽度、边框、字体等。
                field.widget.attrs.update({'class': 'form-control'})
                
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})

'''
Model 是你数据的结构定义。Form 是处理用户输入的通用工具。ModelForm 则是连接 Model 和 Form 的桥梁，它极大地简化了基于模型的 CRUD 操作。

所以，模型不一定非要有模型表单。 但在绝大多数涉及到用户输入并需要将这些输入存储到数据库中的场景下，使用 ModelForm 是最方便、最推荐的方式，因为它能帮你节省大量的代码和精力。
'''