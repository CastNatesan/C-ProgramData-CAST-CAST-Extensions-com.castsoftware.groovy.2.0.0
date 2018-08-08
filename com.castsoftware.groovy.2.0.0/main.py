from lxml.doctestcompare import strip
from _ast import Or
from sqlalchemy.sql.expression import true
import cast.analysers.ua
import cast.analysers.log as Print

from cast.analysers import CustomObject,Bookmark,create_link
import re
from numpy.core.defchararray import endswith
from pydoc import classname
import cast.application


# from fileinput import filename

#AngularJS_NgModule=CustomObject()
finalData={"classObject":[],"abstractObject":[],"functionLink":[]};
class GroovyExtension(cast.analysers.ua.Extension):
    def __init__(self):
        self.k = 1
        self.filename=""
        self.file = "" 
        self.name=""
        cnt= 0
    
    def start_analysis(self):
        self.intermediate_file_providers= self.get_intermediate_file("Class.txt")
        self.intermediate_file_Functions= self.get_intermediate_file("Functions.txt")
        Print.info("Start Analysis!")
        pass
    
    def start_file(self, file):
        Print.info("Start f!")
        contentList=[]
        #self.file = file
        #self.filename = "C:/Users/Angelin.mariya/Desktop/app.module.ts";
        self.filename = file.get_path();
        self.file=file;
        #Print.info("###############printing file name############")
        #Print.info("FileName--" + str(self.filename))
        file_ref = open(self.filename,encoding='UTF_8')
        #contentList=[];
        for i in file_ref:
            contentList.append(str(i)); 
        
        indexOfClass=self.findIndex(contentList,"[c][l][a][s][s][\s]*.*[{]",0)
        indexOfFunction=self.findIndex(contentList,"([v][o][i][d][\s]*|[s][t][r][i][n][g][\s]*|[i][n][t][\s]*).*[(].*[)][\s]+[{]",0)
        Print.info(str(indexOfFunction));
        classNameLine=contentList[indexOfClass];
        #className=classNameLine.replace('{',' ');
        className=classNameLine.split("{");
        className=className[0].split(" ");
        classObject="NA";
        abstractClassObject="NA";
        functionConnections=[];
        if className[0].strip()=="class":
            classObject=className[1];
            finalData["classObject"].append([classObject,indexOfClass]);
            Groovy_class=CustomObject();
            self.saveObject(Groovy_class,str(classObject),self.filename+str(classObject),"Groovy_class",self.file,self.filename+"Groovy_class")
            Groovy_class.save();
            Groovy_class.save_position(Bookmark(self.file,indexOfClass+1,1,indexOfClass+1,-1));
            functionList,functionConnections=self.getFunctionList(contentList,"([v][o][i][d][\s]*|[s][t][r][i][n][g][\s]*|[i][n][t][\s]*).*[(].*[)][\s]+[{]")
            for i in functionConnections:
                finalData["functionLink"].append(i);
            for i in functionList:
                Groovy_Function=CustomObject()
                self.saveObject(Groovy_Function,str(i[0]),self.filename+str(i[0]),"Groovy_Function",self.file,self.filename+str(i[0]))
                Groovy_Function.save()
                Groovy_Function.save_position(Bookmark(self.file,i[1],1,i[1],-1))
                create_link('containLink',Groovy_class,Groovy_Function) 
        elif className[0].strip()=="abstract":
            abstractClassObject=className[2];
            finalData["abstractObject"].append([abstractClassObject,indexOfClass]);
            Groovy_AbstractClass=CustomObject();
            self.saveObject(Groovy_AbstractClass,str(abstractClassObject),self.filename+str(abstractClassObject),"Groovy_AbstractClass",self.file,self.filename+"Groovy_AbstractClass")
            Groovy_AbstractClass.save()
            Groovy_AbstractClass.save_position(Bookmark(self.file,indexOfClass+1,1,indexOfClass+1,-1));
            functionList,functionConnections=self.getFunctionList(contentList,"([v][o][i][d][\s]*|[s][t][r][i][n][g][\s]*|[i][n][t][\s]*).*[(].*[)][\s]+[{]")
            for i in functionConnections:
                finalData["functionLink"].append(i);
            for i in functionList:
                Groovy_Function=CustomObject()
                self.saveObject(Groovy_Function,str(i[0]),self.filename+str(i[0]),"Groovy_Function",self.file,self.filename+str(i[0]))
                print("groovy object saved");
                Groovy_Function.save()
                Groovy_Function.save_position(Bookmark(self.file,i[1],1,i[1],-1))
                create_link('containLink',Groovy_AbstractClass,Groovy_Function) 
        in1=self.findIndex(contentList,"([v][o][i][d][\s]*|[s][t][r][i][n][g][\s]*|[i][n][t][\s]*).*[(].*[)][\s]+[{]",0);
        print("sad",in1);
        #print("to",functionList);
        # save violation rule
        Groovy_Function.save_violation("Groovy_CustomMetrics.AssertWithinFinallyBlock",
                             Bookmark(file, 1, 1, -1, -1), additional_bookmarks=None)

        Print.info('Groovy  Violation  Saved for demo')

        self.validate(file)
        Print.info(str(functionList));
        return contentList;
        
    def findIndex(self,content,tag,index):
        Print.info("aws"+str(index));
        for i in content:
            if re.search(tag,i):
                return index;
            index+=1;       
        return -1; 

    def validate(self,file):
        self.filename = file.get_path();
        self.file = file;
        fList = open(self.filename, encoding='UTF_8')
        for i in fList:
            # if str(i).strip().__len__() > 0:
            #fList.append(str(i).strip())

            print(fList)
        
