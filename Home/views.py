from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserAddForm
from .decorators import admin_only
from .blockgenerator import Block
from datetime import datetime
from .models import Block_2,Block_1,Block_3,Block_4
from .models import Block_1
from manu.models import Medicine


@admin_only
def Index(request):
    medicine = Medicine.objects.all()
    context = {
        "medicine":medicine
    }
    return render(request,"index.html",context)

def MakerIndex(request):
    return render(request,'manufacturer/makerindex.html')

def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or Password Incorrecr")
            return redirect('SignIn')
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            email = user.email 
            password = user.password
            username = user.username
            regdata = {"name":username,'email':email,"password":password}
            
            BlockChain = Block(1, datetime.now(), regdata,"0")
            
            block = Block_1.objects.create(BlockIndex = 1,BlockTimeStrap = datetime.now(),BlockLink = user,BlockData = regdata,previous_hash = "0",Blockhash = BlockChain.hash)
            block.save()
            
            messages.info(request,"User Created")
            return redirect('SignIn')
    return render(request,"register.html",{"form":form})

def SignOut(request):
    logout(request)
    return redirect('SignIn')

def ViewMed(request,pk):
    medi = Medicine.objects.get(id = pk)
    context = {
        "medi":medi
    }
    return render(request,'viewmedicine.html',context)

def ValidateMedicine(request,pk):
    medicine = Medicine.objects.get(id = pk)
    block4 = Block_4.objects.get(MedicineBlock = medicine)
    block3 = Block_3.objects.get(MedicineBlock = medicine)
    block2 = Block_2.objects.get(MedicineBlock = medicine)
    block1 = block2.BlockLink
    meddata = {"name":medicine.name,"manufacturer":medicine.manufacturer,"batch_number":medicine.batch_number,"expiry_date":medicine.expiry_date,"date_of_manufacture":medicine.date_of_manufacture,"owner":medicine.owner}
    BlockChanin2 = Block(3,medicine.timestamp,meddata,block2.Blockhash)
    
    blockdata = [block1,block2,block3]
    blockhashvalue = Block(4,"time",blockdata,block3.Blockhash)
    print(blockhashvalue)
    
    if BlockChanin2.hash == block3.Blockhash:
        if blockhashvalue.hash == block4.Blockhash:
            messages.success(request,"This Medicine is Valid")
            return redirect("ViewMed",pk=pk)            
        else:
            messages.info(request,"This Medicine is InValid")
            return redirect("ViewMed",pk=pk)
    else:
        messages.info(request,"This Medicine is InValid")
        return redirect("ViewMed",pk=pk)
    






