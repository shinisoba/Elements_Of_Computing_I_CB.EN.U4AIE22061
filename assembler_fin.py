#assembler - Group 5, Batch A
#opening the file 
f = open("C:/Users/sudha/OneDrive/Documents/EOC-I/EOC2/BatchA_Group5_Assignment4/MaxL.asm")
re_file = f.readlines() #reading as list
length = len(re_file)
i=0
#print(re_file)

#removing comments,inline comments and whitespaces
while i<length:
    if re_file[i].startswith("//"):
        re_file.remove(re_file[i])
        length-=1
    elif re_file[i].find("//")!=-1:
        s = re_file[i].split("//")
        re_file[i]=s[0]
    elif re_file[i] == "\n":
        re_file.remove(re_file[i])
        length-=1
    else:
        i+=1
        
#removing excess space
for s in range(0,length,1):
    srem = re_file[s].strip()
    re_file.remove(re_file[s])
    re_file.insert(s,srem)

rf = []
n_f = [] #list to store new elements

#removing the EOL character and adding the strings to a new list rf
for i in re_file:
    k=i.replace(" ","")
    rf.append(k.replace("\n",""))
nlen = len(rf)

#pre-defined symbols for A instruction 
pd_symbols = {"SCREEN":"16384","KBD":"24576",
            "R0":"0","R1":"1","R2":"2","R3":"3",
            "R4":"4","R5":"5","R6":"6","R7":"7",
            "R8":"8","R9":"9","R10":"10","R11":"11",
            "R12":"12","R13":"13","R14":"14","R15":"15",
            "SP":"0","LCL":"1","ARG":"2","THIS":"3","THAT":"4"}
label ={}

#to replace strings with pre-defined symbols with their numerical version
for v in range(0,nlen,1):
    if rf[v].startswith("@"):
        for val in pd_symbols:
            if (rf[v][1:])== val:
                aval = pd_symbols[val]
                rf.remove(rf[v])
                ainv = "@"+aval
                rf.insert(v,ainv)
                
#labels
u=1
for i in rf:
    if i.startswith("("):
        label[i[1:-1]]=str(u-1)
        u=u-1
    u=u+1
    
i=0
while(i<len(rf)):
    if rf[i].startswith("("):
        del rf[i]
    else:
        i=i+1

#print(rf)

k=16
for j in range(0,len(rf),1):
    i=rf[j]
    if i[0]=='@':
        if i[1:].isdigit():
            continue
        elif i[1:] in label:
            rf[j] = "@"+label[i[1:]]
        else:
            rf[j] = "@"+str(k)
            k=k+1

#print(rf)
# C instruction bits 
comp = {"0":"0101010","1":"0111111","-1":"0111010","D":"0001100","A":"0110000","!D":"0001101",
        "!A":"0110001","-D":"0001111","-A":"0110011","D+1":"0011111","A+1":"0110111","D-1":"0001110",
        "A-1":"0110111","D+A":"0000010","D-A":"0010011","A-D":"0000111","D&A":"0000000","D|A":"0010101",
        "M":"1110000","!M":"1110001","-M":"1110011","M+1":"1110111","M-1":"1110010","D+M":"1000010",
        "D-M":"1010011","M-D":"1000111","D&M":"1000000","D|M":"1010101"}
dest={"null":"000","M":"001","D":"010","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"}
jump ={"null":"000","JGT":"001","JEQ":"011","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}


cdest=""
ccomp = ""
cjump=""
c_ins=""
for j in range(0,len(rf),1):
    if rf[j].startswith("@"):
        anum = bin(int(rf[j][1:]))[2::]
        co = len(anum)
        a_ins = "0"*(16-co)+anum+'\n'
        n_f+=[a_ins]
        
    else:
        if rf[j].find("=")!=-1:
            destb,sep,compb = rf[j].partition("=")
            cdest = dest[destb]
            ccomp = comp[compb]
            c_ins = "111"+ccomp+cdest+"000"+'\n'
            n_f +=[c_ins]
            
        elif rf[j].find(";")!=-1:
            compb,sep,jumpb = rf[j].partition(";")
            ccomp = comp[compb]
            cjump = jump[jumpb]
            c_ins = "111"+ccomp+"000"+cjump+'\n'
            n_f +=[c_ins]

#printing the output binary code
for line in n_f:
    print(line)

#writing into new .hack file
hackf = open("C:/Users/sudha/OneDrive/Documents/EOC-I/EOC2/BatchA_Group5_Assignment4/MaxL.hack","w")
hackf.writelines(n_f)
hackf.close()
f.close()



