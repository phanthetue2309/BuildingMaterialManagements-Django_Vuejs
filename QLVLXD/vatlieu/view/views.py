from abc import ABC

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import *
from ..models import *

# Create your views here.


def home(request):
    return render(request, 'vatlieu/home.html')


# list view
class InputBillListView(PermissionRequiredMixin, ListView):
    permission_required = 'vatlieu.view_inputbill'
    model = InputBill
    template_name = 'vatlieu/list/list_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
        return redirect('vatlieu-home')


class OutputBillListView(PermissionRequiredMixin, ListView):
    permission_required = 'vatlieu.view_outputbill'
    model = OutputBill
    template_name = 'vatlieu/list/list_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'
    ordering = ['-output_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
        return redirect('vatlieu-home')


class UserInputBillListView(ListView):
    model = InputBill
    template_name = 'vatlieu/staff/staff_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'  # using in template
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return InputBill.objects.filter(staff=user).order_by('-input_date')


class UserOutputBillListView(ListView):
    model = OutputBill
    template_name = 'vatlieu/staff/staff_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'  # using in template
    ordering = ['-output_date']
    paginate_by = 5  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return OutputBill.objects.filter(staff=user).order_by('-output_date')


class ProviderListView(ListView):
    model = Provider
    template_name = 'vatlieu/list/list_provider.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'providers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang


class CustomerListView(ListView):
    model = Customer
    template_name = 'vatlieu/list/list_customer.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'customers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang


class ProductListView(ListView):
    model = Product
    template_name = 'vatlieu/list/list_product.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    ordering = ['type_product__name', 'name']
    paginate_by = 10  # Số lượng phân trang


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'vatlieu/warehouse/warehouse.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'warehouse'
    ordering = ['product__typeproduct__name', 'product__name']
    paginate_by = 10  # Số lượng phân trang


# create view
class InputBillCreateView(LoginRequiredMixin, CreateView):
    model = InputBill
    fields = ['provider', 'input_date', 'flag']  # field must contains in models
    template_name = 'vatlieu/input_bill/input_bill_form.html'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class OutputBillCreateView(LoginRequiredMixin, CreateView):
    model = OutputBill
    fields = ['customer', 'output_date', 'flag']  # field must contains in models
    template_name = 'vatlieu/output_bill/output_bill_form.html'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProviderCreateView(LoginRequiredMixin, CreateView):
    model = Provider
    fields = ['name', 'address', 'phone_number']
    template_name = 'vatlieu/provider/provider_form.html'
    success_url = "/list/provider"


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer    
    fields = ['name', 'address', 'phone_number', 'discription']
    template_name = 'vatlieu/customer/customer_form.html'
    success_url = "/list/customer"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['type_product', 'name', 'calculationUnit', 'unit_cost', 'selling_price', 'origin']
    template_name = 'vatlieu/product/product_form.html'

    # def add new product in wwarehouse with count = 0 
    def get_success_url(self):
        warehouse = Warehouse(product=self.object)
        warehouse.save()
        return self.object.get_absolute_url()


# inline type
@login_required(login_url='login')
def create_detail_inputbill(request, pk):
    detail_input_bill_formset = inlineformset_factory(InputBill, DetailInputBill,
                                                      fields=('product', 'count'), extra=10)
    # why use input_bill and detail_input because it has been created before now we need to
    # insert more than product in the input bill so we choice inlineformset like that
    input_bill = InputBill.objects.get(id=pk)
    formset = detail_input_bill_formset(queryset=DetailInputBill.objects.none(), instance=input_bill)
    if request.method == 'POST':
        formset = detail_input_bill_formset(request.POST, instance=input_bill)
        if formset.is_valid():
            for f in formset:
                # it run all for even not data in that so you have to make try catch to
                # remove the data not has enough data you need
                cd = f.cleaned_data
                product_name = cd.get('product')
                count = cd.get('count')
                # update data in warehouse
                try:
                    warehouse = Warehouse.objects.get(product__name=product_name)
                except Warehouse.DoesNotExist:
                    warehouse = None
                if warehouse is not None:
                    print(warehouse.product)
                    warehouse.count += count
                    warehouse.save()

            formset.save()
            return redirect('/list/input_bill')

    context = {'form': formset}
    return render(request, 'vatlieu/input_bill/detail_input_bill/input_bill_detail_form.html', context)


@login_required(login_url='login')
def create_detail_outputbill(request, pk):
    detail_output_bill_formset = inlineformset_factory(OutputBill, DetailOutputBill,
                                                       fields=('warehouse', 'count'), extra=10)
    # why use input_bill and detail_input because it has been created before now we need to
    # insert more than product in the input bill so we choice inlineformset like that
    output_bill = OutputBill.objects.get(id=pk)
    formset = detail_output_bill_formset(queryset=DetailOutputBill.objects.none(), instance=output_bill)
    if request.method == 'POST':
        formset = detail_output_bill_formset(request.POST, instance=output_bill)
        if formset.is_valid():
            for f in formset:
                # it run all for even not data in that so you have to make try catch to
                # remove the data not has enough data you need
                cd = f.cleaned_data
                warehouse_name = cd.get('warehouse')
                count = cd.get('count')
                # update data in warehouse
                try:
                    warehouse = Warehouse.objects.get(product__name=warehouse_name)
                except Warehouse.DoesNotExist:
                    warehouse = None
                if warehouse is not None:
                    warehouse.count -= count
                    warehouse.save()
                    print(warehouse.count)

            formset.save()
            return redirect('/list/output_bill')

    context = {'form': formset}
    return render(request, 'vatlieu/output_bill/detail_output_bill/output_bill_detail_form.html', context)


# update view
class InputBillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = InputBill
    fields = ['provider', 'input_date', 'flag']
    template_name = 'vatlieu/input_bill/input_bill_form.html'
    success_url = '/list/input_bill'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class OutputBillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = OutputBill
    fields = ['customer', 'output_date', 'flag']
    template_name = 'vatlieu/output_bill/output_bill_form.html'
    success_url = '/list/output_bill'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class ProviderUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Provider
    success_url = '/list/provider'
    fields = ['name', 'address', 'phone_number']
    template_name = 'vatlieu/provider/provider_form.html'


class CustomerUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Customer
    success_url = '/list/customer'
    fields = ['name', 'address', 'phone_number']
    template_name = 'vatlieu/customer/customer_form.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Product
    success_url = '/list/product'
    fields = ['type_product', 'name','calculationUnit', 'unit_cost', 'selling_price','origin']
    template_name = 'vatlieu/product/product_form.html'


class DetailInputUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = DetailInputBill
    fields = ['product', 'count']
    template_name = 'vatlieu/input_bill/detail_input_bill/detail_bill_update.html'
    old_data = []

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)  # use to get pk of objects
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product  # get data in the form when log in
        context['count'] = self.object.count
        self.old_data.clear()  
        # keep old data
        self.old_data.append(context['product'])
        self.old_data.append(context['count'])
        return context

    def get_success_url(self):
        print(self.old_data)
        if self.old_data[0].name == self.object.product.name:
            warehouse = Warehouse.objects.get(product__name=self.object.product.name)
            warehouse.count -= self.old_data[1]
            warehouse.count += self.object.count
            warehouse.save()
        else:
            warehouse = Warehouse.objects.get(product__name=self.old_data[0].name)
            warehouse.count -= self.old_data[1]
            warehouse.save()
            warehouse_new = Warehouse.objects.get(product__name=self.object.product.name)
            warehouse_new.count += self.object.count
            warehouse_new.save()
        return self.object.get_update_return()


class DetailOutputUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = DetailOutputBill
    fields = ['warehouse', 'count']
    template_name = 'vatlieu/output_bill/detail_output_bill/detail_bill_update.html'
    old_data = []

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)  # use to get pk of objects
        context = super().get_context_data(**kwargs)
        context['warehouse'] = self.object.warehouse.product.name  # get data in the form when log in
        context['count'] = self.object.count
        self.old_data.clear()  # keep old data
        self.old_data.append(context['warehouse'])
        self.old_data.append(context['count'])
        return context

    def get_success_url(self):
        print(self.old_data)
        if self.old_data[0] == self.object.warehouse.product.name:
            warehouse = Warehouse.objects.get(product__name=self.object.warehouse.product.name)
            warehouse.count += self.old_data[1]
            warehouse.count -= self.object.count
            warehouse.save()
        else:
            warehouse = Warehouse.objects.get(product__name=self.old_data[0])
            warehouse.count += self.old_data[1]
            warehouse.save()
            warehouse_new = Warehouse.objects.get(product__name=self.object.warehouse.product.name)
            warehouse_new.count -= self.object.count
            warehouse_new.save()
        return self.object.get_update_return()


# delete view
class InputBillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, ABC):
    model = InputBill
    success_url = '/list/input_bill'
    template_name = 'vatlieu/input_bill/input_bill_confirm_delete.html'

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class OutputBillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, ABC):
    model = OutputBill
    success_url = '/list/output_bill'
    template_name = 'vatlieu/output_bill/output_bill_confirm_delete.html'

    def test_func(self):
        output_bill = self.get_object()
        if self.request.user == output_bill.staff:
            return True
        return False


class ProviderDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Provider
    success_url = '/list/provider'
    template_name = 'vatlieu/provider/provider_confirm_delete.html'


class CustomerDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Customer
    success_url = '/list/customer'
    template_name = 'vatlieu/customer/customer_confirm_delete.html'


class ProductDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Product
    success_url = '/list/product'
    template_name = 'vatlieu/product/product_confirm_delete.html'


class DetailInputDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = DetailInputBill
    template_name = 'vatlieu/input_bill/detail_input_bill/detail_bill_delete.html'

    def get_success_url(self):
        return self.object.get_update_return()


class DetailOutputDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = DetailOutputBill
    template_name = 'vatlieu/output_bill/detail_output_bill/detail_bill_delete.html'

    def get_success_url(self):
        return self.object.get_update_return()


# detail view
class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'vatlieu/provider/provider_detail.html'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'vatlieu/customer/customer_detail.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'vatlieu/product/product_detail.html'


# detail of bill
def all_detail_input_bill(request, pk):
    sum_price = 0
    status = "UnDeal"
    input_bill = InputBill.objects.get(id=pk)
    if input_bill.flag == 1:
        status = "Deal"
    input_bill_detail = DetailInputBill.objects.filter(input_bill__id=pk)
    for bill in input_bill_detail:
        bill.price = bill.product.unit_cost * bill.count
        sum_price += bill.price
    context = {
        'input_bill': input_bill,
        'input_bills_detail': input_bill_detail,
        'sum': sum_price,
        'status': status
    }
    # truyền vào các giá trị khác như bình thường, lưu ý phải có lưu dữ liệu ở phía trước
    return render(request, 'vatlieu/input_bill/input_bill_detail.html', context)


def all_detail_output_bill(request, pk):
    sum_price = 0
    status = "UnDeal"
    output_bill = OutputBill.objects.get(id=pk)
    if output_bill.flag == 1:
        status = "Deal"
    output_bill_detail = DetailOutputBill.objects.filter(output_bill__id=pk)
    for bill in output_bill_detail:
        bill.price = bill.warehouse.product.selling_price * bill.count
        sum_price += bill.price
    context = {
        'output_bill': output_bill,
        'output_bills_detail': output_bill_detail,
        'sum': sum_price,
        'status': status
    }
    # truyền vào các giá trị khác như bình thường, lưu ý phải có lưu dữ liệu ở phía trước
    return render(request, 'vatlieu/output_bill/output_bill_detail.html', context)


# list page
def list_new(request):
    return render(request, 'vatlieu/list/list_new.html')


def list_all(request):
    return render(request, 'vatlieu/list/list_all.html')


def about(request):
    return render(request, 'vatlieu/list/about.html')


def search(request):  # xây dựng hàm search
    template = 'vatlieu/search.html'
    query = request.GET.get('q')
    result = Product.objects.filter(Q(name__icontains=query) | Q(selling_price__icontains=query)
             | Q(type_product__name__icontains=query)).order_by('type_product__name', 'name' )
    paginate_by = 10
    # filter theo 3 mức 
    # type_product__name__icontains là truy cập thông qua type_product thuộc tính name 
    # mức độ sắp xếp theo thứ tự từ trái qua phải đầu tiên xếp theo type_product name sau đó sắp xếp theo name
   
    context = {'products': result,
               'query_string': query,
               'count': len(result),
               }
    return render(request, template, context)


def customer_shopping(request):
    template = "vatlieu/customer/customer_shopping.html"
    warehouses = Warehouse.objects.all().order_by('-product__type_product__name', 'product__name')   # sắp xếp theo danh sách sản phẩm 
    context = {'warehouses': warehouses,
               }
    return render(request, template, context)


def buy_products(request):
    id_product = request.POST.get('id_product')
    count = request.POST.get('quantity')
    product = Product.objects.get(id=id_product)
    shopping = Shopping( product=product, staff=request.user, count=count,
                         total_cost=int(product.selling_price*int(count)), buying_unit_cost=int(product.selling_price))
    
    shopping.save()
    warehouse = Warehouse.objects.get(product__name = product.name)
    warehouse.count -= int(count)
    warehouse.save()

    # tesst 
    # print(request.user)
    # print(warehouse.count)
    # print(shopping)
    
    return redirect("customer-shopping")


class UserShopping_Buying(ListView):    # danh sách hóa đơn đặt mua 
    model = Shopping
    template_name = 'vatlieu/customer/customer_buying.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'shoppings'  # using in template
    ordering = ['-buy_date']
    paginate_by = 9  # Số lượng phân trang
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #print(user)
        return Shopping.objects.filter(staff=user).filter(flag=1).order_by('-buy_date')


class UserShopping_Received(ListView): # danh sách hóa đơn đã nhận hàng
    model = Shopping
    template_name = 'vatlieu/customer/customer_received.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'shoppings'  # using in template
    ordering = ['-buy_date']
    paginate_by = 9  # Số lượng phân trang
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Shopping.objects.filter(staff=user).filter(flag=-1).order_by('-buy_date')


def List_typeProduct(request, type_product):
    template = "vatlieu/product/list_type_product.html"
    products = Product.objects.filter(type_product__name = type_product).order_by('name')
    context = {'products': products,
               }
    return render(request, template, context)


def CustomerReceiveBuying(request, username, pk): # change flag of shopping
    shopping = Shopping.objects.get(id = pk)
    shopping.flag = -1 # thay đổi trạng thái từ đang mua thành đã nhận  
    shopping.save()

    return redirect("customer-buying" , username=username)
    