#             for line in range(0, len(fList.read()) - 1):
#     
# #                 if fList[line].__contains__("class"):
#                     print(fList[line])
#                     cls = fList[line].split("class")
#                     cls = cls[1].split(" ")
#                     print(cls)
#                     if len(cls) > 0:
#                         classname = cls[1]
#                 r1 = re.findall(r"(?:void|int|string)", fList[line])
#                 if len(r1) > 0:
#                     # print("rehexp",r1)
#                     fun = fList[line].split(r1[0])
#                     fun = fun[1].replace('(', '')
#                     print(fun)
#                     ''''''
#                 count = 0
#                 if fList[line].__contains__("finally"):
#                     print(fList[line], line)
    
#                     for l in range(line + 1, len(fList) - 1):
#                         print("function lines", l, fList[l])
#                         '''AssertWithinFinallyBlock'''
#                         if fList[l].__contains__("assert"):
#                             print("Finally block contains assert", fList[l], "line number", str(l + 1), "classname:",
#                                   classname, "Funation:", fun)
#                             Rule1 = cast.analysers.CustomObject()
#                             Rule1.set_name(fun)
#                             Rule1.set_type('Groovy_class')
#                             parentFile = file.get_position()
#                             Rule1.set_parent(file)
#                             Rule1.set_fullname(classname+'-'+fun)
#                             Rule1.set_guid(self.filename + fun )
#                             Rule1.save()
#                             Rule1.save_position(file.get_position())
#                             Print.info('Groovy  Object Saved for demo')
#     
#                             # save violation rule
#                             Rule1.save_violation("Groovy_CustomMetrics.AssertWithinFinallyBlock",
#                                                         Bookmark(file, l+1, 1, -1, -1), additional_bookmarks=None)
#     
#                             Print.info('Groovy  Violation  Saved for demo')



    def getFunctionList(self,content,tag):
        functionList=[];
        connectionList=[];
        index=0;
        lengthOfContent=len(content);
        for i in range(0,lengthOfContent):
            index+=1;
            if re.search("([v][o][i][d][\s]*|[M][a][p].*|[s][t][r][i][n][g][\s]*|[i][n][t][\s]*).*[(].*[)][\s]+[{]",content[i]):
                countOfBracket=1;
                functionNameList=content[i].split("(");
                functionName=functionNameList[0].split(" ")[-1];
                functionList.append([functionName.strip(),index]);
                i=i+2;  
                while countOfBracket!=0:
                    if re.search("{",content[i]):
                        countOfBracket+=1;
                    if re.search("}",content[i]):
                        countOfBracket-=1;
                    if re.search("[a-zA-Z]*[.][a-zA-Z]*[(].*[)]",content[i]):
                        functionCallName=content[i].split(".")[1].split("(")[0].strip();
                        if functionCallName!="run":
                            connectionList.append([functionName,functionCallName]);
                    i+=1;
        Print.info(str(connectionList));
        Print.info(str(functionList));
        return functionList,connectionList;

    def end_file(self,file):
        #Print.info.info("declartions" + str(tsDeclarationsList))
        #cast.analysers.log.info("End file!")
        pass
        
        
    def end_analysis(self):
        Print.info(str(finalData))
        self.intermediate_file_Functions.write(str(finalData));
        pass
    def saveObject(self,obj_reference,name,fullname,obj_type,parent,guid): 
        obj_reference.set_name(name)
        cast.analysers.log.info("Obj_Name--------!" +str(name))
        obj_reference.set_fullname(fullname)
        obj_reference.set_type(obj_type)
        cast.analysers.log.info("Obj_Type--------!" +str(obj_type))
        obj_reference.set_parent(parent)
        cast.analysers.log.info("Obj_parent--------!" +str(parent))
        obj_reference.set_guid(guid) 
        cast.analysers.log.info("Obj_guid--------!" +str(guid))
        pass