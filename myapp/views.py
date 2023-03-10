from django.shortcuts import render, HttpResponse, redirect,reverse
from .models import *
import pandas as pd
import datetime
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.views.decorators.cache import never_cache
# Create your views here.
# addmin crop data to main crop table
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_crop(request,pk):
    if request.method == 'POST':
        crop_name = request.POST['crop_name']
        crop_date = request.POST['crop_date']
        crop_notes = request.POST['crop_notes']
        location = request.POST['location']
        print(crop_notes)
        print(crop_date)
        print(crop_name)
        status='ongoing'
        a = main_crop.objects.create(crop_name=crop_name, crop_date=crop_date, crop_notes=crop_notes,location=location, user_id=pk, status=status)
        a.save()
        print("new crop created")
        messages.success(request,"New crop created")

    return render(request, 'new_crop.html')

@login_required(redirect_field_name='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crop_main_dashboard(request,pk):
    if request.user.is_authenticated:
        crop = main_crop.objects.filter(user_id=pk).filter(status='ongoing')
        try:
            crop1 = main_crop.objects.filter(user_id=pk).filter(status='completed')
        except:
            crop1=[]
        print(crop)
        for c in crop:
            print(c.crop_name)
        context = {
            'crops': crop,
            'crops1':crop1
        }
        return render(request, 'maindash.html', context=context)
    else:
        return redirect(user_login)

@login_required(redirect_field_name='userlogin')
def crop_sub_dashboard(request, pk):
    crop_id = pk
    crop = main_crop.objects.get(crop_id=crop_id)
    context = {
        'crops': crop
    }
    return render(request, 'backup templates/crop_sub_dashoard.html', context=context)

@login_required(redirect_field_name='userlogin')
def create_expense(request, pk):
    crop_id=pk
    if request.method == 'POST':
        exp_name = request.POST['exp_name']
        exp_cost = request.POST['exp_cost']
        exp_date = request.POST['exp_date']
        exp_paidto = request.POST['exp_paidto']
        exp_notes = request.POST['exp_notes']
        crop_id = int(pk)

        e = expenses.objects.create(crop_id=crop_id, exp_name=exp_name, exp_cost=exp_cost, exp_date=exp_date,
                                    exp_paidto=exp_paidto, exp_notes=exp_notes)
        e.save()
        print("new expense created")
        msg = "new expense added"
        messages.success(request, 'New expense added successfully!')
        return render(request, 'expense_add.html', {
            'crop_id': crop_id,
        })
    return render(request, 'expense_add.html',
                  {
        'crop_id': crop_id
    })

@login_required(redirect_field_name='userlogin')
def create_workerexp(request, pk):
    if request.method == 'POST':
        worker_name = request.POST['worker_name']
        date = request.POST['date']
        amount = request.POST['amount']
        worker_notes = request.POST['worker_notes']
        crop_id = pk

        w = worker.objects.create(worker_name=worker_name, date=date, amount=amount, worker_notes=worker_notes,
                                  crop_id=crop_id)
        w.save()
        print("new workers expense created")
        messages.success(request, 'New worker expense added successfully!')
        return render(request, 'workexp_add.html', {
            'crop_id': pk,
        })

    return render(request, 'workexp_add.html',{
        'crop_id': pk,
    })

@login_required(redirect_field_name='userlogin')
def create_feed(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        shop_name = request.POST['shop_name']
        bill_no = request.POST['bill_no']
        bill_amount = request.POST['bill_amount']
        feed_notes = request.POST['feed_notes']
        quantity = request.POST['quantity']
        type = request.POST['type']

        f = feed.objects.create(crop_id=crop_id, date=date, shop_name=shop_name, bill_no=bill_no,
                                bill_amount=bill_amount, feed_notes=feed_notes, quantity=quantity, type=type)
        f.save()
        print("new feed bill added")
        messages.success(request, 'New feed bill added successfully!')
        return render(request, 'feed_add.html', {'crop_id': pk})

    return render(request, 'feed_add.html', {'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_medicine(request, pk):
    if request.method == 'POST':
        crop_id = pk
        med_name = request.POST['med_name']
        date = request.POST['date']
        bill_no = request.POST['bill_no']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        med_notes = request.POST['med_notes']

        m = medicine.objects.create(crop_id=crop_id, med_name=med_name, date=date, bill_no=bill_no, quantity=quantity,
                                    amount=amount, med_notes=med_notes)
        m.save()
        print("new medicine added")
        messages.success(request, 'New medicine bill added successfully!')
        return render(request, 'medicine_add.html', {'crop_id': pk})

    return render(request, 'medicine_add.html',{'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_elebill(request, pk):
    if request.method == 'POST':
        crop_id = pk
        tranformer_type = request.POST['transformer_type']
        billed_date = request.POST['billed_date']
        start_read = request.POST['start_read']
        end_read = request.POST['end_read']
        bill_amount = request.POST['bill_amount']
        bill_notes = request.POST['bill_notes']

        print(crop_id)
        print(tranformer_type)
        print(billed_date)
        print(start_read)
        print(end_read)
        print(bill_amount)
        print(bill_notes)

        e = ele_bill.objects.create(crop_id=crop_id, tranformer_type=tranformer_type, billed_date=billed_date,
                                    start_read=start_read, end_read=end_read, bill_amount=bill_amount,
                                    bill_notes=bill_notes)
        e.save()
        print("new electrical bill added")
        messages.success(request, 'New electricity bill added successfully!')
        return render(request, 'elebill_add.html', {'crop_id': pk})

    return render(request, 'elebill_add.html', {'crop_id': pk})

@login_required(redirect_field_name='userlogin')
def create_export(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        tank_no = request.POST['tank_no']
        material_weight = request.POST['material_weight']
        count = request.POST['count']
        amount = request.POST['amount']
        exp_notes = request.POST['exp_notes']

        print(crop_id)
        print(date)
        print(tank_no)
        print(material_weight)
        print(count)
        print(amount)
        print(exp_notes)

        exp = export.objects.create(crop_id=crop_id, date=date, tank_no=tank_no, material_weight=material_weight,
                                    count=count, amount=amount, exp_notes=exp_notes)
        exp.save()
        print("new export record added")
        messages.success(request, 'New export details added successfully!')
        return render(request, 'export_add.html', {'crop_id': pk})

    return render(request, 'export_add.html', {'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_daily_feed(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        tank_no = request.POST['tank_no']
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        fourth = request.POST['fourth']

        print(crop_id)
        print(date)
        print(tank_no)
        print(first)
        print(second)
        print(third)
        print(fourth)

        cr = daily_feed.objects.create(crop_id=crop_id, date=date, tank_no=tank_no, first=first, second=second,
                                       third=third, fourth=fourth)
        cr.save()
        messages.success(request, 'daily feed added successfully!')
        context= {
            'cropid':pk
        }
        print("new daily feed added")
        return render(request, 'dailyfeed_add.html', {'crop_id': pk})

    return render(request, 'dailyfeed_add.html', {'crop_id': pk})

@login_required(redirect_field_name='userlogin')
def complete_view(request, pk):
    # first getting the crop details
    if request.user.is_authenticated:

        maincrop = main_crop.objects.filter(crop_id=pk)

        # getting the information from expenses table
        expense = expenses.objects.filter(crop_id=pk)

        # getting the information from workers expenses table
        work_exp = worker.objects.filter(crop_id=pk)

        # getting the information from feed table
        feed_view = feed.objects.filter(crop_id=pk)

        # getting the information from medicine table
        med = medicine.objects.filter(crop_id=pk)

        # getting the information from electrical bill
        ele = ele_bill.objects.filter(crop_id=pk)

        # getting the information from export
        expo = export.objects.filter(crop_id=pk)

        # getting the information from daily feed
        daily = daily_feed.objects.filter(crop_id=pk).order_by('date')

        print(maincrop)
        print(expense)
        print(work_exp)
        print(feed_view)
        print(med)
        print(ele)
        print(expo)
        print(daily)
        context = {
            'maincrop': maincrop,
            'expense': expense,
            'work_exp': work_exp,
            'feed_view': feed_view,
            'med': med,
            'ele': ele,
            'expo': expo,
            'daily': daily,
            'crop_id': pk

        }

        for a in expense:
            print(a.exp_name)
            print(a.exp_cost)
            print(a.exp_date)
        for b in feed_view:
            print(b.date)

        return render(request, 'tables.html', context=context)
    else:
        return redirect(user_login)


def insight(request, pk):
    # getting information from expenses
    a = expenses.objects.filter(crop_id=pk)
    j = []
    for i in a:
        j.append(i.exp_cost)
    print(sum(j))
    expense_sum = sum(j)
    print("the total expenses sum is", expense_sum)

    # getting information from worker expenses
    b = worker.objects.filter(crop_id=pk)
    work_exp = []
    for i in b:
        work_exp.append(i.amount)
    work_sum = sum(work_exp)
    print("the total worker expenses are ", work_sum)

    c = feed.objects.filter(crop_id=pk)
    feed_exp = []
    for i in c:
        feed_exp.append(i.bill_amount)
    feed_sum = sum(feed_exp)
    print("the total worker expenses are ", feed_sum)

    d = medicine.objects.filter(crop_id=pk)
    med = []
    for i in d:
        med.append(i.amount)
    med_sum = sum(med)
    print("the total worker expenses are ", med_sum)


    # getting the information from electrical bills
    e = ele_bill.objects.filter(crop_id=pk)
    ele = []
    for i in e:
        ele.append(i.bill_amount)
    ele_sum = sum(ele)
    print("the electrical bill sum is", ele_sum)

    # getting the information from export
    f = export.objects.filter(crop_id=pk)
    exp = []
    for i in f:
        exp.append(i.amount)
    export_sum = sum(exp)
    print("the export sum is", export_sum)

    # getting the information from daily feed
    #graph1 and graph 2
    graph1_labels = ['expenses', 'worker', 'electrical']
    graph1_data = [expense_sum, work_sum, ele_sum]
    total_data = sum(graph1_data)
    total_data+= feed_sum+med_sum
    graph2_labels = ['Total spent', 'Total received']
    graph2_data = [total_data,export_sum ]

    # graph3

    #getting information on daily feed
    x = daily_feed.objects.filter(crop_id=pk).filter(tank_no='A1')
    df = pd.DataFrame(list(x.values()))
    #a1_sum = df['first'].sum()
    #for A1
    #a1_df = df.query("tank_no == 'A1'")
    #print(df)
    df['total'] = df['first']+df['second'] + df['third'] + df['fourth']
    a1_total = df['total'].to_list()
    a1_label = df['date'].to_list()
    #print(a1_label, "a1 label")
    s=[]
    for i in a1_label:
        date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
        s.append(date_obj.strftime("%d-%B"))
    a1_label=s


    # a2 sum
    x = daily_feed.objects.filter(crop_id=pk).filter(tank_no='A2')
    df = pd.DataFrame(list(x.values()))
    a2_df = df.query("tank_no == 'A2'")
    a2_label = a2_df['date'].to_list()
    s1=[]
    for i in a2_label:
        date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
        s1.append(date_obj.strftime("%d-%B"))
    a2_label=s
    #print(s,"a2 label")
    a2_df['total'] = a2_df['first']+a2_df['second'] + a2_df['third'] + a2_df['fourth']
    a2_total = a2_df['total'].to_list()
    #print(a2_total)


    #b1 details
    x = daily_feed.objects.filter(crop_id=pk).filter(tank_no='B1')
    df = pd.DataFrame(list(x.values()))
    b1_df = df.query("tank_no == 'B1'")
    #print(b1_df)
    b1_df['total'] = b1_df['first']+b1_df['second'] + b1_df['third'] + b1_df['fourth']
    b1_total = b1_df['total'].to_list()
    b1_label = b1_df['date'].to_list()
    s2 = []
    for i in b1_label:
        date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
        s2.append(date_obj.strftime("%d-%B"))
    b1_label = s2
    #print(b1_label, "b1 label")
    #print(b1_total)


    # b2 details
    x = daily_feed.objects.filter(crop_id=pk).filter(tank_no='B2')
    df = pd.DataFrame(list(x.values()))
    b2_df = df.query("tank_no == 'B2'")
    b2_df['total'] = b2_df['first']+b2_df['second'] + b2_df['third'] + b2_df['fourth']
    b2_total = b2_df['total'].to_list()
    b2_label = b2_df['date'].to_list()
    s3 = []
    for i in b2_label:
        date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
        s3.append(date_obj.strftime("%d-%B"))
    b2_label = s3

    #graph 4:

    #export details:
    f = export.objects.filter(crop_id=pk).filter(tank_no='A1')
    a1_amount = []
    for a in f:
        a1_amount.append(a.amount)
    a1_amount = sum(a1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='A2')
    a2_amount = []
    for a in f:
        a2_amount.append(a.amount)
    a2_amount = sum(a2_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B1')
    b1_amount = []
    for p in f:
        b1_amount.append(int(p.amount))
    b1_amount_final = sum(b1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B2')
    b2_amount = []
    for a in f:
        b2_amount.append(a.amount)
    b2_amount = sum(b2_amount)

    graph4_label = ['A1','A2','B1', 'B2']
    graph_4_data = [a1_amount,a2_amount,b1_amount_final,b2_amount]

    #graph 5
    graph5_label = ['40Kv', '100Kv']
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='40kv')
    sum_40kv = []
    for i in e:
        sum_40kv.append(i.bill_amount)
    sum_40kv = sum(sum_40kv)
    sum_100kv = []
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='100kv')
    for i in e:
        sum_100kv.append(i.bill_amount)
    sum_100kv = sum(sum_100kv)
    graph5_data = [sum_40kv,sum_100kv]
    crop_id = pk
    crop = main_crop.objects.get(crop_id=crop_id)
    #info for matching daily feed totol with feed bills

    return render(request, 'backup templates/graphs.html', {
        'graph1_labels': graph1_labels,
        'graph1_data': graph1_data,
        'graph2_labels':graph2_labels,
        'graph2_data':graph2_data,
        'graph4_label':graph4_label,
        'graph4_data': graph_4_data,
        'graph5_label':graph5_label,
        'graph5_data': graph5_data,
        'a1_label':a1_label,
        'a1_total': a1_total,
        'a2_label': a2_label,
        'a2_total': a2_total,
        'b1_label': b1_label,
        'b1_total': b1_total,
        'b2_label': b2_label,
        'b2_total': b2_total,
        'crops':crop,


    })
@login_required(redirect_field_name='userlogin')
def graphs(request,pk):
    def get_label(a,pk,tank_no):
        x = a.objects.filter(crop_id=pk).filter(tank_no=tank_no).order_by('date')
        if x:
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            a1_total = df['total'].to_list()
            a1_label = df['date'].to_list()
            s = []
            for i in a1_label:
                date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
                s.append(date_obj.strftime("%d-%B"))
            a1_label = s
        else:
            a1_label='no data available'
            a1_total=[0]
        return a1_label,a1_total
    # a1 tank graph1
    graph1_labels, graph1_total = get_label(daily_feed,pk,'A1')
    print(len(graph1_total))
    print(len(graph1_labels))
    # a2 tank graph2
    graph2_labels, graph2_total = get_label(daily_feed,pk,'A2')

    # B1 tank graph3
    graph3_labels, graph3_total = get_label(daily_feed,pk,'B1')

    # B2 tank graph 4:
    graph4_labels, graph4_total = get_label(daily_feed,pk,'B2')

    total = sum(graph1_total)+sum(graph2_total)+sum(graph3_total)+sum(graph4_total)
    print('total sum is',total)
    #electricity transformer comparision - graph 5
    graph5_label = ['40Kv', '100Kv']
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='40kv')
    sum_40kv = []
    for i in e:
        sum_40kv.append(i.bill_amount)
    sum_40kv = sum(sum_40kv)
    sum_100kv = []
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='100kv')
    for i in e:
        sum_100kv.append(i.bill_amount)
    sum_100kv = sum(sum_100kv)
    graph5_total = [sum_40kv,sum_100kv]

    #export details:
    f = export.objects.filter(crop_id=pk).filter(tank_no='A1')
    a1_amount = []
    for a in f:
        a1_amount.append(a.amount)
    a1_amount = sum(a1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='A2')
    a2_amount = []
    for a in f:
        a2_amount.append(a.amount)
    a2_amount = sum(a2_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B1')
    b1_amount = []
    for p in f:
        b1_amount.append(int(p.amount))
    b1_amount_final = sum(b1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B2')
    b2_amount = []
    for a in f:
        b2_amount.append(a.amount)
    b2_amount = sum(b2_amount)

    graph6_label = ['A1', 'A2', 'B1', 'B2']
    graph6_data = [a1_amount,a2_amount,b1_amount_final,b2_amount]
    print(graph6_label)
    print(graph6_data)
    graph1_labels = graph1_labels[1:]
    graph1_total = graph1_total[1:]
    graph2_labels = graph2_labels[1:]
    graph2_total = graph2_total[1:]
    graph3_labels = graph3_labels[1:]
    graph3_total = graph3_total[1:]
    graph4_labels = graph4_labels[1:]
    graph4_total = graph4_total[1:]


    return render(request, 'charts.html', {
        'graph1_labels':graph1_labels,
        'graph1_total': graph1_total,
        'graph2_labels': graph2_labels,
        'graph2_total': graph2_total,
        'graph3_total': graph3_total,
        'graph3_labels': graph3_labels,
        'graph4_labels': graph4_labels,
        'graph4_total': graph4_total,
        'graph5_labels': graph5_label,
        'graph5_total': graph5_total,
        'graph6_labels': graph6_label,
        'graph6_total': graph6_data,
        'crop_id': pk,
    })

def chart_view(request):
    df = ['40kv', '100kv']
    df1 = [10000, 20000]
    my = {
        'df': df,
        'df1': df1
    }
    return render(request, 'expense_add.html', context=my)

@login_required(redirect_field_name='userlogin')
def delete(request, name, pk):
    if name== 'expenses':
        m = expenses.objects.get(exp_no=pk)
        print(m.exp_name)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'worker':
        m = worker.objects.get(worker_no=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'feed':
        m = feed.objects.get(feed_id=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'med':
        m = medicine.objects.get(med_id=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'ele':
        m = ele_bill.objects.get(bill_id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)
    if name == 'export':
        m = export.objects.get(exp_id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)
    if name == 'daily':
        m = daily_feed.objects.get(id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)

@login_required(redirect_field_name='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request, pk):
    if request.user.is_authenticated:

        # getting the total expenses for that particular crop
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)



        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1

        # getting the total feed used till now for that particular crop
        total_expense = int(sum([expense_sum, work_sum, ele_sum]))

        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            print('true')
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed/25)
            print(total_feed)
            print(total_bags)
        else:
            print('false')
            total_feed = '0'
            total_bags = '0'




        #graph1 content
        graph1_labels = ['Regular', 'Worker', 'Electrical']
        graph1_data = [expense_sum, work_sum, ele_sum]

        y = feed.objects.filter(crop_id=pk).filter(type='feed')
        try:
            x = []
            for i in y:
                x.append(i.quantity)
            print(sum(x), "is the total no of bags bought from amalapuram")
            s = sum(x) * 25
            print(s)

            if y:
                fee = []
                bags = []
                for i in y:
                    fee.append(i.bill_amount)
                    bags.append(i.quantity)
                feed_sum= sum(fee)
                feed_bags = sum(bags)
                graph1_labels = ['Regular', 'Worker', 'Electrical','Feed']
                graph1_data = [expense_sum, work_sum, ele_sum, feed_sum]

                z=feed.objects.filter(crop_id=pk).filter(type='other')
                other = []
                for i in z:
                    other.append(i.bill_amount)
                other_sum= sum(other)
                graph1_labels = ['Regular', 'Worker', 'Electrical', 'Feed', 'Other']
                graph1_data = [expense_sum, work_sum, ele_sum, feed_sum, other_sum]
                total_expense = int(sum([expense_sum, work_sum, ele_sum, feed_sum, other_sum]))
                t = abs(feed_bags - total_bags)
                print('total bags ia ', total_bags)
                print('feed bags', feed_bags)

                if t > 15:
                    messages.info(request,
                                  'The total bags does not match with the daily feed, please check if there is any '
                                  'discrepancy!')
        except:
            pass

        #graph 2 content
        f = export.objects.filter(crop_id=pk)
        exp = []
        for i in f:
            exp.append(i.amount)
        export_sum = sum(exp)
        print("the export sum is", export_sum)
        graph2_labels = ['Total spent', 'Total received']
        total_spent = sum(graph1_data)
        graph2_data = [total_spent,export_sum]

        d = main_crop.objects.get(crop_id=pk)
        user_id = d.user_id
        # getting the insights:
        #1 highest expense in that particular crop
        #2 highest daily feed in that particular crop

        if sum(graph1_data)==0:
            print("no data")
        crop = main_crop.objects.get(crop_id=pk)
        crops1 = main_crop.objects.filter(crop_id=pk).filter(status='completed')

        return render(request,'dashboard.html',{
            'total_expense':total_expense,
            'total_days':total_days,
            'total_feed': total_feed,
            'graph1_labels':graph1_labels,
            'graph1_total': graph1_data,
            'graph2_labels': graph2_labels,
            'graph2_total': graph2_data,
            'crop_id': pk,
            'user_id':user_id,
            'total_bags': total_bags,
            'crop':crop,
            'crops1':crops1
        })
    else:
        return redirect(user_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first']
        last_name = request.POST['second']
        try:
            a = User.objects.get(username=username)
            messages.info(request,"user already exists")
            return redirect(user_login)
        except DoesNotExist:
            user = User.objects.create_user(username=username,password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, 'Sign up successful!')
            return redirect(user_login)
    return render(request,'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)

        if user is not None:

            u = User.objects.get(username=username)
            crop = main_crop.objects.filter(user_id=u.id).filter(status='ongoing')
            print(crop)
            login(request, user)
            for c in crop:
                print(c.crop_name)
            crops1 = main_crop.objects.filter(user_id=u.id).filter(status='completed')
            context = {
                'crops': crop,
                'crops1':crops1
            }
            messages.success(request, 'logged in successfully!')
            return render(request, 'maindash.html', context=context)
        else:
            messages.info(request, "Invalid credentials, please try again!!")

    return render(request,'login.html')
@login_required(redirect_field_name='userlogin')
def user_logout(request):
    logout(request)
    messages.success(request, 'logged out successfully!')
    return redirect(landing_page)

# compare the feed quantity with the total no of bags

# use for a1- 100-18days
# for b1 - 100kg in 18 days
# foe a2 - 200kg in 18 days
# a2 200kg in 18 days
def add_data(request,pk):
    tank = 'B2'
    df = pd.read_csv('new_crop_sheet/B2-Table 1.csv')


    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    #df['date'] = pd.to_datetime(df['date'],errors='coerce', dayfirst=True)
    print(df)
    df = df.assign(tank=tank)
    print(df)
    row_iter = df.iterrows()
    obj = [
        daily_feed(
            date=row['date'],
            tank_no=tank,
            first=row['first'],
            second=row['second'],
            third=row['Third'],
            fourth=row['fourth'],
            crop_id=pk
        )
        for index,row in row_iter
    ]
    print(len(obj))
    daily_feed.objects.bulk_create(obj)
    return redirect(user_login)


def maindash_graph(request,pk):
    cr = main_crop.objects.filter(user_id=pk).distinct()
    ids = []
    crop_name = []
    for c in cr:
        ids.append(c.crop_id)
        crop_name.append(c.crop_name)
    crop_exp = []
    def total_exp(pk):
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)
        total_expense = int(sum([expense_sum,work_sum,ele_sum]))
        return total_expense
    # for adding expenses
    for i in ids:
        x = total_exp(i)
        crop_exp.append(x)
        print(x)
    print(crop_exp)
    # labels = crop_name and data = crop_exp
    # for graph 2 comparing total feed used by the crops
    def total_feed(pk):
        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed / 25)
            #print(total_bags)
        else:
            total_feed = 0
            total_bags = 0
        return total_feed,total_bags
    crop_feed = []
    for i in ids:
        x,y = total_feed(i)
        crop_feed.append(x)
    print(crop_feed)
    print(crop_name)
    # comparing the total no of days for the crops
    days=[]
    def get_days(pk):
        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk) # change the model after changing to the (ongoing and completed model)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1
        return total_days
    for i in ids:
        x = get_days(i)
        days.append(x)
    print(days)
    # comparing the electricity expenses of the crops
    total_ele = []
    def get_ele_exp(pk):
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)
        return ele_sum
    for i in ids:
        x = get_ele_exp(i)
        total_ele.append(x)
    print(total_ele)

    # getting the total export amount and material weight
    export_weight = []
    export_cost = []
    def get_export(pk):
        f = export.objects.filter(crop_id=pk)
        exp = []
        weight = []
        for i in f:
            exp.append(i.amount)
            weight.append(i.material_weight)
        export_sum = sum(exp)
        export_weight = sum(weight)
        print("the export sum is", export_sum)
        return export_weight,export_sum
    for i in ids:
        x,y = get_export(i)
        export_weight.append(x)
        export_cost.append(y)
    print(export_cost)
    print(export_weight)
    context={
        'graph1_labels':crop_name,
        'graph1_total':crop_exp,
        'graph2_labels':crop_name,
        'graph2_total': crop_feed,
        'graph3_labels':crop_name,
        'graph3_total': days,
        'graph4_labels': crop_name,
        'graph4_total':total_ele,
        'graph5_labels': crop_name,
        'graph5_total':export_cost,
        'graph6_labels': crop_name,
        'graph6_total':export_weight
    }

    return render(request,'maindash_graph.html',context=context)

def complete_btn_update(request,pk,days):
    c = main_crop.objects.get(crop_id=pk)
    c.status='completed'
    c.days=int(days)
    c.save()
    print("request executed")
    logout(request)
    messages.success(request, 'You have successfully completed the crop, please login again!')
    return redirect(user_login)
    #pk is the crop id
def completed_crop_dashboard(request,pk):
    if request.user.is_authenticated:

        # getting the total expenses for that particular crop
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)

        total_expense = int(sum([expense_sum,work_sum,ele_sum]))

        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1

        # getting the total feed used till now for that particular crop

        #graph1 content
        graph1_labels = ['Expenses', 'Worker Expenses', 'Electrical expenses']
        graph1_data = [expense_sum, work_sum, ele_sum]
        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            print('true')
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed/25)
            print(total_bags)
        else:
            print('false')
            total_feed = '0'
            total_bags = '0'
        y = feed.objects.filter(crop_id=pk).filter(type='feed')
        if y:
            fee = []
            bags = []
            for i in y:
                fee.append(i.bill_amount)
                bags.append(i.quantity)
            feed_sum= sum(fee)
            feed_bags = sum(bags)
            graph1_labels = ['Expenses', 'Worker Expenses', 'Electrical expenses','Feed expenses']
            graph1_data = [expense_sum, work_sum, ele_sum, feed_sum]

        #graph 2 content
        f = export.objects.filter(crop_id=pk)
        exp = []
        for i in f:
            exp.append(i.amount)
        export_sum = sum(exp)
        print("the export sum is", export_sum)
        graph2_labels = ['Total spent', 'Total received']
        total_spent = sum(graph1_data)
        graph2_data = [total_spent,export_sum]

        d = main_crop.objects.get(crop_id=pk)
        user_id = d.user_id
        # getting the insights:
        #1 highest expense in that particular crop
        #2 highest daily feed in that particular crop
        if sum(graph1_data)==0:
            print("no data")
        #crops1 = main_crop.objects.get
        crop = main_crop.objects.get(crop_id=pk)
        t = feed_bags-total_bags
        print(t)
        if t > 15:
            messages.info(request, 'The total no of feed bags does not match with daily feed!! please check if there is a discrepancy!')


        return render(request,'dashboard.html',{
            'total_expense':total_expense,
            'total_days':total_days,
            'total_feed': total_feed,
            'graph1_labels':graph1_labels,
            'graph1_total': graph1_data,
            'graph2_labels': graph2_labels,
            'graph2_total': graph2_data,
            'crop_id': pk,
            'user_id':user_id,
            'total_bags': total_bags,
            'crop':crop,
        })
    else:
        return redirect(user_login)
def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

def landing_page(request):
    return render(request,'landing_page.html')
